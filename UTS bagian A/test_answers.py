#!/usr/bin/env python3
"""
Script to generate UTS Blockchain Bagian A answers document.
Student: Fajar Geran Arifin (NPM: 237006079)
"""

import os
import re
import docx
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

SRC_PATH = "/home/fajar-geran-arifin/Documents/kuliah/block chain/UTS bagian A/UTS_Blockchain_Bagian_A_237006079_Fajar_Geran_Arifin.docx"
DST_PATH = "/home/fajar-geran-arifin/Documents/kuliah/block chain/UTS bagian A/UTS_Blockchain_Bagian_A_237006079_Fajar_Geran_Arifin_JAWABAN.docx"
IMG_PATH = "/home/fajar-geran-arifin/Documents/kuliah/block chain/UTS bagian A/arsitektur-blockchain.png"

def count_words(text):
    clean = re.sub(r'\[.*?\]', '', text)
    clean = re.sub(r'[^\w\s-]', ' ', clean)
    words = clean.split()
    return len(words)

# Answers definitions
ANSWERS = {}

# ==============================================================================
# KASUS 1
# ==============================================================================
ANSWERS["1.1"] = [
    ("paragraph", "Berdasarkan konteks konsorsium rantai pasok pangan yang melibatkan koperasi petani, pabrik pengolahan, perusahaan logistik, laboratorium mutu, dan jaringan ritel, berikut adalah identifikasi kebutuhan bisnis dan kendala teknis yang menentukan desain sistem:"),
    ("paragraph", "A. Tiga Kebutuhan Bisnis:"),
    ("paragraph", "1. Rekam Jejak Audit Bersama yang Abadi (Shared Immutable Audit Trail):\nKonsorsium membutuhkan satu sumber kebenaran data tunggal yang transparan dan tahan manipulasi untuk mendokumentasikan silsilah kepemilikan serta transformasi komoditas dari lahan tani hingga gerai ritel, mengeliminasi perselisihan dan rekonsiliasi manual antar-organisasi."),
    ("paragraph", "2. Akselerasi Penarikan Produk (Rapid Product Recall):\nMemangkas waktu pencocokan nomor lot terdampak dari sebelumnya 2–3 hari menjadi hitungan menit atau jam ketika terjadi insiden kontaminasi, guna mencegah konsumsi produk berbahaya, melindungi keselamatan publik, dan menekan kerugian finansial akibat penarikan massal yang salah sasaran."),
    ("paragraph", "3. Perlindungan Kerahasiaan Komersial Selektif (Selective Confidentiality):\nMenjamin kerahasiaan data komersial sensitif, seperti harga pembelian bahan baku antar-pemasok dan identitas privat (PII) petani tertentu, agar tidak dapat diakses oleh pihak yang tidak berwenang, namun integritas dan keabsahan transaksinya tetap dapat diverifikasi oleh seluruh konsorsium."),
    ("paragraph", "B. Dua Kendala Teknis:"),
    ("paragraph", "1. Throughput Transaksi dan Finalitas Deterministik:\nSistem harus mampu melayani beban transaksi operasional sekitar 25 transaksi per detik (TPS) dengan latensi commit rendah (di bawah beberapa detik) dan finalitas instan tanpa risiko percabangan rantai (zero-forking), mengingat proses serah terima logistik dan pabrikasi menuntut konfirmasi status seketika."),
    ("paragraph", "2. Arsitektur Hibrida On-Chain/Off-Chain dan Integrasi Sistem Warisan:\nBerkas digital berukuran besar (seperti foto fisik panen, sertifikat inspeksi, dan dokumen PDF hasil uji laboratorium) tidak layak disimpan langsung di on-chain ledger karena keterbatasan komputasi dan media simpan node, sehingga menuntut integrasi penyimpanan off-chain terenkripsi yang diselaraskan dengan basis data internal (ERP/RDBMS) eksisting masing-masing entitas.")
]

