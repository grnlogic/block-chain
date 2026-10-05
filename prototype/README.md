# Prototipe Sistem Registri Kredensial Akademik (AcademicCredentialRegistry)
**Mata Kuliah:** Blockchain (KP70067008) — Universitas Siliwangi  
**Penyusun:** Fajar Geran Arifin (NIM: 237006079) — Kelas C, S1 Informatika  
**Dosen Pengampu:** Dr. Ir. Nur Widiyasono, M.Kom.  

---

## 1. Deskripsi Umum
Repositori prototipe ini mengimplementasikan sistem penjangkaran dan verifikasi kredensial akademik (Ijazah, Transkrip, dan Sertifikat Kompetensi) berbasis **Merkle Tree**, **Salted Cryptographic Commitment**, dan **Role-Based Access Control (RBAC)**.

Sistem dirancang dengan arsitektur **Zero-PII On-Chain** untuk mematuhi **UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP)**:
- Tidak ada data pribadi (Nama, NIM, IPK, NIK) yang disimpan di blockchain guna menjamin hak penghapusan (*Right to Erasure*, Pasal 8 dan Pasal 43 UU PDP).
- Dokumen akademik lengkap disimpan off-chain oleh pemegang (*holder*) dalam format standar **W3C Verifiable Credentials (VC) Data Model v2.0**.
- Setiap klaim di-hash bersama nilai *salt* 256-bit berentropi tinggi untuk mencegah serangan kamus (*dictionary / rainbow table attacks*) pada data berentropi rendah.
- Hanya **Merkle Root** per batch wisuda dan status pencabutan individual yang disimpan pada *smart contract*.

---

## 2. Lingkungan dan Versi Perangkat Lunak
Pengujian dijalankan pada lingkungan deterministik:
- **Sistem Operasi:** Linux (Kernel 6.17.0-40-generic x86_64)
- **Node.js:** `v24.14.0`
- **npm:** `11.9.0`
- **Hardhat:** `2.29.1`
- **Solidity Compiler (`solc`):** `0.8.28` (EVM target: `paris`, optimizer: enabled, 200 runs)
- **Pustaka Smart Contract:** `@openzeppelin/contracts` `v5.6.1`
- **Pustaka Kriptografi Off-Chain:** `merkletreejs` `v0.6.0`, `keccak256` `v1.0.6`, `crypto` (Native Node.js)
- **Network ID / Chain ID:** Localhost / Hardhat Network (`31337`)

---

## 3. Struktur Direktori Prototipe
```text
prototype/
├── contracts/
│   └── AcademicCredentialRegistry.sol   # Smart contract utama (AccessControl, Pausable, MerkleProof)
├── scripts/
│   ├── lib/
│   │   └── crypto-utils.js              # Utilitas kanonikalisasi RFC 8785, salted hash, Merkle tree & proof
│   ├── run-demo.js                      # Skrip simulasi end-to-end lengkap (B-01 s.d. B-07)
│   └── perf-bench.js                    # Skrip automated benchmark 30 iterasi (B-08)
├── test/
│   └── AcademicCredentialRegistry.test.js # Test suite otomatis 8 pengujian (T-01 s.d. T-08)
├── results/
│   ├── test-output.txt                  # Log mentah eksekusi unit test (8 passing)
│   ├── demo-output.txt                  # Log mentah simulasi end-to-end (B-01 s.d. B-07)
│   └── perf-output.txt                  # Log mentah hasil benchmark 30 run (B-08)
├── .gitignore                           # Pengecualian node_modules/, artifacts/, cache/, dsb.
├── hardhat.config.js                    # Konfigurasi Hardhat (compiler solc 0.8.28, optimizer)
├── package.json                         # Manifes dependensi dan skrip npm (pipefail-protected)
├── package-lock.json                    # Lockfile dependensi npm
├── README.md                            # Dokumentasi, panduan reproduksi, dan kriteria penerimaan
└── SHA256SUMS.txt                       # Checksum integritas berkas prototipe
```

---

## 4. Panduan Langkah Reproduksi (Reproducibility Guide)

