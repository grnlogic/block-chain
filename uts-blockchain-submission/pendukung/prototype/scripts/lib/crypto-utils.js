const crypto = require("crypto");
const { MerkleTree } = require("merkletreejs");
const keccak256 = require("keccak256");
const { ethers } = require("hardhat");

/**
 * Utilitas kriptografis untuk penjangkaran dan verifikasi kredensial akademik W3C VC.
 */

// Membangkitkan salt acak 256-bit (32 bytes) dari CSPRNG untuk mencegah serangan kamus pada atribut berentropi rendah.
function generateSalt() {
  return "0x" + crypto.randomBytes(32).toString("hex");
}

// Kanonikalisasi JSON deterministik berbasis pengurutan kunci leksikografis UTF-16 (mengacu pada RFC 8785).
function canonicalizeJson(targetValue) {
  if (targetValue === null || typeof targetValue !== "object") {
    return JSON.stringify(targetValue);
  }
  if (Array.isArray(targetValue)) {
    return "[" + targetValue.map(canonicalizeJson).join(",") + "]";
  }
  const propertyKeys = Object.keys(targetValue).sort();
  const serializedEntries = propertyKeys.map(
    (key) => `${JSON.stringify(key)}:${canonicalizeJson(targetValue[key])}`
  );
  return "{" + serializedEntries.join(",") + "}";
}

// Menghitung komitmen daun bergaram: keccak256(keccak256(canonicalClaims) || salt)
function computeCredentialLeaf(credentialClaims, salt) {
  const canonicalClaim = canonicalizeJson(credentialClaims);
  const claimHash = ethers.keccak256(ethers.toUtf8Bytes(canonicalClaim));
  const leafHash = ethers.solidityPackedKeccak256(
    ["bytes32", "bytes32"],
    [claimHash, salt]
  );
  return {
    canonicalClaim,
    claimHash,
    salt,
    leafHash,
  };
}

// Membangun pohon Merkle dari daftar leaf hashes.
// Opsi sortPairs: true wajib digunakan agar cocok dengan logika komparasi internal OpenZeppelin MerkleProof.sol.
function buildCredentialMerkleTree(leafHashes) {
  const tree = new MerkleTree(leafHashes, keccak256, { sortPairs: true });
  const root = "0x" + tree.getRoot().toString("hex");
  return { tree, root };
}

// Mengambil jalur pembuktian (Merkle audit proof) dalam format heksadesimal untuk daun tertentu.
function getMerkleProof(tree, leafHash) {
  return tree.getHexProof(leafHash);
}

module.exports = {
  generateSalt,
  canonicalizeJson,
  computeCredentialLeaf,
  buildCredentialMerkleTree,
  getMerkleProof,
};