ANSWERS["1.2"] = [
    ("paragraph", "A. Pemilihan Jenis Blockchain dan Mekanisme Konsensus:"),
    ("paragraph", "Untuk konsorsium rantai pasok pangan ini, jenis blockchain yang paling tepat adalah Permissioned / Consortium Blockchain dengan platform Hyperledger Fabric. Mekanisme konsensus yang direkomendasikan adalah Ordering Service berbasis Byzantine Fault Tolerant, khususnya SmartBFT (tersedia pada Hyperledger Fabric v3)."),
    ("paragraph", "B. Argumentasi dan Analisis Trade-off:"),
    ("paragraph", "1. Kesesuaian Tata Kelola Jaringan: Seluruh anggota konsorsium (koperasi, pabrik, logistik, lab, ritel) telah diketahui identitas hukumnya secara pasti. Melalui Hyperledger Fabric, setiap entitas diverifikasi menggunakan Certificate Authority (CA) dan Membership Service Provider (MSP), meniadakan kebutuhan mekanisme penambangan anonim ala blockchain publik yang boros energi dan memicu biaya transaksi (gas fee) fluktuatif."),
    ("paragraph", "2. Skalabilitas Performa: Kebutuhan throughput sebesar 25 TPS tergolong sangat wajar dan berada jauh di bawah kapasitas puncak Hyperledger Fabric yang mampu memproses ratusan hingga ribuan TPS dengan finalitas deterministik sub-detik."),
    ("paragraph", "3. Analisis Trade-off Konsensus (SmartBFT vs. Raft): Konsensus berbasis Raft (Crash Fault Tolerant/CFT) memang lebih sederhana dan berkinerja tinggi, namun hanya tahan terhadap node yang padam (crash fault), bukan node yang mengirimkan data bertentangan atau bertindak curang (Byzantine fault). Mengingat anggota konsorsium merupakan entitas bisnis independen dengan kepentingan ekonomi yang berpotensi bersinggungan, SmartBFT jauh lebih tepat karena menjamin konsensus tetap sah selama jumlah node jahat tidak melebihi f dari total 3f + 1 node pemesanan, meskipun memerlukan sedikit overhead komunikasi koordinasi pesan."),
    ("paragraph", "C. Perbandingan dengan Alternatif:"),
    ("paragraph", "1. Ethereum PoS (Blockchain Publik): Tidak sesuai karena seluruh data transaksi bersifat transparan secara inheren (melanggar kerahasiaan harga dan identitas petani), memiliki biaya gas yang tidak pasti, serta latensi finalitas blok mencapai 12–15 menit."),
    ("paragraph", "2. Quorum / Hyperledger Besu (IBFT/QBFT): Meskipun merupakan blockchain konsorsium BFT, model eksekusinya berbasis order-execute di mana seluruh node memvalidasi transaksi di saluran bersama, berbeda dengan arsitektur execute-order-validate milik Fabric yang memungkinkan isolasi data granular melalui Private Data Collections (PDC) dan sub-channel.")
]

ANSWERS["1.3"] = [
    ("image", IMG_PATH, Cm(16.0)),
    ("caption", "Gambar 1. Arsitektur logis sistem ketertelusuran pangan"),
    ("paragraph", "Penjelasan Arsitektur Logis Sistem:\nArsitektur pada Gambar 1 mengintegrasikan lima aktor konsorsium (Koperasi, Pabrik Pengolah, Perusahaan Logistik, Laboratorium, dan Jaringan Ritel) yang berinteraksi melalui Aplikasi Organisasi untuk submit transaksi dan monitoring lot, serta Aplikasi Keterlacakan untuk akses publik konsumen via pemindaian kode QR. Pada lapisan jaringan Hyperledger Fabric, setiap organisasi mengoperasikan Peer Node yang menyimpan World State (CouchDB) dan mengeksekusi logika bisnis smart contract (Chaincode). Konsensus pengurutan transaksi dikelola secara terdesentralisasi oleh klaster Ordering Service berbasis SmartBFT (Node 1–4) yang mendistribusikan blok ke bar Validasi & Pencatatan Ledger guna verifikasi kebijakan endorsement (VSCC) dan validasi konflik versi (MVCC). Sistem menerapkan penyimpanan hibrida: data transaksi bernilai tinggi (nomor lot universal, relasi silsilah antar-lot, jejak peristiwa serah terima, status mutu, status penarikan/recall, serta hash dokumen pendukung) disimpan secara permanen pada on-chain ledger, sedangkan dokumen berukuran besar (PDF laporan uji lab, faktur, foto komoditas, dan rekaman sensor IoT) disimpan pada penyimpanan off-chain terenkripsi (IPFS/Cloud). Data komersial sensitif seperti harga pemasok dilindungi secara bilateral menggunakan Private Data Collections (PDC) via protokol Fabric Gossip. Seluruh interaksi diamankan oleh Certificate Authority (CA) dan Membership Service Provider (MSP) berbasis PKI/X.509 dan RBAC, dengan penegakan aturan di mana penerbitan hasil uji mutu mutlak menjadi hak MSP Laboratorium dan serah terima logistik mewajibkan endorsement ganda dari pihak pengirim dan penerima.")
]