Untuk mereproduksi seluruh hasil pengujian secara deterministik dari awal:

### Langkah 1: Pindah ke Direktori Prototipe
```bash
cd "/home/fajar-geran-arifin/Documents/kuliah/block chain/prototype"
```

### Langkah 2: Instalasi Dependensi Lokal
*(Dependensi sudah terinstal di repositori lokal ini; perintah di bawah untuk mesin penguji baru)*
```bash
npm install
```

### Langkah 3: Kompilasi Smart Contract
```bash
npx hardhat compile
```
*Output yang diharapkan:* `Compiled 9 Solidity files successfully (evm target: paris).`

### Langkah 4: Menjalankan Seluruh Unit Test (T-01 s.d. T-08)
```bash
npm test
```
*Perintah di atas mengeksekusi `bash -o pipefail -c 'mkdir -p results && NO_COLOR=1 npx hardhat test | tee results/test-output.txt'`.*  
*Output yang diharapkan:* `8 passing (~670ms)`. Exit code non-nol diteruskan saat test gagal.

### Langkah 5: Menjalankan Simulasi Demo End-to-End (B-01 s.d. B-07)
```bash
npm run demo
```
*Perintah di atas mengeksekusi skrip end-to-end dan menyimpan log ke `results/demo-output.txt`.*

### Langkah 6: Menjalankan Pengujian Performa 30 Run (B-08)
```bash
npm run bench
```
*Perintah di atas mengeksekusi automated benchmark 30 iterasi terukur (+ 2 warm-up) pada batch $N \in \{6, 100, 1000\}$ dan menyimpan log ke `results/perf-output.txt`.*

---

## 5. Pemetaan Uji, Bukti Pelaksanaan, Skrip, dan Berkas Log Mentah

| ID Uji | ID Bukti | Deskripsi Skenario Uji | Skrip Pelaksana | Berkas Log Mentah |
| :---: | :---: | :--- | :--- | :--- |
| **T-01** | **B-03** | Penerbitan batch ijazah oleh akun berwenang ISSUER_ROLE | `test/AcademicCredentialRegistry.test.js`, `scripts/run-demo.js` | `results/test-output.txt`, `results/demo-output.txt` |
| **T-02** | **B-04** | Verifikasi kredensial sah menggunakan valid Merkle proof | `test/AcademicCredentialRegistry.test.js`, `scripts/run-demo.js` | `results/test-output.txt`, `results/demo-output.txt` |
| **T-03** | **B-05A** | Penolakan manipulasi klaim data IPK dan salt palsu | `test/AcademicCredentialRegistry.test.js`, `scripts/run-demo.js` | `results/test-output.txt`, `results/demo-output.txt` |
| **T-04** | **B-05B** | Pembatalan upaya penerbitan batch oleh pihak tanpa peran ISSUER_ROLE | `test/AcademicCredentialRegistry.test.js`, `scripts/run-demo.js` | `results/test-output.txt`, `results/demo-output.txt` |
| **T-05** | **B-06** | Pencabutan status keabsahan ijazah oleh REVOKER_ROLE secara spesifik | `test/AcademicCredentialRegistry.test.js`, `scripts/run-demo.js` | `results/test-output.txt`, `results/demo-output.txt` |
| **T-06** | — | Pembatalan upaya pencabutan ijazah oleh pihak tanpa peran REVOKER_ROLE | `test/AcademicCredentialRegistry.test.js` | `results/test-output.txt` |
| **T-07** | **B-07** | Penghentian mutasi state saat jeda darurat pause aktif dan pulih pasca-unpause | `test/AcademicCredentialRegistry.test.js`, `scripts/run-demo.js` | `results/test-output.txt`, `results/demo-output.txt` |
| **T-08** | **B-08** | Evaluasi efisiensi gas konstan O(1) dan panjang proof logaritmik O(log N) | `test/AcademicCredentialRegistry.test.js`, `scripts/perf-bench.js` | `results/test-output.txt`, `results/perf-output.txt` |
| — | **B-01** | Deployment smart contract ke node lokal Hardhat | `scripts/run-demo.js` | `results/demo-output.txt` |
| — | **B-02** | Pembangkitan kredensial salted hash dan Merkle tree off-chain | `scripts/run-demo.js` | `results/demo-output.txt` |

