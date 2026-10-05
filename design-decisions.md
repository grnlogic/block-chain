# DOKUMEN KEPUTUSAN DESAIN ARSITEKTUR (DESIGN DECISIONS)
## Rancangan Sistem Verifikasi Kredensial Akademik Berbasis Konsorsium Blockchain
**Mata Kuliah:** Blockchain (KP70067008) — Semester 7 / TA 2026/2027  
**Penyusun:** Fajar Geran Arifin (NIM: 237006079) — Kelas C, S1 Informatika, Universitas Siliwangi  
**Dosen Pengampu:** Dr. Ir. Nur Widiyasono, M.Kom.  

---

## 1. Ringkasan Eksekutif & Konteks Desain
Dokumen ini menetapkan keputusan arsitektural, spesifikasi kriptografis, model tata kelola, dan strategi mitigasi risiko untuk **Sistem Verifikasi Kredensial Akademik (Ijazah, Transkrip, dan Sertifikat Kompetensi)**. Rancangan ini disusun untuk memenuhi rubrik asesmen OBE Bagian B (P1–P6) pada Naskah UTS Blockchain dengan mengadopsi format *Template Laporan Kegiatan Blockchain 2026/2027*.

Sistem dirancang dengan paradigma **Privacy-by-Design** dan **Sovereign-Identity-Aligned**:
1. Menjamin integritas dan non-repudiasi penerbitan dokumen akademik antar-institusi.
2. Mematuhi **Undang-Undang Perlindungan Data Pribadi (UU No. 27 Tahun 2022 / PDP)** dengan memastikan nol data pribadi (PII) tersimpan secara permanen di buku besar terdistribusi (*zero on-chain PII*).
3. Mengadopsi standar internasional **W3C Verifiable Credentials (VC) Data Model v2.0**, **W3C Decentralized Identifiers (DID) v1.0**, dan **1EdTech Open Badges v3.0**.
4. Memisahkan secara tegas antara **lingkungan desain target produksi enterprise** (Hyperledger Besu QBFT) dan **lingkungan prototipe eksekusi laboratorium** (Local EVM Hardhat).

---

## 2. Pemetaan Komponen Rubrik (Naskah P1–P6) ke Struktur Laporan (Template)

Sesuai hasil eksplorasi Fase 0, Bagian 4 pada template yang semula memuat latihan umum ("Case 1–5") dipetakan secara terpadu ke dalam use case Kredensial Akademik Universitas Siliwangi sebagai berikut:

| Bagian Template | Komponen Naskah | Isi & Fokus Utama | Tabel Acuan Template |
| :--- | :---: | :--- | :--- |
| **Identitas & Ringkasan** | Abstrak | Ringkasan eksekutif, masalah, metodologi konsorsium, hasil pengujian, limitasi. | Tabel 0 (Identitas) |
| **1. Pendahuluan** | **P1** | Latar belakang pemalsuan ijazah, pemangku kepentingan, evaluasi proses manual saat ini, keuntungan terukur, serta analisis kritis kapan basis data konvensional lebih tepat dibanding blockchain. | — |
| **2. Data, Alat, & Reproduksibilitas** | Reproduksibilitas | Spesifikasi lingkungan (Node v24, Hardhat, solc 0.8.28), struktur repositori, dan panduan deterministik replikasi pengujian. | Tabel 1 (Lingkungan & Alat) |
| **3. Catatan Pelaksanaan** | Log Bukti | Matriks kronologis pelaksanaan prototipe dan indeks rujukan bukti B-01 s.d. B-07. | Tabel 2 (Log Bukti B-xx) |
| **4.1 Kelayakan & Arsitektur Jaringan** | **P2** | Arsitektur jaringan konsorsium permissioned, peran node (validator vs observer), tata kelola onboarding, hak akses, model governance konsorsium, dan **Diagram Arsitektur Tingkat Tinggi**. | Tabel 3 (DB vs Blockchain) |
| **4.2 Kriptografi, Model Data, & Privasi** | **P3** | Model data W3C VC, skema hashing bergaram (*salted SHA-256*), mitigasi entropi rendah, struktur Merkle tree batch wisuda, pembagian on-chain vs off-chain, dan pemenuhan hak hapus UU PDP. | Tabel 4 (Record Merkle Batch) |
| **4.3 Konsensus, Platform, & Alur Transaksi** | **P2 & P3** | Evaluasi komparatif PoW vs PoS vs PBFT/PoA, pemilihan QBFT/PoA, evaluasi Account Model vs UTXO, siklus transaksi, dan **Diagram Alur Transaksi End-to-End**. | Tabel 5 (Konsensus) & Tabel 7 (Field Transaksi EVM) |
| **4.4 Keamanan, Privasi, & Manajemen Risiko** | **P4** | STRIDE Threat Model ($\ge 5$ ancaman teridentifikasi), **Matriks Ancaman & Mitigasi**, manajemen kunci multisig/threshold issuer, pemulihan kunci lulusan, audit logging, dan SOP penanganan insiden 24 jam. | Tabel 10 diadaptasi (Matriks Mitigasi) |
| **4.5 Implementasi Prototipe & Pengujian** | **P5** | Smart contract `AcademicCredentialRegistry.sol`, OpenZeppelin AccessControl, batch issuance Merkle root, revocation bitmap/mapping, test matrix T-01 s.d. T-07, evaluasi gas, dan bukti uji eksekusi nyata. | Tabel 9 diadaptasi (Matriks Uji T-xx) |
| **4.6 Keputusan Desain, Batasan, & Refleksi** | **P6** | Rekapitulasi trade-off arsitektural, keterbatasan prototipe lokal, evaluasi risiko etika & kesenjangan digital (*digital divide*), roadmap produksi, serta refleksi individual penulis. | — |
| **5. Bagian Khusus UAS** | — | **DIHAPUS** seluruhnya sesuai instruksi template. | — |
| **6. Kesimpulan, Pustaka, & Lampiran** | Luaran Akhir | Kesimpulan pencapaian, $\ge 5$ referensi standar resmi, Lampiran A (Pernyataan Orisinalitas bertanda tangan), Lampiran B (Transparansi penggunaan AI Claude & Antigravity). | Tabel Orisinalitas |

---

## 3. Keputusan Desain P1: Rumusan Masalah, Stakeholder, dan Batas Kelayakan

### 3.1 Masalah Utama Sistem Saat Ini
1. **Pemalsuan Fisik & Digital Rendah Biaya:** Penggunaan ijazah palsu atau hasil manipulasi perangkat lunak grafis sulit dibedakan oleh verifikator pihak ketiga tanpa verifikasi silang langsung ke kampus penerbit.
2. **Latensi Verifikasi Konvensional Tinggi:** Proses verifikasi manual/legalisir memerlukan waktu 3–14 hari kerja melalui pos, email birokrasi, atau kunjungan fisik.
3. **Ketergantungan Ekstrem pada Single Point of Failure (SPoF):** Pangkalan data terpusat kampus rawan terhadap serangan siber (*ransomware*, kebocoran data), insiden bencana fisik server, atau manipulasi oleh oknum orang dalam (*malicious insider / database administrator*).
4. **Pelanggaran Privasi Berlebih (*Over-disclosure*):** Verifikator lapangan sering kali meminta salinan lengkap ijazah dan transkrip akademik resmi meskipun yang dibutuhkan hanya pembuktian bahwa pelamar memiliki predikat kelulusan tertentu, mengekspos data pribadi non-relevan (alamat, tanggal lahir, riwayat nilai mata kuliah lain).

### 3.2 Pemangku Kepentingan (Stakeholders)
1. **Penerbit Kredensial (Issuer):** Universitas Siliwangi (Biro Akademik dan Kemahasiswaan - BAK, Dekanat, Rektorat). Bertanggung jawab atas validasi yuridis data akademik dan penerbitan komitmen kriptografis ke blockchain.
2. **Pemilik Kredensial (Holder / Subject):** Mahasiswa dan Lulusan. Menyimpan dokumen kredensial digital di dompet pribadi (*edge/mobile wallet*), mengendalikan hak akses, dan menghasilkan pembuktian kriptografis (*verifiable presentation*).
3. **Pihak Pemverifikasi (Verifier / Relying Party):** Industri, instansi pemerintah, BUMN, institusi pendidikan lanjutan. Memverifikasi keabsahan dokumen dalam hitungan detik tanpa perantara birokrasi.
4. **Otoritas Pengawas / Regulator (Governance Authority):** Kementerian Pendidikan Tinggi, Sains, dan Teknologi / LLDIKTI Wilayah IV. Bertindak sebagai validator penjamin standar nasional, pengawas tata kelola, dan resolusi sengketa.