ANSWERS["1.4"] = [
    ("paragraph", "Dua indikator keberhasilan pilot project yang terukur ditetapkan sebagai berikut:"),
    ("paragraph", "1. Durasi Waktu Pelacakan Lot Terdampak (Recall Traceability Time):\nTarget penurunan durasi pelacakan silsilah lot lengkap dari hulu ke hilir dari sebelumnya 2–3 hari (48–72 jam) menjadi di bawah 15 menit. Indikator ini diukur melalui uji simulasi penarikan produk (mock recall) berkala, dihitung sejak kueri nomor lot dimasukkan hingga sistem berhasil memetakan seluruh rantai distribusi dan lokasi gerai ritel yang menampung lot tersebut."),
    ("paragraph", "2. Tingkat Kelengkapan dan Integritas Pencatatan Data Lot (Data Completeness Rate):\nTarget minimal 95% dari seluruh lot komoditas yang diproses selama masa pilot project tercatat secara lengkap dan konsisten dari panen awal hingga gerai ritel pada on-chain ledger. Indikator diukur melalui audit rekonsiliasi data mingguan antara volume fisik di ERP internal masing-masing entitas dengan transaksi yang berhasil ter-commit di blockchain.")
]

# ==============================================================================
# KASUS 2
# ==============================================================================
ANSWERS["2.1"] = [
    ("paragraph", "Berikut adalah analisis insiden keamanan wallet treasury organisasi yang memisahkan antara fakta empiris, hipotesis investigatif, dan bukti forensik yang wajib dikumpulkan:"),
    ("table_2_1", None),
    ("paragraph", "Urutan Kejadian Kronologis yang Paling Mungkin:"),
    ("paragraph", "1. [Hipotesis] Penyerang merekayasa domain typosquatting (berbeda satu karakter dari domain resmi) dan menyebarkan antarmuka dApp web tiruan yang identik secara visual."),
    ("paragraph", "2. [Fakta] Staf mengakses antarmuka melalui perangkat kerja sah yang terdaftar dalam log sistem (kemungkinan akibat kelalaian pengetikan URL atau tautan phishing)."),
    ("paragraph", "3. [Hipotesis] Antarmuka palsu memicu interaksi web3 dan menampilkan dialog konfirmasi yang disamarkan sebagai rutinitas 'Pembaruan Kontrak'."),
    ("paragraph", "4. [Fakta] Staf menyetujui dan menandatangani transaksi tersebut menggunakan browser wallet yang menyimpan private key treasury."),
    ("paragraph", "5. [Hipotesis] Transaksi yang ditandatangani sebenarnya memuat payload pengalihan izin aset (infinite token approval/permit) atau pemindahan langsung ke alamat penyerang (blind signing)."),
    ("paragraph", "6. [Fakta] Transaksi di-broadcast ke jaringan blockchain, diverifikasi oleh validator, dan dieksekusi secara sah sehingga aset treasury terkuras seketika tanpa adanya hambatan multisignature.")
]

ANSWERS["2.2"] = [
    ("paragraph", "Tanda tangan digital (berbasis algoritma ECDSA secp256k1) tetap valid secara teknis karena mekanisme kriptografi blockchain hanya bertugas membuktikan autentisitas matematis dan integritas data, bukan menguji intensi psikologis atau konteks kebenaran manusia di balik penandatanganan tersebut (semantic blindness)."),
    ("paragraph", "Secara protokol, tanda tangan digital membuktikan dua hal pasti: (1) transaksi didekripsi menggunakan public key yang secara matematis berpasangan dengan private key yang sah (autentikasi pengirim), dan (2) muatan data transaksi (payload byte array) tidak mengalami modifikasi sejak ditandatangani (integritas pesan). Ketika staf menjadi korban rekayasa sosial, staf secara sadar menggunakan private key treasury yang tersimpan di browser wallet untuk menandatangani data."),
    ("paragraph", "Pada kasus ini terjadi fenomena blind signing: antarmuka web menampilkan narasi palsu 'Pembaruan Kontrak', padahal muatan byte data heksadesimal mentah yang diserahkan ke wallet adalah fungsi pemindahan aset atau transfer approval tak terbatas. Karena penandatanganan dilakukan menggunakan private key yang valid, node validator blockchain memproses transaksi tersebut sebagai instruksi yang sah dan memutasi saldo secara permanen di buku besar.")
]