---

## 6. Rincian Komponen Gas Transaksi On-Chain `issueBatch`

Gas eksekusi kontrak dihitung secara ketat menggunakan definisi standar EVM:
$$\text{Gas Eksekusi Murni} = \text{gasUsed (Receipt)} - 21.000\text{ (Biaya Dasar Transaksi)} - \text{Biaya Calldata tx.data}$$
Biaya calldata dihitung langsung dari data transaksi aktual (`tx.data`) sesuai aturan **EIP-2028** (16 gas per byte non-nol, 4 gas per byte nol):

| Komponen Gas `issueBatch` | Batch $N = 6$ | Batch $N = 100$ | Batch $N = 1.000$ | Analisis & Justifikasi Karakteristik |
| :--- | :---: | :---: | :---: | :--- |
| **Total `gasUsed` (Receipt) (mean)** | 187.874 gas *(187.873,80)* | 187.922 gas *(187.922,20)* | 187.958 gas *(187.957,80)* | Total gas yang dipotong dari pengirim transaksi. |
| **- Biaya Dasar Transaksi (*Intrinsic*)** | 21.000 gas | 21.000 gas | 21.000 gas | Biaya standar pemrosesan transaksi EVM (konstan). |
| **- Biaya Calldata `tx.data` (EIP-2028)** | 1.963 gas *(1.962,80)* | 2.011 gas *(2.011,20)* | 2.047 gas *(2.046,80)* | Dihitung dari payload aktual (140,4 byte nol, 87,6 byte non-nol). |
| **= Gas Eksekusi Kontrak Murni** | **164.911 gas** | **164.911 gas** | **164.911 gas** | **Eksak Identik ($O(1)$)**: Logika smart contract konstan 100% pada seluruh skala. |
| **Deviasi Relatif Gas Eksekusi vs $N=6$** | **0,00%** *(Baseline)* | **0,0000%** | **0,0000%** | Membuktikan skalabilitas penjangkaran tanpa batas volume. |

---

## 7. Pembuktian dan Rincian Sumber Selisih Gas `issueBatch` (84 Gas)

Selisih biaya calldata sebesar **84 gas** antara batch $N=6$ dan $N=1.000$ telah dibuktikan secara analitis dan empiris **bukan berasal dari komputasi smart contract**, melainkan dari akumulasi 3 parameter calldata ABI transaksi:

| Parameter / Calldata Word | Biaya Calldata $N=6$ | Biaya Calldata $N=1000$ | Selisih Gas ($\Delta$) | Penjelasan Penyebab Perubahan Byte |
| :--- | :---: | :---: | :---: | :--- |
| **Word 0: `batchId` (bytes32)** | 296 gas | 332 gas | **+36 gas** | Penambahan 3 karakter ASCII (`"BATCH-1000"` vs `"BATCH-6"`) mengubah 3 byte nol menjadi byte non-nol ($3 \times 12\text{ gas} = 36$). |
| **Word 1: `merkleRoot` (bytes32)** | 512 gas | 512 gas | **0 gas** | Hash 32-byte acak (identik 32 byte non-nol pada kondisi baseline). |
| **Word 2: `graduateCount` (uint256)** | 140 gas | 152 gas | **+12 gas** | Nilai heksadesimal $N=1000$ (`0x03e8`) memuat 2 byte non-nol vs $N=6$ (`0x06`) 1 byte non-nol ($1 \times 12\text{ gas} = 12$). |
| **Word 3: `metadataURI` offset** | 140 gas | 140 gas | **0 gas** | Pointer offset statis `0x00...0080` (128 decimal). |
| **Word 4: `metadataURI` length** | 140 gas | 140 gas | **0 gas** | Panjang string (34 vs 37 karakter, sama-sama 1 byte non-nol). |
| **Word 5: `metadataURI` chunk 1** | 512 gas | 512 gas | **0 gas** | 32 byte karakter awal URL (seluruhnya non-nol). |
| **Word 6: `metadataURI` chunk 2** | 152 gas | 188 gas | **+36 gas** | Bagian akhir URL (`"1000.json"` vs `"6.json"`) memuat 3 karakter ekstra ($3 \times 12\text{ gas} = 36$). |
| **Total Akumulasi Selisih Calldata** | **1.963 gas** | **2.047 gas** | **+84 gas** | **$36 + 12 + 36 = \mathbf{84\text{ gas}}$ (Eksak 100%)** |