### 3.3 Analisis Kritis: Kapan Basis Data Konvensional Lebih Tepat?
Penerapan blockchain bukan solusi universal. Berdasarkan kerangka keputusan *Birch-Brown-Parulian* dan prinsip kelayakan sistem terdistribusi, **basis data relasional konvensional (RDBMS/PostgreSQL) jauh lebih tepat apabila:**
1. **Model Kepercayaan Terpusat Penuh (*Single Trust Domain*):** Jika seluruh proses penerbitan, pengelolaan, dan validasi hanya berada di bawah kendali tunggal satu instansi tertutup tanpa kebutuhan validasi lintas batas institusi independen.
2. **Kebutuhan Throughput Sangat Tinggi dan Latensi Sub-detik:** Jika sistem menuntut jutaan transaksi pembaruan per detik dengan latensi baca-tulis $< 10$ milidetik (misalnya log kehadiran harian kelas).
3. **Data Dinamis yang Kerap Mengalami Mutasi (*High-frequency Updates / Deletions*):** Jika objek data terus-menerus diubah statusnya setiap jam. Blockchain bersifat *append-only*; data dinamis yang sering berubah menyebabkan inefisiensi penyimpanan buku besar.
4. **Biaya Infrastruktur dan Kompleksitas Operasional Rendah:** Pengoperasian node terdistribusi, koordinasi konsorsium, dan audit smart contract menuntut biaya dan keahlian teknis yang tidak sebanding jika integritas data cukup dijamin oleh tanda tangan digital tersertifikasi (PSrE / *X.509 Digital Certificate*) pada server institusi.

**Kesimpulan Kelayakan:** Kasus Kredensial Akademik memerlukan koordinasi multi-pihak independen (Kampus, LLDIKTI, Industri, Asosiasi Profesi), membutuhkan ketahanan terhadap manipulasi masa lalu (*tamper-proof audit trail*), dan tidak mentoleransi adanya satu pihak yang dapat secara sepihak menghapus rekam jejak ijazah sah. Oleh karena itu, **arsitektur konsorsium permissioned blockchain terbukti layak dan diperlukan**.

---

## 4. Keputusan Desain P2: Arsitektur Jaringan dan Tata Kelola (Governance)

### 4.1 Jenis Jaringan: Permissioned Consortium Blockchain
- **Justifikasi:** Jaringan publik tanpa izin (*permissionless / public*) seperti Ethereum Mainnet memiliki volatilitas biaya gas tinggi, latensi konsensus probabilistik, serta risiko kepatuhan hukum karena node validasi tersebar tanpa akuntabilitas yuridis. Sebaliknya, jaringan privat murni (*private*) gagal menciptakan desentralisasi kepercayaan.
- **Pilihan Arsitektur:** **Permissioned Consortium Blockchain**. Akses menulis blok dibatasi pada node validator resmi anggota konsorsium, sedangkan akses pembacaan/verifikasi publik disediakan secara terbuka (*open read*) melalui *read-only RPC gateway*.
- **Pembedaan Jelas Desain Produksi vs Prototipe Eksekusi:**
  - **Target Produksi Enterprise (Desain Rujukan):** **Hyperledger Besu** yang dikonfigurasi dengan konsensus **QBFT (Quorum Byzantine Fault Tolerance)**. Jaringan ini dijalankan oleh node institusional berkemampuan tinggi, mendukung *zero gas fee* internal atau *fixed gas*, dan kepatuhan penuh terhadap standar enterprise ISO/IEC 27001.
  - **Prototipe Laboratorium (Eksekusi Nyata Sesi Ini):** **Local EVM Blockchain (Hardhat)** dengan deterministik Chain ID `31337`. Dipilih agar seluruh logika smart contract, kontrol akses, batch Merkle root, dan simulasi penyerangan dapat diuji secara komprehensif, cepat, aman, dan 100% dapat direproduksi oleh dosen tanpa biaya jaringan (*zero-cost reproducibility*).