ANSWERS["2.3"] = [
    ("paragraph", "Untuk mencegah insiden serupa terulang, dirancang arsitektur pengamanan berlapis (Defense-in-Depth) yang mencakup empat pilar:"),
    ("paragraph", "1. Lapisan Manusia (People):\n- Pelatihan Anti-Phishing dan Simulasi Rekayasa Sosial: Edukasi periodik mengenai ancaman typosquatting dan teknik manipulasi antarmuka web3.\n- Disiplin Akses Berbasis Bookmark: Mewajibkan operator treasury mengakses antarmuka dApp hanya melalui tautan resmi yang telah disimpan di bookmark browser terverifikasi, serta larangan keras mengakses antarmuka dari tautan pesan instan atau email.\n- Verifikasi Parameter Mentah: Mewajibkan verifikasi manual terhadap alamat kontrak tujuan, nomor fungsi, dan kuantitas token sebelum menandatangani transaksi."),
    ("paragraph", "2. Lapisan Proses (Process):\n- Pemisahan Wewenang (Segregation of Duties): Menerapkan prinsip dual-control / four-eyes di mana inisiasi transaksi dan persetujuan akhir harus dieksekusi oleh individu berbeda.\n- Prosedur Operasional Standar (SOP) Treasury: Penetapan batas wewenang transaksi dan protokol eskalasi insiden darurat.\n- Rekonsiliasi Kas Berkala: Pencocokan harian antara pembukuan internal organisasi dan saldo on-chain."),
    ("paragraph", "3. Lapisan Wallet (Infrastructure):\n- Migrasi ke Multi-Signature / MPC: Menghapus total penyimpanan private key tunggal pada browser extension, dan memigrasikan treasury ke smart contract multisig (misal Safe / Gnosis Safe) atau Multi-Party Computation (MPC) dengan ambang batas minimal 3-of-5 dari perangkat terpisah.\n- Isolasi Hardware Wallet (Cold Storage): Mewajibkan seluruh penandatangan menggunakan hardware wallet (Ledger/Trezor) dengan fitur layar verifikasi independen (clear signing), serta memisahkan hot wallet untuk operasional harian kecil dan cold vault untuk aset utama."),
    ("paragraph", "4. Lapisan Kontrol Transaksi (Transaction Policy Controls):\n- Allowlist / Whitelist Alamat: Membatasi eksekusi transaksi hanya ke alamat kontrak atau mitra terdaftar yang telah diaudit.\n- Time-Lock Delay dan Spending Limits: Menerapkan batas nominal transaksi harian serta jeda waktu tunda (time-lock 24–48 jam) untuk transaksi bernilai besar guna memberikan jendela intervensi pembatalan.\n- Simulasi Transaksi Pra-Eksekusi: Memasang alat simulasi transaksi otomatis (seperti Tenderly atau PocketUniverse) untuk memvisualisasikan dampak mutasi saldo sebelum penandatanganan dilakukan.")
]

ANSWERS["2.4"] = [
    ("paragraph", "Tindakan pada 24 jam pertama harus memprioritaskan preservasi bukti digital volatil sebelum langkah remediasi:"),
    ("paragraph", "1. Jam 0–2 (Aktivasi Tim & Isolasi Non-Destruktif):\nDeklarasikan status darurat insiden. Segera putuskan perangkat staf dari koneksi internet dan jaringan lokal (cabut kabel LAN, matikan Wi-Fi) tanpa mematikan daya (power off) atau mereboot sistem untuk menjaga integritas memori volatil. Lakukan live acquisition untuk menduplikasi RAM (memory dump) guna mengamankan session token dan cache DNS, disusul pembuatan bit-stream disk image forensik terverifikasi hash SHA-256."),
    ("paragraph", "2. Jam 2–6 (Containment & Penyelamatan Aset):\nMelalui perangkat bersih (clean device) yang terisolasi, periksa status on-chain. Segera cabut (revoke) seluruh token allowance yang berisiko menggunakan platform terverifikasi, lalu selamatkan sisa aset treasury ke wallet multi-sig / cold storage baru."),
    ("paragraph", "3. Jam 6–12 (Tracing On-Chain & Koordinasi Eksternal):\nCatat transaction hash, ekstraksi alamat penerima peretas, dan lacak aliran dana secara real-time. Kirimkan peringatan darurat pembekuan aset (freeze request) beserta bukti hash ke bursa terpusat (CEX) yang dituju dana tersebut."),
    ("paragraph", "4. Jam 12–24 (Konsolidasi Bukti & Komunikasi Terkendali):\nAmankan log proxy, router, dan riwayat penjelajahan. Buat laporan kronologi awal untuk manajemen dan kepolisian (cyber crime unit), serta rilis pernyataan publik terukur tanpa membocorkan detail teknis yang rentan dieksploitasi ulang.")
]

