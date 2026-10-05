const path = require("path");

let hre;
try {
  hre = require("hardhat");
} catch {
  hre = require(path.resolve(__dirname, "../../prototype/node_modules/hardhat"));
}
const { ethers } = hre;

function analyzeCalldata(hexData) {
  const bytes = ethers.getBytes(hexData);
  let zero = 0;
  let nonZero = 0;
  for (const b of bytes) {
    if (b === 0) zero++;
    else nonZero++;
  }
  return { cost: zero * 4 + nonZero * 16, zero, nonZero, totalBytes: bytes.length };
}

function countNonZeroBytes(bytes32Hex) {
  const bytes = ethers.getBytes(bytes32Hex);
  let count = 0;
  for (const b of bytes) {
    if (b !== 0) count++;
  }
  return count;
}

async function executeRevocation(contract, issuer, revoker, batchIdStr, leafHash, reasonStr) {
  const snapshotId = await ethers.provider.send("evm_snapshot", []);
  const encodedBatchId = ethers.encodeBytes32String(batchIdStr);
  await contract.connect(issuer).issueBatch(encodedBatchId, ethers.keccak256("0x1234"), 6, "ipfs://meta");

  const tx = await contract.connect(revoker).revokeCredential(leafHash, encodedBatchId, reasonStr);
  const receipt = await tx.wait();
  const calldata = analyzeCalldata(tx.data);

  await ethers.provider.send("evm_revert", [snapshotId]);

  return {
    batchIdStr,
    encodedBatchId,
    batchIdBytes: 32,
    batchIdNonZero: countNonZeroBytes(encodedBatchId),
    reasonStr,
    reasonBytes: Buffer.byteLength(reasonStr, "utf8"),
    gasUsed: Number(receipt.gasUsed),
    calldataCost: calldata.cost,
    zeroBytes: calldata.zero,
    nonZeroBytes: calldata.nonZero,
  };
}

function printRunSummary(title, run, baseRun = null) {
  console.log(title);
  console.log(`Batch ID          : "${run.batchIdStr}" (Bytes: ${run.batchIdBytes}, Non-zero: ${run.batchIdNonZero})`);
  console.log(`Reason            : "${run.reasonStr}" (Bytes: ${run.reasonBytes})`);
  console.log(`Calldata Gas      : ${run.calldataCost} (Non-zero: ${run.nonZeroBytes}, Zero: ${run.zeroBytes})`);
  console.log(`Gas Receipt       : ${run.gasUsed} unit`);

  if (!baseRun) {
    console.log(`Status Nilai Demo : ${run.gasUsed === 56359 ? "COCOK 56.359" : "BEDA"}\n`);
    return;
  }

  const deltaGas = run.gasUsed - baseRun.gasUsed;
  const deltaCalldata = run.calldataCost - baseRun.calldataCost;
  const residual = deltaGas - deltaCalldata;
  console.log(`Selisih vs Run A  : ${deltaGas} gas`);
  console.log(`Prediksi Calldata : ${deltaCalldata} gas`);
  console.log(`SISA (Terukur-Cd) : ${residual} gas\n`);
}

async function runWordBoundaryTests(contract, issuer, revoker, demoBatchIdStr, demoLeaf, baseRun) {
  console.log("Run D: Uji lompatan batas word 32 byte event log data");
  const testReasons = [
    { len: 11, str: "Sidang Etik" },
    { len: 31, str: "1234567890123456789012345678901" },
    { len: 32, str: "12345678901234567890123456789012" },
    { len: 33, str: "123456789012345678901234567890123" },
    { len: 60, str: "Putusan Sidang Komite Etik: Terbukti Plagiarisme Tugas Akhir" }
  ];

  for (const item of testReasons) {
    const res = await executeRevocation(contract, issuer, revoker, demoBatchIdStr, demoLeaf, item.str);
    const deltaGas = res.gasUsed - baseRun.gasUsed;
    const deltaCalldata = res.calldataCost - baseRun.calldataCost;
    const residual = deltaGas - deltaCalldata;
    console.log(`Reason (${item.len} byte) : Gas=${res.gasUsed} | Calldata=${res.calldataCost} | Selisih Gas=${deltaGas} | Selisih Cd=${deltaCalldata} | SISA=${residual}`);
  }
  console.log("");
}

async function runBenchmarkVariations(contract, issuer, revoker, demoLeaf, baseRun) {
  console.log("Run E: Benchmark batch-id (N=6, 100, 1000) dengan reason 'Sidang Etik'");
  const benchmarkBatches = ["BATCH-6-ITER-1", "BATCH-100-ITER-1", "BATCH-1000-ITER-1"];
  for (const batchStr of benchmarkBatches) {
    const res = await executeRevocation(contract, issuer, revoker, batchStr, demoLeaf, "Sidang Etik");
    const deltaGas = res.gasUsed - baseRun.gasUsed;
    const deltaCalldata = res.calldataCost - baseRun.calldataCost;
    const residual = deltaGas - deltaCalldata;
    const nonZeroCount = countNonZeroBytes(ethers.encodeBytes32String(batchStr));
    console.log(`Batch "${batchStr}" (${nonZeroCount} non-zero) : Gas=${res.gasUsed} | Calldata=${res.calldataCost} | Selisih Gas=${deltaGas} | Selisih Cd=${deltaCalldata} | SISA=${residual}`);
  }
}

async function main() {
  const [admin, issuer, revoker] = await ethers.getSigners();
  const Factory = await ethers.getContractFactory("AcademicCredentialRegistry");
  const contract = await Factory.deploy(admin.address, issuer.address, revoker.address);
  await contract.waitForDeployment();

  const demoLeaf = "0xf3695a1ce4a97902b58bf9bb868bac471c484bcedec9edfbb1a8290fa86a1575";
  const demoBatchIdStr = "WISUDA-2026-PERIODE-1";
  const demoReason = "Putusan Sidang Komite Etik: Terbukti Plagiarisme Tugas Akhir";

  console.log("Eksperimen uji variabel gas revokeCredential (exp_b06_v2)");
  console.log("Pemeriksaan Panjang String Reason Demo:");
  console.log(`- String : "${demoReason}"`);
  console.log(`- reason.length (karakter UTF-16) : ${demoReason.length}`);
  console.log(`- Buffer.byteLength (byte UTF-8)  : ${Buffer.byteLength(demoReason, "utf8")}`);
  console.log("(Perbedaan 60 vs 61 terselesaikan: panjang sebenarnya adalah 60 karakter/byte; penyebutan 61 sebelumnya merupakan salah hitung manual).\n");

  const runA = await executeRevocation(contract, issuer, revoker, demoBatchIdStr, demoLeaf, demoReason);
  printRunSummary("Run A (Identik Demo)", runA);

  const runB = await executeRevocation(contract, issuer, revoker, "BATCH-6-ITER-1", demoLeaf, demoReason);
  printRunSummary("Run B (Hanya BatchId Berubah ke BATCH-6-ITER-1)", runB, runA);

  const runC = await executeRevocation(contract, issuer, revoker, demoBatchIdStr, demoLeaf, "Sidang Etik");
  printRunSummary("Run C (Hanya Reason Berubah ke 'Sidang Etik')", runC, runA);

  await runWordBoundaryTests(contract, issuer, revoker, demoBatchIdStr, demoLeaf, runA);
  await runBenchmarkVariations(contract, issuer, revoker, demoLeaf, runA);
}

main().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