---

## 8. Model Regresi Linier Komputasi Verifikasi (`verifyCredential`)

> **Catatan Metodologis:**  
> Ambang batas anggaran (*budget*) komputasi verifikasi ini **diturunkan pasca-pengukuran (post-measurement)**, bukan merupakan hipotesis apriori yang ditetapkan sebelum pengujian.

Persamaan hasil regresi empiris dari 30 run pengukuran:
$$\text{pureVerifyGas}(k) = 7.800,04 + 251,26 \times k$$
di mana $k$ adalah jumlah sibling hash pada bukti Merkle ($k = \lceil \log_2 N \rceil$).

- **Biaya per Sibling Terukur:** Rata-rata terukur adalah $\approx 251,3$ gas/sibling, membuktikan pertumbuhan biaya yang proporsional terhadap panjang bukti Merkle $k = \lceil \log_2 N \rceil$ (konsisten dengan $O(\log N)$).
- **Catatan Koefisien Determinasi ($R^2$):** Nilai $R^2 = 1,0000$ diperoleh dari 3 titik data terukur ($k = 3, 7, 10$). Oleh karena itu, $R^2$ tidak disajikan sebagai bukti statistik yang kuat, melainkan sebagai konfirmasi atas sifat eksekusi deterministik EVM.
- **Kriteria Penerimaan / Ambang Anggaran (*Budget*):**  
  $$\text{pureVerifyGas}(k) \le 10.000 + (k \times 350)\text{ gas}$$
  Untuk $N = 1.000$ ($k = 10$ siblings), ambang anggaran adalah $\le 13.500$ gas. Hasil terukur nyata adalah **10.313 gas** (**LULUS**).

---

## 9. Tabel Kriteria Penerimaan (Acceptance Criteria) Terverifikasi