# ==============================================================================
# KASUS 3
# ==============================================================================
ANSWERS["3.1"] = [
    ("paragraph", "Berdasarkan analisis arsitektur smart contract vault, diidentifikasi empat kerentanan dan kelemahan desain kritis beserta dampaknya:"),
    ("paragraph", "1. Kerentanan Reentrancy Akibat Pelanggaran Pola Checks-Effects-Interactions (Kritis):\nKontrak melakukan panggilan eksternal (external call) untuk mentransfer aset kepada pemanggil sebelum saldo internal pengguna dikurangi (balances[msg.sender]). Penyerang dapat menyebarkan kontrak eksploitasi dengan fungsi fallback() atau receive() yang memanggil ulang fungsi withdraw() secara rekursif sebelum saldo sempat dimutasi. Dampaknya, seluruh cadangan dana di dalam vault dapat dikuras habis (complete vault drain) dalam satu transaksi."),
    ("paragraph", "2. Ketergantungan pada Oracle Harga Tunggal (Tinggi):\nMengandalkan satu sumber oracle harga tanpa mekanisme pembanding menciptakan Single Point of Failure. Oracle tunggal (terutama spot price pool DEX) sangat rentan dimanipulasi secara artifisial melalui serangan flash loan dalam satu blok transaksi. Dampaknya, penyerang dapat mendistorsi kalkulasi harga aset/agunan untuk menarik aset melebihi hak proporsionalnya, memicu kebangkrutan likuiditas vault."),
    ("paragraph", "3. Ketiadaan Time-Lock pada Fungsi Admin Penggantian Oracle (Tinggi):\nFungsi admin dapat mengganti alamat kontrak oracle seketika tanpa jeda waktu tunda (time-lock). Desain ini menghadirkan risiko sentralisasi ekstrim dan bahaya kompromi kunci admin (rugged / stolen admin key). Apabila private key admin bocor, peretas dapat langsung mengarahkan oracle ke kontrak palsu buatannya yang mengembalikan harga manipulatif dan melucuti seluruh aset pengguna seketika."),
    ("paragraph", "4. Ketiadaan Circuit Breaker (Emergency Pause) dan Pengujian Invariant Sebelum Mainnet (Sedang-Tinggi):\nPenerapan langsung ke mainnet tanpa pengujian invariant matematis dan tanpa fungsi pembekuan darurat (pause switch) menghilangkan lapisan mitigasi krisis. Dampaknya, saat eksploitasi terjadi di mainnet, tim pengelola tidak memiliki mekanisme teknis untuk menghentikan fungsi penarikan sementara, memastikan kerugian total dana pengguna.")
]

ANSWERS["3.2"] = [
    ("paragraph", "A. Usulan Perbaikan Logika Penarikan (Withdrawal Logic):"),
    ("paragraph", "1. Penerapan Pola Checks-Effects-Interactions (CEI):\nUrutan eksekusi fungsi withdraw wajib dibalik secara ketat:\n- Checks: Validasi input dan kecukupan saldo pemanggil (require(balances[msg.sender] >= amount, 'Saldo tidak mencukupi'); require(amount > 0, 'Nominal tidak valid');).\n- Effects: Kurangi saldo internal pengguna pada state kontrak terlebih dahulu (balances[msg.sender] -= amount;).\n- Interactions: Eksekusi transfer aset ke alamat eksternal pemanggil.\nAlasan: Jika penyerang mencoba reentrancy, pengecekan saldo pada panggilan kedua akan gagal karena saldo internal sudah nol/berkurang."),
    ("paragraph", "2. Penerapan Mutex Guard (nonReentrant):\nMenambahkan modifier nonReentrant dari library OpenZeppelin ReentrancyGuard sebagai pertahanan berlapis (defense-in-depth).\nAlasan: Mencegah eksekusi konkuren fungsi penarikan selama panggilan eksternal masih berjalan."),
    ("paragraph", "3. Penggunaan SafeERC20:\nMembungkus operasi transfer token ERC-20 dengan library SafeERC20 (safeTransfer).\nAlasan: Menangani token non-standar yang tidak mengembalikan nilai boolean agar transaksi tidak gagal secara tersembunyi."),
    ("paragraph", "B. Usulan Perbaikan Kontrol Akses Admin dan Tata Kelola Oracle:"),
    ("paragraph", "1. Tata Kelola Multi-Signature: Menghapus hak admin EOA tunggal dan mengalihkannya ke kontrak multi-sig (minimal 3-of-5).\nAlasan: Menghilangkan risiko kegagalan tunggal apabila satu private key hilang atau disusupi."),
    ("paragraph", "2. Penerapan Time-Lock Controller (24–48 Jam): Mewajibkan seluruh perubahan parameter kritis, terutama alamat oracle, melewati antrean tunda minimal 24–48 jam disertai emisi event on-chain transparan.\nAlasan: Memberikan jeda waktu bagi pengguna untuk memeriksa perubahan dan menarik dana mereka secara aman jika terjadi indikasi perubahan mencurigakan."),
    ("paragraph", "3. Redundansi Multi-Oracle dan Sanity Checks: Menggunakan agregator harga terdesentralisasi (misal Chainlink Price Feeds) yang dipadukan dengan Time-Weighted Average Price (TWAP) DEX, dilengkapi pemeriksaan keusangan data (staleness check via updatedAt), batasan deviasi harga, dan circuit breaker batas nilai wajar."),
    ("paragraph", "4. Mekanisme Emergency Pause: Menerapkan fungsi pause() berbasis role (OpenZeppelin Pausable) untuk membekukan setoran dan penarikan saat terdeteksi anomali.")
]

