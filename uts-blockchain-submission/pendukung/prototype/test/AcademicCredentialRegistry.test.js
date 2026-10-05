const { expect } = require("chai");
const { ethers } = require("hardhat");
const {
  generateSalt,
  computeCredentialLeaf,
  buildCredentialMerkleTree,
  getMerkleProof,
} = require("../scripts/lib/crypto-utils");

describe("AcademicCredentialRegistry Test Suite", function () {
  let registry;
  let admin, issuer, revoker, student, verifier, attacker;
  let simulatedGraduates;
  let credentialLeaves;
  let merkleTree, merkleRoot;
  const batchId = ethers.encodeBytes32String("WISUDA-2026-PERIODE-1");
  const metadataURI = "ipfs://bafybeigdyrzt5sfp7udm7hu76uh7y26nf3efuylqabf3oclgtqy55fbzdi/metadata.json";

  before(async function () {
    [admin, issuer, revoker, student, verifier, attacker] = await ethers.getSigners();

    simulatedGraduates = [
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

    credentialLeaves = simulatedGraduates.map((grad) => {
      const salt = generateSalt();
      const leafData = computeCredentialLeaf(grad, salt);
      return {
        graduate: grad,
        salt: salt,
        leafHash: leafData.leafHash,
        claimHash: leafData.claimHash,
      };
    });

    const leafHashes = credentialLeaves.map((item) => item.leafHash);
    const treeData = buildCredentialMerkleTree(leafHashes);
    merkleTree = treeData.tree;
    merkleRoot = treeData.root;
  });

  beforeEach(async function () {
    const Factory = await ethers.getContractFactory("AcademicCredentialRegistry");
    registry = await Factory.deploy(admin.address, issuer.address, revoker.address);
    await registry.waitForDeployment();
  });
  it("T-01: menerbitkan batch ijazah oleh akun berwenang ISSUER_ROLE", async function () {
    const tx = await registry
      .connect(issuer)
      .issueBatch(batchId, merkleRoot, credentialLeaves.length, metadataURI);
    const receipt = await tx.wait();

    await expect(tx)
      .to.emit(registry, "BatchIssued")
      .withArgs(
        batchId,
        merkleRoot,
        credentialLeaves.length,
        metadataURI,
        issuer.address,
        (await ethers.provider.getBlock(receipt.blockNumber)).timestamp
      );

    const batchData = await registry.batches(batchId);
    expect(batchData.exists).to.be.true;
    expect(batchData.merkleRoot).to.equal(merkleRoot);
    expect(batchData.graduateCount).to.equal(credentialLeaves.length);
    expect(batchData.metadataURI).to.equal(metadataURI);
  });

  it("T-02: memverifikasi kredensial sah menggunakan valid Merkle proof", async function () {
    await registry
      .connect(issuer)
      .issueBatch(batchId, merkleRoot, credentialLeaves.length, metadataURI);

    const target = credentialLeaves[0];
    const proof = getMerkleProof(merkleTree, target.leafHash);

    const [isValid, statusMessage] = await registry
      .connect(verifier)
      .verifyCredential(batchId, target.leafHash, proof);

    expect(isValid).to.be.true;
    expect(statusMessage).to.equal("VALID");
  });

  it("T-03: menolak manipulasi klaim data IPK dan salt palsu", async function () {
    await registry
      .connect(issuer)
      .issueBatch(batchId, merkleRoot, credentialLeaves.length, metadataURI);

    const original = credentialLeaves[0];
    const proof = getMerkleProof(merkleTree, original.leafHash);

    const tamperedGrad = { ...original.graduate, ipk: "4.00" };
    const tamperedLeafData = computeCredentialLeaf(tamperedGrad, original.salt);

    const [isValid1, statusMessage1] = await registry
      .connect(verifier)
      .verifyCredential(batchId, tamperedLeafData.leafHash, proof);

    expect(isValid1).to.be.false;
    expect(statusMessage1).to.equal("INVALID_PROOF_OR_TAMPERED");

    const fakeSalt = generateSalt();
    const tamperedSaltData = computeCredentialLeaf(original.graduate, fakeSalt);

    const [isValid2, statusMessage2] = await registry
      .connect(verifier)
      .verifyCredential(batchId, tamperedSaltData.leafHash, proof);

    expect(isValid2).to.be.false;
    expect(statusMessage2).to.equal("INVALID_PROOF_OR_TAMPERED");
  });

  it("T-04: membatalkan upaya penerbitan batch oleh pihak tanpa peran ISSUER_ROLE", async function () {
    const issuerRole = await registry.ISSUER_ROLE();
    await expect(
      registry
        .connect(attacker)
        .issueBatch(batchId, merkleRoot, credentialLeaves.length, metadataURI)
    )
      .to.be.revertedWithCustomError(registry, "AccessControlUnauthorizedAccount")
      .withArgs(attacker.address, issuerRole);
  });

  it("T-05: mencabut status keabsahan ijazah oleh REVOKER_ROLE secara spesifik", async function () {
    await registry
      .connect(issuer)
      .issueBatch(batchId, merkleRoot, credentialLeaves.length, metadataURI);

    const target = credentialLeaves[1];
    const proof = getMerkleProof(merkleTree, target.leafHash);

    const [isValidBefore] = await registry.verifyCredential(batchId, target.leafHash, proof);
    expect(isValidBefore).to.be.true;

    const reason = "Terbukti pemalsuan dokumen prasyarat yudisium pada sidang etik";
    const revokeTx = await registry
      .connect(revoker)
      .revokeCredential(target.leafHash, batchId, reason);

    await expect(revokeTx)
      .to.emit(registry, "CredentialRevoked")
      .withArgs(
        target.leafHash,
        batchId,
        reason,
        revoker.address,
        (await ethers.provider.getBlock(await ethers.provider.getBlockNumber())).timestamp
      );

    const [isValidAfter, statusMessageAfter] = await registry
      .connect(verifier)
      .verifyCredential(batchId, target.leafHash, proof);

    expect(isValidAfter).to.be.false;
    expect(statusMessageAfter).to.equal("CREDENTIAL_REVOKED");
    expect(await registry.isCredentialRevoked(target.leafHash)).to.be.true;
  });

  it("T-06: membatalkan upaya pencabutan ijazah oleh pihak tanpa peran REVOKER_ROLE", async function () {
    await registry
      .connect(issuer)
      .issueBatch(batchId, merkleRoot, credentialLeaves.length, metadataURI);

    const target = credentialLeaves[0];
    const revokerRole = await registry.REVOKER_ROLE();

    await expect(
      registry
        .connect(attacker)
        .revokeCredential(target.leafHash, batchId, "Mencoba mencabut tanpa hak")
    )
      .to.be.revertedWithCustomError(registry, "AccessControlUnauthorizedAccount")
      .withArgs(attacker.address, revokerRole);
  });

  it("T-07: menghentikan mutasi state saat jeda darurat pause aktif dan pulih pasca-unpause", async function () {
    await expect(registry.connect(admin).pause())
      .to.emit(registry, "RegistryPaused")
      .withArgs(admin.address);

    expect(await registry.paused()).to.be.true;

    await expect(
      registry
        .connect(issuer)
        .issueBatch(batchId, merkleRoot, credentialLeaves.length, metadataURI)
    ).to.be.revertedWithCustomError(registry, "EnforcedPause");

    await expect(registry.connect(admin).unpause())
      .to.emit(registry, "RegistryUnpaused")
      .withArgs(admin.address);

    expect(await registry.paused()).to.be.false;

    await expect(
      registry
        .connect(issuer)
        .issueBatch(batchId, merkleRoot, credentialLeaves.length, metadataURI)
    ).to.emit(registry, "BatchIssued");
  });

  it("T-08: mengevaluasi efisiensi gas konstan O(1) dan panjang proof logaritmik O(log N)", async function () {
    const batchSizes = [100, 1000];
    for (const size of batchSizes) {
      const rawGraduates = [];
      for (let i = 1; i <= size; i++) {
        rawGraduates.push({
          nim: (237006000 + i).toString(),
          nama: `Mhs Fiktif ${i}`,
          ipk: "3.75",
        });
      }
      const records = rawGraduates.map((graduate) => {
        const salt = generateSalt();
        const leaf = computeCredentialLeaf(graduate, salt);
        return leaf.leafHash;
      });
      const { tree, root } = buildCredentialMerkleTree(records);
      const testBatchId = ethers.encodeBytes32String(`BATCH-${size}`);

      const tx = await registry
        .connect(issuer)
        .issueBatch(testBatchId, root, size, `ipfs://metadata-${size}`);
      const receipt = await tx.wait();

      expect(receipt.gasUsed).to.be.lessThan(250000n);

      const targetLeaf = records[0];
      const proof = getMerkleProof(tree, targetLeaf);
      const expectedMaxProofLen = Math.ceil(Math.log2(size));
      expect(proof.length).to.be.at.most(expectedMaxProofLen);

      const rawGasEst = await registry.verifyCredential.estimateGas(
        testBatchId,
        targetLeaf,
        proof
      );
      expect(rawGasEst).to.be.lessThan(40000n);

      const encodedCalldata = registry.interface.encodeFunctionData("verifyCredential", [
        testBatchId,
        targetLeaf,
        proof,
      ]);
      const bytesCd = ethers.getBytes(encodedCalldata);
      let cdCost = 0;
      for (const b of bytesCd) cdCost += b === 0 ? 4 : 16;
      const pureGas = Number(rawGasEst) - 21000 - cdCost;
      const maxExpectedPureGas = 10000 + expectedMaxProofLen * 350;
      expect(pureGas).to.be.lessThan(maxExpectedPureGas);

      const [isValid, statusMessage] = await registry.verifyCredential(
        testBatchId,
        targetLeaf,
        proof
      );
      expect(isValid).to.be.true;
      expect(statusMessage).to.equal("VALID");
    }
  });
});
