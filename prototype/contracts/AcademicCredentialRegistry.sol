// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/access/AccessControl.sol";
import "@openzeppelin/contracts/utils/Pausable.sol";
import "@openzeppelin/contracts/utils/cryptography/MerkleProof.sol";

/**
 * @title AcademicCredentialRegistry
 * @notice Registri Kredensial Akademik Konsorsium berbasis Merkle Tree dan Role-Based Access Control.
 * @dev Menerapkan prinsip Privacy-by-Design dan Kepatuhan UU PDP (Zero-PII On-Chain).
 *      Hanya jangkar integritas kriptografis (Merkle root batch wisuda) dan status pencabutan
 *      yang disimpan on-chain. Dokumen PII disimpan off-chain oleh pemegang (holder/mahasiswa).
 */
contract AcademicCredentialRegistry is AccessControl, Pausable {
    bytes32 public constant ISSUER_ROLE = keccak256("ISSUER_ROLE");
    bytes32 public constant REVOKER_ROLE = keccak256("REVOKER_ROLE");

    struct BatchRecord {
        bytes32 merkleRoot;
        uint256 issuanceTimestamp;
        uint256 graduateCount;
        string metadataURI;
        bool exists;
    }

    mapping(bytes32 => BatchRecord) public batches;
    mapping(bytes32 => bool) public isCredentialRevoked;

    event BatchIssued(
        bytes32 indexed batchId,
        bytes32 indexed merkleRoot,
        uint256 graduateCount,
        string metadataURI,
        address indexed issuer,
        uint256 timestamp
    );

    event CredentialRevoked(
        bytes32 indexed leafHash,
        bytes32 indexed batchId,
        string reason,
        address indexed revoker,
        uint256 timestamp
    );

    event RegistryPaused(address indexed account);
    event RegistryUnpaused(address indexed account);

    error BatchAlreadyExists(bytes32 batchId);
    error BatchNotFound(bytes32 batchId);
    error InvalidMerkleRoot();
    error InvalidGraduateCount();
    error CredentialAlreadyRevoked(bytes32 leafHash);

    /**
     * @notice Inisialisasi tata kelola multi-peran konsorsium pendidikan tinggi.
     * @param admin Alamat pengendali tata kelola (Governance Board / Multisig).
     * @param issuer Alamat berwenang menerbitkan root batch (Biro Akademik / BAK).
     * @param revoker Alamat berwenang melakukan pencabutan status kredensial (Komite Etik).
     */
    constructor(address admin, address issuer, address revoker) {
        require(admin != address(0), "Admin cannot be zero address");
        require(issuer != address(0), "Issuer cannot be zero address");
        require(revoker != address(0), "Revoker cannot be zero address");

        _grantRole(DEFAULT_ADMIN_ROLE, admin);
        _grantRole(ISSUER_ROLE, issuer);
        _grantRole(REVOKER_ROLE, revoker);
    }

    /**
     * @notice Menghentikan sementara operasi mutasi state saat kondisi darurat atau insiden keamanan.
     */
    function pause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _pause();
        emit RegistryPaused(msg.sender);
    }

    /**
     * @notice Mengaktifkan kembali operasi normal setelah investigasi dan mitigasi insiden tuntas.
     */
    function unpause() external onlyRole(DEFAULT_ADMIN_ROLE) {
        _unpause();
        emit RegistryUnpaused(msg.sender);
    }

    /**
     * @notice Menjangkarkan komitmen kriptografis akar pohon Merkle untuk satu batch periode wisuda.
     * @param batchId Pengenal unik periode batch wisuda (bytes32).
     * @param merkleRoot Akar pohon Merkle perangkum seluruh komitmen hash daun ijazah.
     * @param graduateCount Jumlah lulusan yang terdaftar pada batch terkait.
     * @param metadataURI Penunjuk ke skema metadata off-chain non-PII (misal IPFS URI).
     */
    function issueBatch(
        bytes32 batchId,
        bytes32 merkleRoot,
        uint256 graduateCount,
        string calldata metadataURI
    ) external onlyRole(ISSUER_ROLE) whenNotPaused {
        if (batches[batchId].exists) revert BatchAlreadyExists(batchId);
        if (merkleRoot == bytes32(0)) revert InvalidMerkleRoot();
        if (graduateCount == 0) revert InvalidGraduateCount();

        batches[batchId] = BatchRecord({
            merkleRoot: merkleRoot,
            issuanceTimestamp: block.timestamp,
            graduateCount: graduateCount,
            metadataURI: metadataURI,
            exists: true
        });

        emit BatchIssued(
            batchId,
            merkleRoot,
            graduateCount,
            metadataURI,
            msg.sender,
            block.timestamp
        );
    }

    /**
     * @notice Mencabut status keabsahan ijazah tertentu secara spesifik tanpa mengubah root batch.
     * @param leafHash Hash daun komitmen ijazah yang dicabut.
     * @param batchId Pengenal batch tempat ijazah terdaftar.
     * @param reason Alasan yuridis pencabutan status kredensial akademik.
     */
    function revokeCredential(
        bytes32 leafHash,
        bytes32 batchId,
        string calldata reason
    ) external onlyRole(REVOKER_ROLE) whenNotPaused {
        if (!batches[batchId].exists) revert BatchNotFound(batchId);
        if (isCredentialRevoked[leafHash]) revert CredentialAlreadyRevoked(leafHash);

        isCredentialRevoked[leafHash] = true;

        emit CredentialRevoked(
            leafHash,
            batchId,
            reason,
            msg.sender,
            block.timestamp
        );
    }

    /**
     * @notice Memverifikasi keabsahan kredensial akademik menggunakan bukti jalur Merkle.
     * @param batchId Pengenal batch wisuda.
     * @param leafHash Hash daun komitmen kredensial yang diajukan pemegang dokumen.
     * @param proof Rangkaian sibling hashes untuk merekonstruksi akar Merkle.
     * @return isValid Status keabsahan (true jika sah, false jika gagal/dicabut/palsu).
     * @return statusMessage Deskripsi status verifikasi teknis.
     */
    function verifyCredential(
        bytes32 batchId,
        bytes32 leafHash,
        bytes32[] calldata proof
    ) external view returns (bool isValid, string memory statusMessage) {
        if (!batches[batchId].exists) {
            return (false, "BATCH_NOT_FOUND");
        }

        if (isCredentialRevoked[leafHash]) {
            return (false, "CREDENTIAL_REVOKED");
        }

        bool validProof = MerkleProof.verify(proof, batches[batchId].merkleRoot, leafHash);
        if (!validProof) {
            return (false, "INVALID_PROOF_OR_TAMPERED");
        }

        return (true, "VALID");
    }
}