### 4.2 Peran Node dalam Konsorsium
1. **Validator Nodes (Core Consortium):**
   - Dioperasikan oleh entitas terakreditasi: Universitas Siliwangi, Universitas Mitra, LLDIKTI Wilayah IV, dan Badan Akreditasi Nasional (BAN-PT).
   - Menjalankan konsensus QBFT, mengusulkan dan memvalidasi blok baru, mengeksekusi smart contract, dan memelihara salinan buku besar penuh (*full ledger*).
2. **Observer / RPC Read-Only Nodes:**
   - Dioperasikan oleh asosiasi industri, kementerian tenaga kerja, atau portal verifikasi publik.
   - Tidak memiliki hak suara dalam konsensus; hanya menyinkronkan state blok untuk melayani permintaan pembacaan verifikasi dokumen dari masyarakat luas dengan latensi rendah.

### 4.3 Evaluasi Mekanisme Konsensus

| Kriteria | Proof-of-Work (PoW) | Proof-of-Stake (PoS) | QBFT / PoA (Pilihan Terpilih) |
| :--- | :--- | :--- | :--- |
| **Finalitas Blok** | Probabilistik (risiko *reorganization*) | Deterministik bertahap (memerlukan beberapa epoch) | **Seketika / Instan (*Immediate Finality*)** |
| **Konsumsi Energi** | Sangat masif (komputasi hash) | Rendah | **Sangat Rendah (*Green Computing*)** |
| **Throughput** | Rendah (7–15 TPS) | Sedang–Tinggi (100–1000 TPS) | **Tinggi (500–2.000 TPS)** |
| **Model Keamanan** | Dominasi kekuatan komputasi (51% attack) | Konsentrasi modal/token ekonomi | **Identitas hukum yuridis terdaftar ($3f + 1$)** |
| **Biaya Transaksi** | Volatil & mahal (*gas fee market*) | Bergantung fluktuasi harga token | **Dapat diprediksi / Rp0 (*Zero Internal Gas*)** |
| **Kesesuaian Kasus** | Tidak layak | Kurang efisien untuk konsorsium akademik | **Sangat Sesuai untuk Konsorsium Pendidikan** |

**Alasan Pemilihan QBFT/PoA:**
1. *Immediate Finality:* Blok yang telah ditandatangani oleh $> 2/3$ validator tidak dapat mengalami *fork*, memberikan kepastian hukum seketika atas status ijazah.
2. *Non-economic Security:* Integritas validator tidak digantungkan pada spekulasi token kripto, melainkan reputasi institusional dan perjanjian konsorsium hukum (*legal agreement*).
3. *Zero-gas Operation:* Biaya pemeliharaan operasional dapat didistribusikan merata di antara anggota konsorsium tanpa membebankan biaya verifikasi kepada lulusan atau industri.

### 4.4 Model Tata Kelola Konsorsium (Governance)
1. **Dewan Tata Kelola Konsorsium (*Consortium Steering Committee*):** Beranggotakan perwakilan pimpinan perguruan tinggi anggota dan regulator (LLDIKTI). Mengendalikan kebijakan keanggotaan dan resolusi perselisihan.
2. **Prosedur Onboarding Validator:** Calon validator baru wajib melewati verifikasi legalitas, penandatanganan pakta integritas node, dan persetujuan suara mayoritas $\ge 67\%$ dari validator aktif melalui voting on-chain/multisig.
3. **Pengelolaan Peningkatan Kontrak (*Upgradeability & Time-Lock*):** Smart contract menggunakan arsitektur UUPS (*Universal Upgradeable Proxy Standard*) atau kontrak modular yang dikendalikan oleh kontrak **TimelockController** minimal 48 jam. Hal ini mencegah perubahan logika kontrak secara sepihak atau mendadak tanpa pemberitahuan kepada seluruh pemangku kepentingan.

---