ANSWERS["3.3"] = [
    ("paragraph", "Strategi pengujian komprehensif dirancang menggunakan pendekatan multi-layer guna menjamin ketahanan smart contract vault sebelum rilis produksi:"),
    ("paragraph", "1. Unit Testing (Pemeriksaan Deterministik):\nMenguji seluruh alur kerja dasar dan batas ekstrem (edge cases): deposit saldo normal, penarikan penuh dan parsial, penolakan penarikan melebihi saldo atau bernilai nol, transfer aset token non-standar, penolakan akses pemanggil non-admin, serta simulasi serangan reentrancy aktif menggunakan mock contract jahat untuk memverifikasi bahwa panggilan rekursif berhasil ditolak oleh modifier nonReentrant dan pola CEI."),
    ("paragraph", "2. Fuzzing & Property-Based Testing (Pengujian Berbasis Sifat Acak):\nMemanfaatkan framework modern seperti Foundry (Forge Fuzz) atau Echidna untuk mengeksekusi ratusan ribu kombinasi urutan transaksi acak multi-pengguna dengan nilai parameter ekstrem (nilai setoran mendekati 0 hingga type(uint256).max, variasi waktu block timestamp). Pengujian ini bertujuan mendeteksi kerentanan tersembunyi seperti pembulatan presisi aritmatika (rounding errors) dan overflow/underflow."),
    ("paragraph", "3. Invariant Utama yang Wajib Terpelihara (Formal Invariants):"),
    ("paragraph", "a. Invariant Solvabilitas (Vault Solvency): Total saldo aset cadangan fisik yang dipegang oleh kontrak vault harus selalu lebih besar atau sama dengan total kewajiban saldo seluruh pengguna:\nTotalAsetFisik >= TotalSaldoPengguna"),
    ("paragraph", "b. Invariant Non-Negativitas Saldo: Saldo akun pengguna tidak boleh pernah bernilai negatif atau mengalami underflow di bawah kondisi transaksi apa pun."),
    ("paragraph", "c. Invariant Integritas Penarikan: Jumlah total aset yang ditarik oleh seorang pengguna sepanjang siklus hidup akunnya tidak boleh melebihi total setoran sah ditambah imbal hasil yang berhak diterimanya."),
    ("paragraph", "d. Invariant Otorisasi Parameter: Parameter kritis kontrak (oracle address, status pause) tidak dapat berubah tanpa melewati alur time-lock dan otorisasi multi-sig."),
    ("paragraph", "4. Tahap Lanjutan: Menjalankan static analysis (Slither, Mythril) dan menguji pada testnet publik sebelum audit eksternal independen.")
]

ANSWERS["3.4"] = [
    ("paragraph", "Keputusan:\nTUNDA (NO-GO) deployment ke mainnet secara mutlak hingga seluruh kerentanan kritis diperbaiki dan diverifikasi."),
    ("paragraph", "Kriteria Go / No-Go Terukur:"),
    ("paragraph", "1. Remediasi Total Temuan Kritis: 100% temuan kerentanan berstatus Kritis dan Tinggi (Reentrancy, manipulasi oracle, dan hak admin instan) telah diperbaiki, diuji ulang, dan memperoleh sertifikasi bebas celah kritis dari auditor keamanan independen ternama."),
    ("paragraph", "2. Keberhasilan Uji Invariant & Fuzzing: Invariant solvabilitas vault lolos pengujian fuzzing minimal 100.000 run tanpa satupun pelanggaran properti invariant."),
    ("paragraph", "3. Tata Kelola Aman Aktif: Kontrak Multi-Signature (ambang batas minimal 3-of-5) dan Time-Lock Controller (jeda minimal 24–48 jam) telah aktif terpasang pada lingkungan deployment."),
    ("paragraph", "4. Uji Coba Testnet & Rilis Bertahap: Vault telah beroperasi stabil tanpa anomali di testnet publik selama minimal dua minggu, dilanjutkan peluncuran awal mainnet secara bertahap (canary launch) dengan pembatasan batas atas total nilai terkunci (deposit cap).")
]

