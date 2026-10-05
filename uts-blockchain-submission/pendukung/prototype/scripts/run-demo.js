const { ethers } = require("hardhat");
const {
  generateSalt,
  computeCredentialLeaf,
  buildCredentialMerkleTree,
  getMerkleProof,
} = require("./lib/crypto-utils");

async function deployRegistry(adminAddress, issuerAddress, revokerAddress) {
  const Factory = await ethers.getContractFactory("AcademicCredentialRegistry");
  const contract = await Factory.deploy(adminAddress, issuerAddress, revokerAddress);
  await contract.waitForDeployment();
  const receipt = await contract.deploymentTransaction().wait();
  return { contract, receipt };
}

function prepareSimulatedCredentials() {
  const graduates = [
    {
      id: "G-01",
      nim: "237006801",
      nama: "Ahmad Dahlan Al-Faruq",
      prodi: "Informatika",
      fakultas: "Teknik",
      ipk: "3.82",
      predikat: "Dengan Pujian",
      nomorIjazah: "IJZ/UNSIL/FT/2026/0801",
    },
    {
      id: "G-02",
      nim: "237006802",
      nama: "Bunga Citra Lestari Fiktif",
      prodi: "Informatika",
      fakultas: "Teknik",
      ipk: "3.65",
      predikat: "Sangat Memuaskan",
      nomorIjazah: "IJZ/UNSIL/FT/2026/0802",
    },
    {
      id: "G-03",
      nim: "237006803",
      nama: "Cahyo Rizki Pratama",
      prodi: "Sistem Informasi",
      fakultas: "Teknik",
      ipk: "3.91",
      predikat: "Dengan Pujian",
      nomorIjazah: "IJZ/UNSIL/FT/2026/0803",
    },
    {
      id: "G-04",
      nim: "237006804",
      nama: "Dewi Sekar Ayu",
      prodi: "Informatika",
      fakultas: "Teknik",
      ipk: "3.45",
      predikat: "Memuaskan",
      nomorIjazah: "IJZ/UNSIL/FT/2026/0804",
    },
    {
      id: "G-05",
      nim: "237006805",
      nama: "Eko Prasetyo Fiktif",
      prodi: "Teknik Elektro",
      fakultas: "Teknik",
      ipk: "3.55",
      predikat: "Sangat Memuaskan",
      nomorIjazah: "IJZ/UNSIL/FT/2026/0805",
    },
    {
      id: "G-06",
      nim: "237006806",
      nama: "Farhan Maulana",
      prodi: "Informatika",
      fakultas: "Teknik",
      ipk: "3.78",
      predikat: "Dengan Pujian",
      nomorIjazah: "IJZ/UNSIL/FT/2026/0806",
    },
  ];

  const credentialRecords = graduates.map((graduate) => {
    const salt = generateSalt();
    const leafData = computeCredentialLeaf(graduate, salt);
    return {
      graduate,
      salt,
      claimHash: leafData.claimHash,
      leafHash: leafData.leafHash,
    };
  });

  const leafHashes = credentialRecords.map((record) => record.leafHash);
  const { tree, root } = buildCredentialMerkleTree(leafHashes);
  return { credentialRecords, tree, root };
}

function calculateCalldataCost(encodedHexData) {
  const bytes = ethers.getBytes(encodedHexData);
  let cost = 0;
  for (const b of bytes) {
    cost += b === 0 ? 4 : 16;
  }
  return cost;
}

