const path = require("path");
const hre = require(path.resolve(__dirname, "../../prototype/node_modules/hardhat"));
const { ethers } = hre;

function analyzeCalldata(hexData) {
  const bytes = ethers.getBytes(hexData);
  let zero = 0;
  let nonZero = 0;
  for (const b of bytes) {
    if (b === 0) zero++;
    else nonZero++;
  }
  const cost = zero * 4 + nonZero * 16;
  return { cost, zero, nonZero, totalBytes: bytes.length };
}

function countNonZeroBytes(bytes32Hex) {
  const bytes = ethers.getBytes(bytes32Hex);
  let nonZero = 0;
  for (const b of bytes) {
    if (b !== 0) nonZero++;
  }
  return nonZero;
}

async function main() {
  const [admin, issuer, revoker] = await ethers.getSigners();
  const Factory = await ethers.getContractFactory("AcademicCredentialRegistry");
  const contract = await Factory.deploy(admin.address, issuer.address, revoker.address);
  await contract.waitForDeployment();

  const demoLeaf = "0xf3695a1ce4a97902b58bf9bb868bac471c484bcedec9edfbb1a8290fa86a1575";
  const demoBatchIdStr = "WISUDA-2026-PERIODE-1";
  const demoBatchId = ethers.encodeBytes32String(demoBatchIdStr);
  const demoReason = "Putusan Sidang Komite Etik: Terbukti Plagiarisme Tugas Akhir";

  console.log("=== EKSPERIMEN UJI VARIABEL GAS REVOKECREDENTIAL (exp_b06_v2) ===");
  console.log(`Pemeriksaan Panjang String Reason Demo:`);
  console.log(`- String : "${demoReason}"`);
  console.log(`- reason.length (karakter UTF-16) : ${demoReason.length}`);
  console.log(`- Buffer.byteLength (byte UTF-8)  : ${Buffer.byteLength(demoReason, "utf8")}`);
  console.log(`(Perbedaan 60 vs 61 terselesaikan: panjang sebenarnya adalah 60 karakter/byte; penyebutan 61 sebelumnya merupakan salah hitung manual).\n`);

  async function executeRevoke(batchIdStr, leafHash, reasonStr) {
    const snap = await ethers.provider.send("evm_snapshot", []);
    const bId = ethers.encodeBytes32String(batchIdStr);
    await contract.connect(issuer).issueBatch(bId, ethers.keccak256("0x1234"), 6, "ipfs://meta");

    const tx = await contract.connect(revoker).revokeCredential(leafHash, bId, reasonStr);
    const rc = await tx.wait();
    const cd = analyzeCalldata(tx.data);

    await ethers.provider.send("evm_revert", [snap]);

    return {
      batchIdStr,
      bId,
      batchIdBytes: 32,
      batchIdNonZero: countNonZeroBytes(bId),
      reasonStr,
      reasonBytes: Buffer.byteLength(reasonStr, "utf8"),
      gasUsed: Number(rc.gasUsed),
      calldataCost: cd.cost,
      zeroBytes: cd.zero,
      nonZeroBytes: cd.nonZero,
    };
  }

  // Run A
  const runA = await executeRevoke(demoBatchIdStr, demoLeaf, demoReason);
  console.log("--- RUN A (Identik Demo) ---");
  console.log(`Batch ID          : "${runA.batchIdStr}" (Bytes: ${runA.batchIdBytes}, Non-zero: ${runA.batchIdNonZero})`);
  console.log(`Reason            : "${runA.reasonStr}" (Bytes: ${runA.reasonBytes})`);
  console.log(`Calldata Gas      : ${runA.calldataCost} (Non-zero: ${runA.nonZeroBytes}, Zero: ${runA.zeroBytes})`);
  console.log(`Gas Receipt       : ${runA.gasUsed} unit`);
  console.log(`Status Nilai Demo : ${runA.gasUsed === 56359 ? "COCOK 56.359" : "BEDA"}\n`);

  // Helper printer
  function printRunComparison(label, run) {
    const deltaGas = run.gasUsed - runA.gasUsed;
    const deltaCd = run.calldataCost - runA.calldataCost;
    const sisa = deltaGas - deltaCd;
    console.log(`--- ${label} ---`);
    console.log(`Batch ID          : "${run.batchIdStr}" (Bytes: ${run.batchIdBytes}, Non-zero: ${run.batchIdNonZero})`);
    console.log(`Reason            : "${run.reasonStr}" (Bytes: ${run.reasonBytes})`);
    console.log(`Calldata Gas      : ${run.calldataCost} (Non-zero: ${run.nonZeroBytes}, Zero: ${run.zeroBytes})`);
    console.log(`Gas Receipt       : ${run.gasUsed} unit`);
    console.log(`Selisih vs Run A  : ${deltaGas} gas`);
    console.log(`Prediksi Calldata : ${deltaCd} gas`);
    console.log(`SISA (Terukur-Cd) : ${sisa} gas\n`);
    return { deltaGas, deltaCd, sisa };
  }

  // Run B: hanya batchId diganti ke BATCH-6-ITER-1
  const runB = await executeRevoke("BATCH-6-ITER-1", demoLeaf, demoReason);
  printRunComparison("RUN B (Hanya BatchId Berubah ke BATCH-6-ITER-1)", runB);

  // Run C: hanya reason diganti ke Sidang Etik (11 karakter)
  const runC = await executeRevoke(demoBatchIdStr, demoLeaf, "Sidang Etik");
  printRunComparison("RUN C (Hanya Reason Berubah ke 'Sidang Etik')", runC);

  // Run D: Variasi panjang reason (11, 31, 32, 33, 60 karakter)
  console.log("=== RUN D: UJI LOMPATAN BATAS WORD 32 BYTE EVENT LOG DATA ===");
  const testReasons = [
    { len: 11, str: "Sidang Etik" },
    { len: 31, str: "1234567890123456789012345678901" },
    { len: 32, str: "12345678901234567890123456789012" },
    { len: 33, str: "123456789012345678901234567890123" },
    { len: 60, str: "Putusan Sidang Komite Etik: Terbukti Plagiarisme Tugas Akhir" }
  ];

  for (const tr of testReasons) {
    const resD = await executeRevoke(demoBatchIdStr, demoLeaf, tr.str);
    const deltaGas = resD.gasUsed - runA.gasUsed;
    const deltaCd = resD.calldataCost - runA.calldataCost;
    const sisa = deltaGas - deltaCd;
    console.log(`Reason (${tr.len} byte) : Gas=${resD.gasUsed} | Calldata=${resD.calldataCost} | Selisih Gas=${deltaGas} | Selisih Cd=${deltaCd} | SISA=${sisa}`);
  }
  console.log("");

  // Run E: Benchmark Batch IDs dengan reason "Sidang Etik"
  console.log("=== RUN E: BENCHMARK BATCH-ID (N=6, 100, 1000) DENGAN REASON 'Sidang Etik' ===");
  const benchBatches = ["BATCH-6-ITER-1", "BATCH-100-ITER-1", "BATCH-1000-ITER-1"];
  for (const bStr of benchBatches) {
    const resE = await executeRevoke(bStr, demoLeaf, "Sidang Etik");
    const deltaGas = resE.gasUsed - runA.gasUsed;
    const deltaCd = resE.calldataCost - runA.calldataCost;
    const sisa = deltaGas - deltaCd;
    console.log(`Batch "${bStr}" (${countNonZeroBytes(ethers.encodeBytes32String(bStr))} non-zero) : Gas=${resE.gasUsed} | Calldata=${resE.calldataCost} | Selisih Gas=${deltaGas} | Selisih Cd=${deltaCd} | SISA=${sisa}`);
  }
}

main().catch(console.error);