# ==============================================================================
# KASUS 4
# ==============================================================================
ANSWERS["4.1"] = [
    ("paragraph", "A. Metode Rekonstruksi Aliran Dana:"),
    ("paragraph", "Rekonstruksi aliran dana lintas jaringan dilakukan melalui pendekatan analisis graf transaksi terarah (Directed Acyclic Graph / DAG), di mana alamat bertindak sebagai node dan transfer aset bertindak sebagai edge:"),
    ("paragraph", "1. Pelacakan Percabangan (Fan-Out Tracing): Menelusuri seluruh transaksi keluar dari alamat eksploitasi awal A menuju enam alamat perantara untuk memetakan skema pemecahan dana (layering)."),
    ("paragraph", "2. Dekonvolusi Interaksi DEX: Menganalisis interaksi pertukaran token pada smart contract Decentralized Exchange (DEX) dengan membedah log event (Swap, Transfer, Sync) untuk mengidentifikasi token input, token output, nilai kurs, slippage, serta alamat penerima hasil penukaran."),
    ("paragraph", "3. Pelacakan Lintas Rantai (Cross-Chain Bridge Tracing): Menghubungkan peristiwa penguncian/pembakaran aset (event Deposit/Lock/Burn) pada kontrak bridge rantai asal dengan peristiwa pencetakan/pelepasan aset (event Withdraw/Mint/Unlock) pada rantai tujuan, dengan mencocokkan parameter penaut seperti nonce transaksi, hash pesan lintas rantai, timestamp, dan nominal aset."),
    ("paragraph", "4. Penelusuran Titik Akhir (Egress Tracing): Mengikuti pergerakan dana hingga mencapai alamat deposit bursa terpusat (CEX) atau protokol mixing."),
    ("paragraph", "B. Artefak On-Chain yang Harus Dikumpulkan:"),
    ("paragraph", "- Data Identifikasi Transaksi: Transaction hash, nomor blok (block height), indeks transaksi, dan timestamp blok (presisi UTC).\n- Entitas Alamat: Alamat pengirim (from), alamat penerima (to), dan alamat penandatangan (origin).\n- Alamat Kontrak Terlibat: Alamat smart contract token ERC-20, router DEX, contract pool likuiditas, dan bridge gateway.\n- Log Event dan Topik: Log event mentah beserta topic terindeks (Topic 0 sebagai signature event, Topic 1–3 untuk pengirim/penerima terindeks) dan data heksadesimal unindexed yang memuat nilai transfer.\n- Jejak Panggilan Internal (Internal Call Traces): Trace call internal (Parity/Geth debug trace) untuk mendeteksi transfer aset yang terjadi di dalam eksekusi kontrak pintar tanpa memicu transaksi eksternal langsung.\n- Status dan Bukti Resi: Status receipt transaksi (success/fail) dan konsumsi gas fee.")
]

ANSWERS["4.2"] = [
    ("paragraph", "Evaluasi kekuatan dan keterbatasan dari ketiga heuristik analisis blockchain:"),
    ("paragraph", "1. Heuristik Common-Input Ownership:\n- Kekuatan: Sangat tangguh pada model UTXO (seperti Bitcoin), di mana penggabungan beberapa input yang ditandatangani dalam satu transaksi membuktikan secara kuat bahwa seluruh alamat input tersebut dikuasai oleh satu entitas yang sama (kecuali pada transaksi CoinJoin).\n- Keterbatasan: Heuristik ini tidak berlaku secara langsung pada jaringan berbasis akun (Account-based model) seperti Ethereum/EVM, karena setiap transaksi hanya memiliki satu alamat pengirim tunggal (msg.sender). Pada model akun, investigator harus mengandalkan heuristik padanan, seperti ketergantungan sumber pendanaan gas fee awal yang sama (common gas funding address) atau penandatangan bersama pada kontrak multisig."),
    ("paragraph", "2. Clustering Waktu (Temporal Analysis):\n- Kekuatan: Efektif dalam mendeteksi eksekusi terkoordinasi dan otomatisasi berbasis skrip bot, seperti pemecahan dana dari alamat A ke enam alamat perantara yang terjadi dalam blok yang sama atau selang detik yang sangat berdekatan.\n- Keterbatasan: Rentan menghasilkan kesimpulan keliru (false positive) pada kondisi kemacetan jaringan atau jam sibuk transaksi global. Selain itu, penyerang profesional dapat mengelabui heuristik ini dengan sengaja menyetel jeda waktu acak (randomized delay) dan memecah transaksi lintas hari/minggu."),
    ("paragraph", "3. Hubungan Alamat Deposit (Deposit Address Clustering):\n- Kekuatan: Heuristik paling kuat untuk menghubungkan pergerakan on-chain dengan entitas layanan dunia nyata (atribusi layanan). Setiap alamat deposit unik yang diterbitkan oleh bursa terpusat (CEX) secara berkala akan mengalirkan/menyapu (sweep) dananya ke hot wallet utama milik CEX tersebut. Hubungan penyapuan ini memberikan kepastian tinggi mengenai identitas platform bursa yang digunakan.\n- Keterbatasan: Hubungan ini hanya membuktikan identitas layanan perantara, bukan identitas pemilik rekening. Peretas sering kali memanfaatkan identitas palsu, akun curian (mule accounts), atau bursa tanpa kepatuhan KYC ketat untuk mengaburkan pemilik manfaat akhir (ultimate beneficial owner).")
]