async function main() {
  const network = await ethers.provider.getNetwork();
  console.log(`Lingkungan: Hardhat Local Network | Chain ID: ${network.chainId}`);
  console.log(`Waktu Eksekusi: ${new Date().toISOString()}`);
  console.log("");

  const [admin, issuer, revoker, student, verifier, attacker] = await ethers.getSigners();
  console.log(`Admin (Governance) : ${admin.address}`);
  console.log(`Issuer (Akademik)  : ${issuer.address}`);
  console.log(`Revoker (Komite)   : ${revoker.address}`);
  console.log(`Pemegang (Holder)  : ${student.address}`);
  console.log(`Verifikator        : ${verifier.address}`);
  console.log(`Pihak Tak Berwenang: ${attacker.address}`);
  console.log("");

  // B-01: Deployment Kontrak
  console.log("[B-01 Deployment Kontrak AcademicCredentialRegistry]");
  const { contract, receipt: deployReceipt } = await deployRegistry(
    admin.address,
    issuer.address,
    revoker.address
  );
  const contractAddress = await contract.getAddress();
  console.log(`Alamat Kontrak       : ${contractAddress}`);
  console.log(`Tx Hash Deployment   : ${deployReceipt.hash}`);
  console.log(`Block Number         : ${deployReceipt.blockNumber}`);
  console.log(`Gas Terpakai (Deploy): ${deployReceipt.gasUsed.toString()} unit`);
  console.log("");

  // B-02: Pembuatan Kredensial Merkle Tree
  console.log("[B-02 Pembangkitan Kredensial Salted Hash dan Merkle Tree]");
  const { credentialRecords, tree, root } = prepareSimulatedCredentials();
  console.log(`Jumlah Kredensial    : ${credentialRecords.length} lulusan`);
  credentialRecords.forEach((record) => {
    console.log(
      `  [${record.graduate.id}] NIM: ${record.graduate.nim} | Nama: ${record.graduate.nama.padEnd(26)} | IPK: ${record.graduate.ipk} | Leaf: ${record.leafHash.substring(0, 18)}...`
    );
  });
  console.log(`Merkle Root Terhitung: ${root}`);
  console.log("");

  // B-03: Penjangkaran On-Chain Root Batch
  console.log("[B-03 Penjangkaran Root Batch On-Chain]");
  const batchId = ethers.encodeBytes32String("WISUDA-2026-PERIODE-1");
  const metadataURI = "ipfs://bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi/metadata.json";

  const issueTx = await contract
    .connect(issuer)
    .issueBatch(batchId, root, credentialRecords.length, metadataURI);
  const issueReceipt = await issueTx.wait();

  console.log(`Batch ID             : ${ethers.decodeBytes32String(batchId)}`);
  console.log(`Tx Hash Penerbitan   : ${issueReceipt.hash}`);
  console.log(`Block Number         : ${issueReceipt.blockNumber}`);
  console.log(`Gas Terpakai (Batch) : ${issueReceipt.gasUsed.toString()} unit`);
  const storedBatch = await contract.batches(batchId);
  console.log(`Root Tersimpan State : ${storedBatch.merkleRoot}`);
  console.log("");

  // B-04: Verifikasi Sah Kredensial
  console.log("[B-04 Verifikasi Keabsahan Dokumen dan Bukti Merkle]");
  const targetStudent = credentialRecords[0];
  const proofTarget = getMerkleProof(tree, targetStudent.leafHash);

  console.log(`Mahasiswa Diuji      : ${targetStudent.graduate.nama} (${targetStudent.graduate.nim})`);
  console.log(`Leaf Hash Diajukan   : ${targetStudent.leafHash}`);
  console.log(`Panjang Merkle Proof : ${proofTarget.length} siblings`);
  proofTarget.forEach((p, idx) => console.log(`  Proof[${idx}]: ${p}`));

  const [isValid, statusMsg] = await contract
    .connect(verifier)
    .verifyCredential(batchId, targetStudent.leafHash, proofTarget);

  const rawGasEstimate = await contract
    .connect(verifier)
    .verifyCredential.estimateGas(batchId, targetStudent.leafHash, proofTarget);

  const encodedCalldata = contract.interface.encodeFunctionData("verifyCredential", [
    batchId,
    targetStudent.leafHash,
    proofTarget,
  ]);
  const calldataCost = calculateCalldataCost(encodedCalldata);
  const pureExecutionGas = Number(rawGasEstimate) - 21000 - calldataCost;

  console.log(`Hasil Verifikasi     : ${isValid ? "SAH / VALID (TRUE)" : "TIDAK VALID"}`);
  console.log(`Pesan Status Kontrak : ${statusMsg}`);
  console.log(`Biaya Gas Verifikator: 0 gas (Dipanggil via eth_call view query, bebas biaya)`);
  console.log(`Raw estimateGas      : ${rawGasEstimate.toString()} unit (Simulasi EVM termasuk 21.000 gas transaksi)`);
  console.log(`Biaya Calldata       : ${calldataCost} gas (EIP-2028: 16 gas non-zero, 4 gas zero byte)`);
  console.log(`Estimasi Gas Murni   : ${pureExecutionGas} unit (Opcode murni eksekusi loop MerkleProof.verify)`);
  console.log("");

  // B-05: Uji Anti-Tampering dan Kontrol Akses RBAC
  console.log("[B-05 Uji Ketahanan Manipulasi Data dan Kontrol Akses RBAC]");
  console.log("Skenario 5A: Pelamar mengubah IPK 3.82 menjadi 4.00 pada berkas lokal");
  const tamperedGrad = { ...targetStudent.graduate, ipk: "4.00" };
  const tamperedLeaf = computeCredentialLeaf(tamperedGrad, targetStudent.salt);
  console.log(`Leaf Asli            : ${targetStudent.leafHash}`);
  console.log(`Leaf Hasil Manipulasi: ${tamperedLeaf.leafHash}`);

  const [isValidTampered, msgTampered] = await contract
    .connect(verifier)
    .verifyCredential(batchId, tamperedLeaf.leafHash, proofTarget);
  console.log(`Hasil Verifikasi     : ${isValidTampered ? "SAH" : "DITOLAK / INVALID (FALSE)"}`);
  console.log(`Pesan Status Kontrak : ${msgTampered}`);
  console.log("");

  console.log("Skenario 5B: Upaya penerbitan batch oleh penyerang tanpa hak (Attacker)");
  try {
    await contract
      .connect(attacker)
      .issueBatch(ethers.encodeBytes32String("BATCH-PALSU"), root, 10, "ipfs://palsu");
    console.log("Peringatan: Transaksi attacker berhasil!");
  } catch (err) {
    console.log(`Hasil Pencegatan RBAC: Transaksi Dibatalkan (Reverted)`);
    console.log(`Eksepsi Kontrak      : ${err.message.split("(")[0].trim()}`);
  }
  console.log("");

  // B-06: Pencabutan Kredensial
  console.log("[B-06 Pencabutan Kredensial Akademik oleh REVOKER_ROLE]");
  const revokedTarget = credentialRecords[1];
  const proofRevoked = getMerkleProof(tree, revokedTarget.leafHash);

  const [statusBeforeRevoke] = await contract.verifyCredential(
    batchId,
    revokedTarget.leafHash,
    proofRevoked
  );
  console.log(`Status Sebelum Cabut : ${statusBeforeRevoke ? "VALID" : "INVALID"}`);

  const revokeReason = "Putusan Sidang Komite Etik: Terbukti Plagiarisme Tugas Akhir";
  const revokeTx = await contract
    .connect(revoker)
    .revokeCredential(revokedTarget.leafHash, batchId, revokeReason);
  const revokeReceipt = await revokeTx.wait();

  console.log(`Mahasiswa Dicabut    : ${revokedTarget.graduate.nama} (${revokedTarget.graduate.nim})`);
  console.log(`Tx Hash Pencabutan   : ${revokeReceipt.hash}`);
  console.log(`Gas Terpakai (Revoke): ${revokeReceipt.gasUsed.toString()} unit`);

  const [statusAfterRevoke, msgAfterRevoke] = await contract
    .connect(verifier)
    .verifyCredential(batchId, revokedTarget.leafHash, proofRevoked);
  console.log(`Status Setelah Cabut : ${statusAfterRevoke ? "VALID" : "TIDAK SAH / DIBATALKAN (FALSE)"}`);
  console.log(`Pesan Status Kontrak : ${msgAfterRevoke}`);
  console.log("");

  // B-07: Mekanisme Jeda Darurat
  console.log("[B-07 Mekanisme Jeda Darurat Circuit Breaker]");
  const pauseTx = await contract.connect(admin).pause();
  const pauseReceipt = await pauseTx.wait();
  console.log(`Admin Mengaktifkan Pause. Tx: ${pauseReceipt.hash} | Gas: ${pauseReceipt.gasUsed.toString()}`);
  console.log(`Status Kontrak Paused: ${await contract.paused()}`);

  try {
    await contract
      .connect(issuer)
      .issueBatch(ethers.encodeBytes32String("BATCH-DARURAT"), root, 5, "ipfs://test");
    console.log("Peringatan: Transaksi berhasil saat pause!");
  } catch (err) {
    console.log(`Hasil Pencegatan Pause: Transaksi Reverted (EnforcedPause)`);
    console.log(`Pesan Error           : ${err.message.split("(")[0].trim()}`);
  }

  const unpauseTx = await contract.connect(admin).unpause();
  await unpauseTx.wait();
  console.log(`Admin Mengaktifkan Unpause. Status Kontrak Paused: ${await contract.paused()}`);
  console.log("");
  console.log("Seluruh tahapan pengujian selesai.");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