## 5. Keputusan Desain P3: Model Data Kredensial, Kriptografi, dan Kepatuhan Privasi

### 5.1 Standar Interoperabilitas: W3C Verifiable Credentials & DID
Dokumen akademik distrukturkan mengikuti standar **W3C Verifiable Credentials Data Model v2.0**:
- **Format:** JSON-LD (*JavaScript Object Notation for Linked Data*).
- **Subjek Identitas:** Menggunakan **W3C Decentralized Identifier (DID)**, misalnya `did:unsil:alumni:237006079` atau DID berbasis metode `did:key` / `did:jwk`.
- **Standar Kompetensi Tambahan:** Mendukung metadata **1EdTech Open Badges v3.0** untuk sertifikat mikrokredensial dan kompetensi laboratorium.

### 5.2 Strategi Privasi: Mengapa Plain Hashing Berbahaya dan UU PDP Menuntut Off-Chain
- **Bahaya Hashing Tanpa Garam pada Data Berentropi Rendah:**
  - Data akademik sering kali memiliki ruang variasi nilai yang sangat sempit (*low entropy*), misalnya NIM berurutan, Indeks Prestasi Kumulatif (IPK) dengan rentang 2.00–4.00, atau tahun kelulusan.
  - Jika nilai seperti `"237006079,3.85"` langsung di-hash dengan SHA-256 tanpa pelindung, penyerang dapat dengan mudah membuat tabel pra-komputasi (*rainbow tables*) atau melakukan serangan kamus (*brute-force dictionary attack*) untuk membongkar nilai asli di balik hash on-chain.
- **Solusi Kriptografis: Salted Hash & Merkle Leaf Commitment:**
  - Setiap bidang data (*claim*) maupun dokumen lengkap wajib digabungkan dengan nilai acak berkekuatan kriptografis tinggi (*cryptographic salt / blinding factor* minimal 256-bit):
    $$\text{Leaf}_i = \text{SHA-256}(\text{Claim}_i \parallel \text{Salt}_i)$$
  - Komitmen individual digabungkan ke dalam **Merkle Tree**, dan hanya **Merkle Root** yang dipublikasikan ke blockchain.
- **Kepatuhan Terhadap UU No. 27 Tahun 2022 (UU PDP):**
  - **Prinsip Hak untuk Dihapus (*Right to Erasure / Right to be Forgotten*, Pasal 43 UU PDP):** Sifat dasar blockchain adalah kekal (*immutable*). Jika Data Pribadi (PII seperti Nama, NIK, Tempat/Tanggal Lahir) ditulis ke on-chain, institusi akan melanggar hukum saat subjek meminta penghapusan data atau perbaikan data pribadi.
  - **Arsitektur Pemisahan On-Chain vs Off-Chain:**
    - **Off-Chain (Penyimpanan Pribadi Mahasiswa / SIAKAD Kampus):** Menyimpan dokumen lengkap JSON-LD, tanda tangan kriptografis penerbit, dan pasangan *salt*.
    - **On-Chain (Blockchain Konsorsium):** HANYA menyimpan Merkle Root per batch wisuda, ID Batch, Timestamp penerbitan, Alamat Issuer, Status Pencabutan (*Revocation Bitmask/Mapping*), dan Versi Skema. **Tidak ada satu pun bit data pribadi yang menyentuh blockchain.**

### 5.3 Selective Disclosure (Pengungkapan Selektif)
Dengan struktur Merkle Tree, lulusan dapat membuktikan bahwa mereka benar lulusan Program Studi Informatika dengan predikat "Dengan Pujian" kepada verifikator kerja, **tanpa harus memperlihatkan riwayat nilai mata kuliah lain atau data sensitif lainnya**. Verifikator cukup diberikan:
1. Pasangan klaim yang ingin diverifikasi beserta salt-nya.
2. Rangkaian bukti Merkle (*Merkle Audit Path / Proof*).
3. Merkle Root yang dicocokkan langsung ke smart contract di blockchain.

---

## 6. Keputusan Desain P4: Keamanan, Manajemen Kunci, dan Respons Insiden

### 6.1 STRIDE Threat Model
Berikut adalah analisis ancaman mendalam berbasis metodologi STRIDE untuk sistem verifikasi kredensial:

| Kode Ancaman | Kategori STRIDE | Skenario Ancaman Khusus Kredensial | Dampak Bisnis / Teknis | Tingkat Risiko | Kontrol Mitigasi |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **TH-01** | **Spoofing** | Penyerang menyamar sebagai Biro Akademik resmi untuk menerbitkan ijazah palsu langsung ke smart contract. | Kredibilitas institusi rusak; ijazah bodong beredar dengan stempel sistem. | **Tinggi** | Role-Based Access Control (`ISSUER_ROLE`) via OpenZeppelin; otorisasi transaksi wajib menggunakan skema dompet multi-tanda tangan (*Multisig Gnosis Safe*). |
| **TH-02** | **Tampering** | Pemilik dokumen mengubah IPK pada berkas PDF/JSON-LD lokal lalu menyerahkannya ke HRD. | Dokumen palsu lolos verifikasi jika verifikator ceroboh. | **Tinggi** | Hash bergaram pada dokumen off-chain dihitung ulang oleh verifikator dan dicocokkan dengan daun Merkle yang berakar pada Merkle Root on-chain. Integritas dijamin oleh resistensi benturan (*collision resistance*) SHA-256. |
| **TH-03** | **Repudiation** | Kampus menyangkal pernah menerbitkan ijazah yang sah kepada mahasiswa tertentu akibat perselisihan internal. | Kerugian hukum bagi lulusan sah. | **Sedang** | Transaksi penerbitan root batch tersimpan abadi di buku besar lengkap dengan signature digital issuer dan event log `BatchIssued` yang dapat diaudit regulator. |
| **TH-04** | **Information Disclosure** | Pihak luar menyadap transaksi blockchain untuk membongkar nilai IPK atau identitas mahasiswa dari data on-chain. | Pelanggaran UU PDP; tuntutan denda hukum bagi kampus. | **Kritis** | Zero On-Chain PII; data di-hash menggunakan salt 256-bit berentropi tinggi; hanya Merkle Root yang tersimpan di blockchain. |
| **TH-05** | **Denial of Service (DoS)** | Penyerang membanjiri RPC node verifikasi dengan jutaan kueri atau mencoba mengeksploitasi konsumsi gas kontrak pintar. | Layanan verifikasi ijazah lumpuh; HRD gagal memverifikasi calon pekerja. | **Sedang** | Pembatasan laju (*Rate limiting*) pada gateway RPC; struktur penyimpanan smart contract menggunakan $O(1)$ mapping lookup tanpa perulangan dinamis tak terbatas (*unbounded loops*). |
| **TH-06** | **Elevation of Privilege** | Penyerang mengeksploitasi fungsi administratif untuk mengangkat alamat pribadinya sebagai admin atau revoker. | Pembajakan kendali seluruh registri ijazah universitas. | **Kritis** | Pembagian peran terpisah (`DEFAULT_ADMIN_ROLE`, `ISSUER_ROLE`, `REVOKER_ROLE`); admin wajib dikendalikan oleh kontrak multi-sig institusi dengan jeda waktu eksekusi (*timelock*). |

### 6.2 Manajemen Kunci (Key Management Strategy)
1. **Kunci Penerbit Institusi (Issuer Keys):**
   - Menggunakan dompet multi-tanda tangan (*Multisig Wallet* / Safe) dengan ambang batas $m$-of-$n$ (misalnya 3 dari 5 kunci: Rektor, Dekan Fakultas Teknik, Kepala Biro Akademik, Ketua Jurusan Informatika, dan Administrator TIK).
   - Private key tersimpan di dalam perangkat keras aman (*Hardware Security Module / HSM* atau YubiKey FIPS 140-2 Level 3).
2. **Kunci Pemilik Dokumen (Holder / Student Keys):**
   - Mahasiswa mengelola pasangan kunci menggunakan dompet digital berbasis peramban/seluler.
   - **Mekanisme Pemulihan Kunci (Key Recovery):** Karena mahasiswa tidak melakukan transaksi on-chain yang membutuhkan gas, kehilangan private key dompet mahasiswa **tidak menghanguskan status kelulusan mereka**. Mahasiswa dapat mengajukan rotasi DID melalui verifikasi biometrik/KTP di Biro Akademik, dan universitas akan menerbitkan ulang atestasi klaim dokumen yang diikat ke DID baru mahasiswa tanpa mengubah Merkle Root yang sudah ada di blockchain.