ANSWERS["4.3"] = [
    ("paragraph", "Untuk memastikan integritas, keabsahan, dan penerimaan bukti digital di ranah hukum maupun audit forensik, disusun prosedur Chain of Custody yang mencakup bukti on-chain dan data pendukung off-chain:"),
    ("paragraph", "1. Identifikasi dan Dokumentasi Sumber Akuisisi:\nMendokumentasikan secara rinci metadata penarikan bukti: endpoint JSON-RPC yang digunakan, versi node client, block height, rentang blok, penyedia penjelajah blok (Etherscan API), serta tanggal dan waktu penarikan presisi UTC."),
    ("paragraph", "2. Hashing Kriptografis dan Integritas Seketika:\nSegera setelah data on-chain mentah (raw JSON response, transaction receipt, event logs, trace data) dan data pendukung off-chain (dokumen spesifikasi bridge, log transaksi CEX, screenshot penjelajah blok) diekstraksi, lakukan kalkulasi nilai hash kriptografis SHA-256 pada masing-masing berkas bukti digital. Catat nilai hash tersebut ke dalam Berita Acara Pengambilan Bukti."),
    ("paragraph", "3. Pemisahan Master Copy dan Working Copy:\nSimpan salinan asli (Master Copy) dalam media penyimpanan fisik terenkripsi berstatus write-once-read-many (WORM) atau repositori cloud dengan akses baca-saja (read-only). Seluruh proses rekonstruksi aliran dana, penguraian ABI, dan visualisasi graf hanya boleh dilakukan pada salinan kerja (Working Copy)."),
    ("paragraph", "4. Buku Log Rantai Penjagaan (Evidence Log Sheet):\nMencatat rekam jejak setiap interaksi fisik dan logis terhadap berkas bukti: tanggal/waktu, nama lengkap investigator, tindakan yang dilakukan (analisis, parsing, visualisasi), lokasi penyimpanan, serta verifikasi ulang hash SHA-256 sebelum dan sesudah analisis guna memastikan tidak terjadi perubahan byte data sedikit pun."),
    ("paragraph", "5. Pengamanan dan Reprodusibilitas Metodologi:\nMenyimpan skrip otomatisasi ekstraksi (misal skrip Python/Web3.py) dan mencatat versi pustaka piranti lunak yang digunakan. Hal ini menjamin bahwa pihak penguji independen atau pengadilan dapat menjalankan ulang metodologi tersebut dan memperoleh hasil rekonstruksi yang identik (reproducible).")
]

ANSWERS["4.4"] = [
    ("paragraph", "Berdasarkan hasil rekonstruksi on-chain dan pembuktian digital, ditarik kesimpulan investigatif dengan membedakan secara tegas tiga tingkatan atribusi:"),
    ("paragraph", "1. Atribusi Alamat (Keyakinan: Pasti / Bukti Keras On-Chain):\nTercatat secara deterministik pada buku besar publik bahwa alamat A mengeksekusi transfer aset hasil eksploitasi ke enam alamat perantara, melakukan konversi token melalui kontrak DEX, memindahkan dana lintas jaringan via bridge gateway, dan salah satu alamat meneruskan dana ke alamat penerima akhir 0xDeposit... Fakta perpindahan aset antarnode alamat ini terbukti secara matematis dan abadi."),
    ("paragraph", "2. Atribusi Layanan (Keyakinan: Sedang hingga Tinggi / Berbasis Pola Perilaku On-Chain):\nBerdasarkan analisis interaksi transaksi penyapuan saldo (sweeping transfer) dari alamat 0xDeposit... menuju hot wallet utama yang teridentifikasi secara publik, alamat tersebut diduga kuat merupakan alamat deposit milik bursa terpusat (Centralized Exchange / CEX) tertentu."),
    ("paragraph", "3. Atribusi Individu (Keyakinan: Belum Terbukti / Membutuhkan Data Hukum Off-Chain):\nIdentitas hukum atau individu pengendali alamat A dan rekening penampung di bursa belum dapat disimpulkan. Mengidentifikasi pelaku secara personal memerlukan proses penegakan hukum formal (surat panggilan / subpoena) kepada pihak bursa terkait untuk membuka rekaman Know Your Customer (KYC), log alamat IP login, data perangkat, dan riwayat rekening bank penarikan fiat yang terhubung.")
]

# Print word count check for each answer
print("=== WORD COUNT REPORT ===")
case_words = {"Kasus 1": 0, "Kasus 2": 0, "Kasus 3": 0, "Kasus 4": 0}

for q_id in sorted(ANSWERS.keys()):
    total_q_words = 0
    for item_type, content, *rest in ANSWERS[q_id]:
        if item_type == "paragraph":
            total_q_words += count_words(content)
    case_num = f"Kasus {q_id[0]}"
    case_words[case_num] += total_q_words
    print(f"Soal {q_id}: {total_q_words} kata")

for c_name, count in case_words.items():
    print(f"Total {c_name}: {count} kata")
print("Total Keseluruhan:", sum(case_words.values()), "kata")