| Kelompok Uji | ID Uji | Kriteria Penerimaan (*Acceptance Criteria*) | Ambang Batas Teoretis | Justifikasi Ilmiah & Landasan Referensi | Hasil Nyata Pengujian | Status |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: |
| **Fungsional** | **T-01 / B-03** | **T-01: menerbitkan batch ijazah oleh akun berwenang ISSUER_ROLE** | Transaksi sukses (`status = 1`), `exists == true`. | **W3C VC Data Model v2.0, Bagian 4.10 (*Status*) [URL: https://www.w3.org/TR/vc-data-model-2.0/#status]:** Konsisten dengan mekanisme penemuan status kredensial (*credentialStatus*) untuk memeriksa keabsahan dokumen via rujukan status eksternal (W3C Recommendation, 15 Mei 2025). | Root terdaftar di Block #2; event `BatchIssued` terpancar sah. | **LULUS** |
| **Fungsional** | **T-02 / B-04** | **T-02: memverifikasi kredensial sah menggunakan valid Merkle proof** | `isValid == true`, status `"VALID"`, gas pemanggil $= 0$. | **Dokumentasi Resmi Ethereum JSON-RPC API, metode `eth_call` [URL: https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_call]:** Eksekusi pesan panggilan simulasi lokal pada node tanpa transaksi on-chain (*executes a new message call immediately without creating a transaction on the blockchain*), tidak memodifikasi status (*state*), dan bebas biaya gas bagi publik (*eth_call consumes zero gas*). | Mengembalikan `true`, status `"VALID"`, 0 gas verifikator publik. | **LULUS** |
| **Fungsional** | **T-05 / B-06** | **T-05: mencabut status keabsahan ijazah oleh REVOKER_ROLE secara spesifik** | Status verifikasi pasca-cabut berubah menjadi `false` (`CREDENTIAL_REVOKED`). | **Pembanding Desain vs W3C Bitstring Status List v1.0:** Berbeda dari pendekatan bitstring terkompresi off-chain (W3C Recommendation, 15 Mei 2025), prototipe mengadopsi pencabutan on-chain berbasis mapping hash (`mapping(bytes32 => bool)`) untuk status pembatalan deterministik $O(1)$ seketika di smart contract. | Status tercabut seketika; ijazah lain tetap valid. | **LULUS** |
| **Keamanan** | **T-03 / B-05A** | **T-03: menolak manipulasi klaim data IPK dan salt palsu** | `isValid == false`, pesan `INVALID_PROOF_OR_TAMPERED`. | **Konsisten dengan spesifikasi Keccak asli (Bertoni et al., 2011) dan NIST FIPS 202:** Resistensi benturan dan *pre-image* varian asli Keccak-256 (padding $10^*1$, berbeda dari FIPS 202 SHA3-256 ber-domain separator 0x06) menjamin daun termutasi menghasilkan hash berbeda sehingga gagal verifikasi root. | Ditolak seketika oleh verifikasi Merkle on-chain. | **LULUS** |
| **Keamanan** | **T-04, T-06 / B-05B** | **T-04: membatalkan upaya penerbitan batch oleh pihak tanpa peran ISSUER_ROLE** & **T-06: membatalkan upaya pencabutan ijazah oleh pihak tanpa peran REVOKER_ROLE** | *Revert* dengan `AccessControlUnauthorizedAccount`. | **Konsisten secara umum dengan prinsip *Least Privilege* (Saltzer & Schroeder, 1975, Bagian I.A.1.f):** Setiap entitas hanya diberikan hak akses minimum yang esensial, diimplementasikan secara terisolasi via pustaka OpenZeppelin Contracts v5 `AccessControl`. | Transaksi penyerang dibatalkan (*revert*) secara deterministik. | **LULUS** |
| **Keamanan** | **T-07 / B-07** | **T-07: menghentikan mutasi state saat jeda darurat pause aktif dan pulih pasca-unpause** | Penulisan *revert* dengan `EnforcedPause`; pemulihan via `unpause()`. | **Dokumentasi OpenZeppelin Contracts v5 Pausable & ConsenSys Circuit Breaker Pattern [URL: https://docs.openzeppelin.com/contracts/5.x/api/utils#Pausable]:** Menghentikan sementara seluruh mutasi state saat kunci privat diduga terkompromi atau terdeteksi anomali operasional. | Penulisan dicegat saat pause, normal pasca-unpause. | **LULUS** |
| **Performa** | **T-08 / B-08** | **T-08: mengevaluasi efisiensi gas konstan O(1) dan panjang proof logaritmik O(log N)** (Sub-aspek 1: Skalabilitas Gas) | Deviasi relatif gas eksekusi murni antar-skala $\le 1,0\%$; total gas $\le 1,0\%$ Block Gas Limit (30M gas). | **Konsep Kompresi Pohon Autentikasi (Merkle, U.S. Patent 4,309,569, 1982) & Pengukuran Empiris EVM:** Paten Merkle (1982) memformulasikan tree authentication dan kompresi $N$ daun menjadi satu root 32-byte. Klaim bahwa biaya penulisan penyimpanan konstan $O(1)$ (`SSTORE`) merupakan sifat teknis penyimpanan 32 byte di EVM dan hasil ukur prototipe (B-08); selisih gas transaksi riil terbukti murni berasal dari payload calldata ABI (EIP-2028). | Gas Eksekusi Murni $N=6$: 164.911 gas vs $N=1000$: 164.911 gas ($\Delta = 0\text{ gas} = 0,0000\%$). | **LULUS** |
| **Performa** | **T-08 / B-08** | **T-08: mengevaluasi efisiensi gas konstan O(1) dan panjang proof logaritmik O(log N)** (Sub-aspek 2: Batas Bukti Logaritmik) | Panjang proof $\le \lceil \log_2 N \rceil$ (3 untuk $N=6$, 7 untuk $N=100$, 10 untuk $N=1.000$). | **Sifat Struktural Pohon Biner Lengkap (*Complete Binary Tree*, Merkle 1982):** Pada pohon biner lengkap beranggotakan $N$ daun, jalur verifikasi (*audit path*) dari sembarang daun ke root secara matematis memiliki panjang tepat $k = \lceil \log_2 N \rceil$ simpul saudara (*sibling hashes*), meminimalkan ukuran transmisi data payload verifikasi. | Tepat 3, 7, dan 10 sibling hash (100% presisi matematis). | **LULUS** |
| **Performa** | **T-08 / B-08** | **T-08: mengevaluasi efisiensi gas konstan O(1) dan panjang proof logaritmik O(log N)** (Sub-aspek 3: Anggaran Komputasi Verifikasi) | Ambang anggaran (*budget*) turunan pengukuran: $\text{pureGas}(k) \le 10.000 + (k \times 350)$ gas ($\le 13.500$ gas untuk $k=10$). | **Model Anggaran Linier Pasca-Pengukuran:** Pertumbuhan terukur $\approx 251,3$ gas/sibling konsisten dengan $O(\log N)$ dan perkiraan analitis biaya opcode loop `MerkleProof.verify` (KECCAK256 42 gas, MLOAD/MSTORE 6 gas, stack/jump ~200 gas; catatan: rincian opcode adalah perkiraan analitis, bukan profil langsung). | 8.554 gas ($N=6$) hingga 10.313 gas ($N=1000$). | **LULUS** |
| **Performa** | **T-08 / B-08** | **T-08: mengevaluasi efisiensi gas konstan O(1) dan panjang proof logaritmik O(log N)** (Sub-aspek 4: Responsivitas Sub-detik) | Durasi rata-rata $< 1.000$ ms pada perangkat keras standar. | **Konsisten dengan pedoman batas responsivitas interaksi manusia-komputer (Nielsen, 1993, "Response Times: The 3 Important Limits", Nielsen Norman Group):** Eksekusi komputasi sub-detik (< 1.000 ms) menjaga alur kognitif pengguna tetap terjaga tanpa distraksi jeda antarmuka. | Rata-rata 129,44 ms (rentang 121,10 – 146,35 ms). | **LULUS** |

---

## 10. Indeks Bukti Eksekusi Nyata (B-01 s.d. B-08)

1. **B-01 (Deployment Kontrak):**
   - Alamat Kontrak: `0x5FbDB2315678afecb367f032d93F642f64180aa3`
   - Tx Hash: `0x145b5523b5eeb4fd842f56a495a3e9bf17267ea22d4c48a416d08a142f384498`
   - Konsumsi Gas: `1.039.368` unit
   - Status: Sukses; RBAC terinisialisasi untuk Admin, Issuer, dan Revoker (`results/demo-output.txt`).
2. **B-02 (Pembangkitan Kredensial & Merkle Tree):**
   - 6 Lulusan sintetis diproses dengan salt 256-bit unik CSPRNG.
   - Merkle Root terhitung: `0x46ca2e8399d6be8a489c375dcd355319d7eaa4a92a132afdc3a00220c1faccd3`.
   - Daun L1 (G-01): `0x7b5f7365dffd18a87fb7b5471e7843da27e53b4ec53e8e1ef064b78ab3b0645c`.
   - Daun L2 (G-02): `0xf3695a1ce4a97902b58bf9bb868bac471c484bcedec9edfbb1a8290fa86a1575`.
3. **B-03 (Penjangkaran Root On-Chain):**
   - Batch ID: `WISUDA-2026-PERIODE-1`
   - Tx Hash: `0x1737c3595a7ffab660d99cb81bd14dc04b8c21f9fb399ad5b2aa454998a88321`
   - Konsumsi Gas: `211.084` unit
   - Status: Terdaftar di Block #2 (`results/demo-output.txt`).
4. **B-04 (Verifikasi Kredensial Sah):**
   - Mahasiswa: Ahmad Dahlan Al-Faruq (NIM: 237006801)
   - Leaf: `0x7b5f7365dffd18a87fb7b5471e7843da27e53b4ec53e8e1ef064b78ab3b0645c`
   - Panjang Bukti Merkle: 3 sibling hash
   - **Biaya Gas Pemverifikasi Publik:** `0 gas` (dipanggil via `eth_call` query off-chain, bebas biaya bagi masyarakat/HRD).
   - **Raw estimateGas Simulasi Transaksi:** `32.309 unit` (simulasi transaksi mencakup 21.000 gas dasar).
   - **Biaya Intrinsik Calldata (EIP-2028):** `2.772 gas`.
   - **Estimasi Gas Eksekusi Murni EVM:** `8.537 unit` (komputasi murni loop `MerkleProof.verify`).
   - Hasil Kontrak: `isValid = true`, `statusMessage = "VALID"`.
5. **B-05 (Uji Ketahanan Tampering & RBAC):**
   - 5A (Tamper IPK): Nilai daun termutasi `0x0b097c59bcd2b3d0b5cba350b03cea87b34b4294eba79c5d5cf2f0a548d04f97` ditolak dengan pesan `INVALID_PROOF_OR_TAMPERED`.
   - 5B (Attacker RBAC): Upaya penyerang dibatalkan dengan eksepsi `AccessControlUnauthorizedAccount`.
6. **B-06 (Pencabutan Kredensial):**
   - Mahasiswa Dicabut: Bunga Citra Lestari Fiktif (NIM: 237006802)
   - Tx Hash: `0xb46a5c18e00d340e376fe0188895f25610daa04eb1f1d72f3ed05cc6b5642ab4`
   - Konsumsi Gas: `56.359` unit
   - Hasil Kontrak: `isValid = false`, `statusMessage = "CREDENTIAL_REVOKED"`.
7. **B-07 (Audit Jeda Darurat):**
   - Admin mengaktifkan pause: Tx `0xd254074356083b2825edb43243c001de2430bf82be45f8757c40ecc8b5965648` (Gas: `48.214` unit).
   - Upaya penerbitan oleh issuer dibatalkan dengan error `EnforcedPause`.
   - Pemulihan normal via `unpause()`.
8. **B-08 (Benchmark Skalabilitas & Performa Batch 6, 100, 1000):**
   - Sumber: `prototype/scripts/perf-bench.js` (Hardhat Local EVM Chain ID 31337, berkas `results/perf-output.txt`).
   - Sampel: **30 iterasi terukur + 2 iterasi warm-up** per batch size.
   - Rekapitulasi Data Nyata (Mean | Median | SD | [Min - Max]):
     - **Waktu Build Tree Off-Chain (ms):**
       - $N = 6$: 1.43 ms | 1.31 ms | 0.43 | [0.87 - 2.48]
       - $N = 100$: 14.01 ms | 13.01 ms | 2.92 | [11.29 - 26.39]
       - $N = 1.000$: 129.44 ms | 128.35 ms | 6.49 | [121.10 - 146.35]
     - **Panjang Bukti Merkle (Siblings):**
       - $N = 6$: 3 siblings (SD: 0) [3 - 3]
       - $N = 100$: 7 siblings (SD: 0) [7 - 7]
       - $N = 1.000$: 10 siblings (SD: 0) [10 - 10]
     - **Gas Transaksi `issueBatch` (Total):**
       - $N = 6$: 187.874 gas (med: 187.879, SD: 8) [187.855 - 187.879]
       - $N = 100$: 187.922 gas (med: 187.927, SD: 6) [187.915 - 187.927]
       - $N = 1.000$: 187.958 gas (med: 187.963, SD: 6) [187.951 - 187.963]
     - **Gas Eksekusi Murni `issueBatch`:**
       - $N = 6$: **164.911 gas** (med: 164.911, SD: 0) [164.911 - 164.911]
       - $N = 100$: **164.911 gas** (med: 164.911, SD: 0) [164.911 - 164.911]
       - $N = 1.000$: **164.911 gas** (med: 164.911, SD: 0) [164.911 - 164.911]
       - *Deviasi Relatif Antar-Skala:* **0,0000% (Konstan $O(1)$)**.
     - **Gas Transaksi `revokeCredential` (On-Chain):**
       - $N = 6$: 55.303 gas (med: 55.309, SD: 7) [55.285 - 55.309]
       - $N = 100$: 55.328 gas (med: 55.333, SD: 6) [55.321 - 55.333]
       - $N = 1.000$: 55.340 gas (med: 55.345, SD: 7) [55.321 - 55.345]
     - **Raw `estimateGas` `verifyCredential`:**
       - $N = 6$: 32.242 gas (med: 32.245, SD: 13) [32.211 - 32.267]
       - $N = 100$: 35.311 gas (med: 35.315, SD: 20) [35.269 - 35.347]
       - $N = 1.000$: 37.611 gas (med: 37.612, SD: 25) [37.566 - 37.666]
     - **Biaya Intrinsik Calldata Bukti (EIP-2028):**
       - $N = 6$: 2.687 gas | $N = 100$: 4.753 gas | $N = 1.000$: 6.298 gas
     - **Estimasi Gas Eksekusi Murni EVM `verifyCredential`:**
       - $N = 6$: 8.554 gas (med: 8.557, SD: 8) [8.537 - 8.567]
       - $N = 100$: 9.558 gas (med: 9.555, SD: 13) [9.535 - 9.585]
       - $N = 1.000$: 10.313 gas (med: 10.316, SD: 17) [10.266 - 10.346]
       - *Model Linier Terukur:* $\text{pureGas}(k) = 7.800,04 + 251,26 \times k$, $R^2 = 1,0000$.
     - **Biaya Verifikasi bagi Pemverifikasi / Publik:** `0 gas` (*free read call* via `eth_call`).
     - **Latensi Kueri Verifikasi Off-Chain:** 0.82 – 0.89 ms.

---

## 11. Keterbatasan Pengujian (Testing Limitations)

Laporan ini secara jujur menguraikan batasan-batasan teknis dari lingkungan pengujian yang dilaksanakan:
1. **Lingkungan In-Process Single Node:**  
   Pengujian benchmark dijalankan pada node lokal Hardhat in-process (`chainId: 31337`). Pengujian ini tidak mencakup latensi jaringan fisik (*round-trip network latency*), jitter paket internet, serta latensi konsensus antar-node multi-validator (seperti voting ronde QBFT pada Hyperledger Besu multi-node).
2. **Data Sintetis Fiktif:**  
   Seluruh data lulusan ($N=6$, $N=100$, $N=1.000$) adalah 100% data simulasi sintetis guna menjamin tidak adanya data pribadi riil yang bocor. Karakteristik entropi data diuji menggunakan kombinasi salt acak 256-bit standar industri.
3. **Karakteristik Mesin Uji Tunggal:**  
   Benchmark dijalankan pada satu workstation pengembang dengan spesifikasi:  
   - Prosesor: Intel Core i5-12450H (12 vCPU / 8 cores, frekuensi basis 2.0 GHz, turboboost up to 4.4 GHz)  
   - Memori: 16 GB DDR4 RAM  
   - Sistem Operasi: Ubuntu Linux 24.04 LTS (Kernel 6.17 x86_64)  
   Variasi perangkat keras dapat mempengaruhi angka durasi waktu build off-chain (*wall-clock time*), meskipun konsumsi gas EVM dijamin deterministik 100% di semua mesin.
4. **Hakikat `estimateGas`:**  
   Nilai `estimateGas` pada fungsi verifikasi adalah hasil estimasi eksekusi dry-run internal EVM yang mencakup 21.000 gas transaksi dan biaya calldata. Nilai ini bukan merupakan gas aktual yang dipotong dari saldo dompet pemverifikasi, karena pada arsitektur produksi fungsi verifikasi dipanggil tanpa biaya gas melalui metode `eth_call`.