### 6.3 Prosedur Tanggap Darurat Insiden 24 Jam Pertama (SOP)
Jika terjadi insiden kebocoran salah satu private key penandatangan penerbit:
- **Jam 0 – 2 (Identifikasi & Isolasi):** Sistem deteksi otomatis membunyikan alarm; administrator mengaktifkan fungsi darurat `pause()` pada smart contract untuk membekukan fungsi penerbitan batch baru.
- **Jam 2 – 6 (Pencabutan Kunci & Investigasi Forensik):** Multisig admin mencabut peran `ISSUER_ROLE` dari alamat yang terkompromi melalui fungsi `revokeRole()`. Log transaksi dianalisis untuk memastikan tidak ada batch ijazah palsu yang sempat dimasukkan.
- **Jam 6 – 12 (Rotasi & Re-keying):** Anggota konsorsium membangkitkan pasangan kunci baru pada perangkat HSM bersih dan mendaftarkan alamat baru ke smart contract.
- **Jam 12 – 24 (Pemulihan & Transparansi):** Menyalakan kembali kontrak (`unpause()`), mempublikasikan laporan insiden (*post-mortem report*) kepada regulator konsorsium, dan memulihkan operasi normal.

---

## 7. Keputusan Desain P5: Spesifikasi Prototipe dan Kerangka Pengujian

### 7.1 Spesifikasi Smart Contract: `AcademicCredentialRegistry.sol`
Smart contract ditulis dalam Solidity versi `^0.8.28` dengan memanfaatkan pustaka standar industri OpenZeppelin Contracts v5:
- `AccessControl`: Membagi kewenangan menjadi `DEFAULT_ADMIN_ROLE`, `ISSUER_ROLE`, dan `REVOKER_ROLE`.
- `Pausable`: Memungkinkan pembekuan fungsi kritis saat masa pemeliharaan atau insiden keamanan.
- **Struktur Data On-Chain:**
  ```solidity
  struct BatchRecord {
      bytes32 merkleRoot;
      uint256 issuanceTimestamp;
      uint256 graduateCount;
      string metadataURI; // URI metadata skema non-PII (misal IPFS hash skema)
      bool active;
  }
  ```
- **State Pencabutan Efisien (*Revocation*):**
  - Menggunakan mapping hash daun individual ke status pencabutan: `mapping(bytes32 => bool) public isCredentialRevoked;`
  - Memberikan kompleksitas waktu $O(1)$ untuk pengecekan status dan pembatalan tanpa memerlukan perulangan komputasi.
- **Fungsi Verifikasi On-Chain:**
  - `verifyCredential(bytes32 leaf, bytes32[] calldata proof, bytes32 batchId)`: Memverifikasi secara kriptografis keaslian daun ijazah terhadap Merkle Root batch yang tersimpan.

### 7.2 Rencana Matriks Pengujian Komprehensif (T-01 s.d. T-07)
Seluruh pengujian dijalankan secara otomatis menggunakan skrip Hardhat TypeScript dengan target kelulusan 100%:

| ID Uji | Tipe Pengujian | Skenario dan Tindakan | Ekspektasi Hasil | ID Bukti Terkait |
| :---: | :---: | :--- | :--- | :---: |
| **T-01** | Fungsional | Penerbitan batch ijazah wisuda oleh akun berwenang `ISSUER_ROLE`. | Transaksi berhasil, event `BatchIssued` terpancar, root tersimpan di state. | B-02 |
| **T-02** | Fungsional | Verifikasi keabsahan bukti Merkle (*valid Merkle proof*) untuk ijazah sah. | Fungsi mengembalikan nilai `true` dan status aktif. | B-03 |
| **T-03** | Keamanan (Tamper) | Pengujian modifikasi klaim data (misal IPK diubah dari 3.85 menjadi 4.00 atau salt dimanipulasi). | Daun Merkle yang dihitung ulang berbeda; verifikasi ditolak (`false`). | B-04 |
| **T-04** | Akses Kontrol | Upaya penerbitan batch oleh akun peretas yang tidak memiliki peran `ISSUER_ROLE`. | Transaksi dibatalkan (*revert*) dengan pesan error AccessControl Unauthorized. | B-05 |
| **T-05** | Fungsional / Batas | Pencabutan kredensial tertentu oleh akun `REVOKER_ROLE` dan pengecekan ulang verifikasi. | Status kredensial tercatat dicabut; verifikasi gagal dengan status `REVOKED`. | B-06 |
| **T-06** | Akses Kontrol | Upaya pencabutan ijazah oleh pihak ketiga yang bukan revoker resmi. | Transaksi dibatalkan (*revert*) dengan error AccessControl Unauthorized. | B-05 |
| **T-07** | Keamanan (Pausable)| Upaya penerbitan saat kontrak dalam status `paused`. | Transaksi dibatalkan (*revert*) dengan error `EnforcedPause`. | B-06 |

---

## 8. Keputusan Desain P6: Batasan Teknis, Pertimbangan Etika, dan Draf Refleksi

### 8.1 Batasan Prototipe Laboratorium
1. **Lingkungan Single-Node Local EVM:** Prototipe dijalankan pada mesin lokal pengembang (Hardhat Network) yang mensimulasikan lingkungan EVM. Konsensus multi-node QBFT enterprise (Hyperledger Besu) diposisikan sebagai arsitektur rujukan produksi dan tidak di-deploy pada sesi pengujian lokal ini demi efisiensi resource pengujian.
2. **Data Simulasi:** Seluruh data mahasiswa, nomor ijazah, dan nilai akademik yang digunakan dalam pengujian adalah 100% data simulasi sintetis fiktif guna menjamin tidak adanya kebocoran data riil.

### 8.2 Pertimbangan Etika dan Kesenjangan Digital (*Digital Divide*)
1. **Inklusivitas Lulusan Tanpa Gawai Cerdas:** Tidak semua lulusan memiliki literasi web3 atau ponsel pintar canggih untuk mengelola dompet digital pribadi. Solusi: Sistem wajib menyediakan *fallback mechanism* berupa dokumen cetak fisik resmi yang dilengkapi **QR-Code Kriptografis**. QR-Code tersebut memuat link verifikasi publik yang langsung mengarahkan verifikator ke portal baca konsorsium.
2. **Netralitas Biaya:** Lulusan dan pencari kerja tidak boleh dibebani biaya gas atau biaya langganan apa pun untuk sekadar membuktikan ijazah yang sah. Seluruh biaya komputasi konsorsium ditanggung oleh anggaran operasional perguruan tinggi dan konsorsium.

### 8.3 Draf Refleksi Pengambilan Keputusan Mahasiswa (P6)
> `[DRAFT - untuk ditinjau dan disesuaikan oleh Fajar Geran Arifin]`  
> *"Dalam merancang sistem verifikasi kredensial akademik ini, saya menyadari bahwa tantangan terbesar arsitektur blockchain bukanlah pada penulisan kode smart contract, melainkan pada ketepatan penentuan batasan batas kepercayaan (trust boundary) dan kepatuhan terhadap hak privasi manusia. Godaan terbesar seorang insinyur sering kali adalah menaruh seluruh data ijazah ke dalam blockchain karena anggapan bahwa semakin banyak data di blockchain, semakin aman sistem tersebut. Melalui studi kasus ini, saya belajar secara mendalam bahwa menaruh data pribadi di blockchain adalah kekeliruan fatal yang melanggar prinsip Right to Erasure UU PDP. Keputusan untuk memadukan Merkle Tree, salt berentropi tinggi, dan arsitektur konsorsium permissioned membuktikan bahwa blockchain paling efektif bila diperlakukan sebagai jangkar integritas (integrity anchor), bukan sebagai basis data penyimpanan dokumen."*

---
Dokumen keputusan desain ini menjadi dasar rujukan tunggal untuk pelaksanaan Fase 2 (Implementasi Prototipe & Bukti Pengujian Nyata).
