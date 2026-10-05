#!/usr/bin/env python3
"""
build_v6.py
Script to generate Laporan_UTS_Blockchain_237006079_v6.docx from Laporan_UTS_Blockchain_237006079.docx
applying all corrections requested by user:
1. Numbered table captions for Tables 1 through 13 in sequential order.
2. Fix all cross-references to point to the correct table number.
3. Update footer: "Laporan UTS Blockchain | TA 2026/2027".
4. Remove "Case n" labels from headings 4.1 - 4.5 and tables.
5. Explicitly state roles of 4.4 and 4.5 towards P2, P3, P5.
6. Update hardware specs to match verified lscpu / free / uname output.
7. Tone down excessive claims (legal, security, local scope) and accurately cite UU PDP (Pasal 8, 9, 43) & Permendikbudristek No. 6/2022 [13].
8. Add reference [13] to Daftar Pustaka.
9. Ensure Diagram 1, 2, 3 and Tabel 1-13 match `^(Tabel|Gambar|Diagram) [0-9]+` cleanly in pdftotext.
"""

import docx
from docx.shared import Pt, RGBColor
import subprocess
import os
import re

SRC_DOCX = "uts-blockchain-submission/Laporan_UTS_Blockchain_237006079.docx"
OUT_DOCX = "uts-blockchain-submission/Laporan_UTS_Blockchain_237006079_v6.docx"
OUT_PDF = "uts-blockchain-submission/Laporan_UTS_Blockchain_237006079_v6.pdf"
SUBMISSION_PDF = "uts-blockchain-submission/237006079_Fajar_Geran_Arifin_UTS_Blockchain_OBE.pdf"

doc = docx.Document(SRC_DOCX)

# 1. UPDATE FOOTER
for sec in doc.sections:
    footer = sec.footer
    for p in footer.paragraphs:
        if "Template Laporan Kegiatan Blockchain" in p.text:
            p.text = "Laporan UTS Blockchain | TA 2026/2027"

# 2. UPDATE HEADINGS (REMOVE "Case n") & EXPLAIN ROLES TO P1-P6
heading_fixes = {
    "4.1 Analisis Kelayakan, Pemangku Kepentingan, dan Arsitektur Jaringan (P1, P2 / Case 1)":
        "4.1 Analisis Kelayakan, Pemangku Kepentingan, dan Arsitektur Jaringan (P1, P2)",
    "4.2 Kriptografi, W3C Verifiable Credentials, dan Integritas Daun Bergaram (P3 / Case 2)":
        "4.2 Kriptografi, W3C Verifiable Credentials, dan Integritas Daun Bergaram (P3)",
    "4.3 Jaringan P2P, Siklus Transaksi, dan Mekanisme Konsensus (P2, P3 / Case 3)":
        "4.3 Jaringan P2P, Siklus Transaksi, dan Mekanisme Konsensus (P2, P3)",
    "4.4 Evaluasi Model UTXO Bitcoin vs Account-Based State Registry (Case 4)":
        "4.4 Evaluasi Model Transaksi UTXO Bitcoin vs Account-Based State Registry (P2)",
    "4.5 Model Akun EVM, Analisis Ketat Komponen Gas, dan Model Regresi (P3, P5 / Case 5)":
        "4.5 Model Akun EVM, Analisis Ketat Komponen Gas, dan Model Regresi (P3, P5)"
}

for p in doc.paragraphs:
    t = p.text.strip()
    if t in heading_fixes:
        p.text = heading_fixes[t]

# 3. TEXT & CROSS-REFERENCE FIXES, TONE DOWN CLAIMS
for p in doc.paragraphs:
    # Heading 2 intro
    if "Untuk menjamin bahwa seluruh hasil observasi, angka konsumsi gas, dan waktu komputasi" in p.text:
        p.text = p.text.replace(
            "Untuk menjamin bahwa seluruh hasil observasi, angka konsumsi gas, dan waktu komputasi yang dilaporkan dalam dokumen ini dapat diuji ulang secara independen oleh dosen penguji maupun peneliti lain, seluruh konfigurasi perangkat keras, perangkat lunak, pustaka dependensi, dan perintah eksekusi dirangkum secara komprehensif pada rincian berikut:",
            "Untuk memastikan bahwa seluruh hasil observasi, angka konsumsi gas, dan waktu komputasi yang dilaporkan dalam dokumen ini dapat diuji ulang secara independen oleh dosen penguji maupun peneliti lain, seluruh konfigurasi perangkat keras, perangkat lunak, pustaka dependensi, dan perintah eksekusi dirangkum secara komprehensif pada Tabel 1:"
        )

    # Heading 3 intro
    if p.text.strip() == "3 Catatan Pelaksanaan":
        # We will add an introductory sentence right after heading 3
        pass

    # Table 3 intro
    if "melainkan dijamin oleh konsensus kriptografis terdistribusi." in p.text:
        p.text = p.text.replace(
            "melainkan dijamin oleh konsensus kriptografis terdistribusi.",
            "melainkan dijamin oleh konsensus kriptografis terdistribusi, sebagaimana dikomparasikan dalam Tabel 3."
        )

    # Table 4 intro
    if "seperti diilustrasikan pada Diagram 1." in p.text and "Tabel 4" not in p.text:
        p.text = p.text.replace(
            "seperti diilustrasikan pada Diagram 1.",
            "seperti diilustrasikan pada Diagram 1. Pembagian peran dan penempatan data dirangkum pada Tabel 4."
        )

    # Table 5 intro & UU PDP update in paragraph 42
    if "Standar W3C VC & Kepatuhan Hak Hapus:" in p.text or "Standar W3C VC & Keselarasan Hak Hapus:" in p.text:
        p.text = (
            "Standar W3C VC & Keselarasan Hak Hapus: Kanonikalisasi JSON yang mengacu pada RFC 8785 [9] "
            "memastikan bahwa susunan kunci atribut kamus selalu deterministik secara byte-level di seluruh platform sistem operasi. "
            "Standar W3C Verifiable Credentials Data Model v2.0 [1] mendefinisikan mekanisme credentialStatus untuk memeriksa "
            "keabsahan dokumen; penjangkaran status melalui Merkle Root on-chain [4] merupakan pilihan desain arsitektur pada prototipe ini. "
            "Desain arsitektur Zero-PII ini dirancang selaras dengan prinsip pelindungan data pribadi pada UU No. 27 Tahun 2022 (UU PDP) [10], "
            "khususnya klasifikasi data pribadi umum (nama lengkap) pada Pasal 8, hak pemusnahan/penghapusan subjek data pada Pasal 9, "
            "serta kewajiban pengendali data untuk melakukan penghapusan data pribadi pada Pasal 43 ayat (1) huruf c: "
            "jika alumni mengajukan hak penghapusan data, universitas dan alumni cukup memusnahkan dokumen lokal dan nilai salt, "
            "sehingga daun hash pada blockchain menjadi artefak komputasi acak semu yang mustahil direkonstruksi kembali (cryptographic erasure). "
            "Struktur data record daun dan injeksi salt ini dirangkum dalam Tabel 5."
        )

    # Table 6 intro in paragraph 50
    if "menghasilkan empat keunggulan operasional utama:" in p.text or "Analisis Fork & Pemilihan Konsensus:" in p.text:
        if "Tabel 6" not in p.text and "Istanbul / Quorum Byzantine Fault Tolerance" in p.text:
            p.text = p.text.replace(
                "empat keunggulan operasional utama:",
                "empat keunggulan operasional utama, sebagaimana dirangkum dalam Tabel 6:"
            )

    # Subchapter 4.4 role clarification & Table 7 intro
    if "Analisis Model UTXO: Model transaksi Unspent Transaction Output (UTXO)" in p.text:
        p.text = (
            "Keterkaitan dengan P2 & Evaluasi Model UTXO: Dalam memenuhi luaran P2 (justifikasi pemilihan arsitektur), "
            "evaluasi terhadap model transaksi Unspent Transaction Output (UTXO) pada arsitektur Bitcoin penting untuk membuktikan "
            "mengapa arsitektur blockchain berbasis akun dipilih. Model UTXO beroperasi atas dasar perpindahan kepemilikan nilai diskrit "
            "(Input -> Transaksi -> Output + Change). Pencegahan double spending pada UTXO dijamin oleh aturan bahwa suatu koin output "
            "hanya dapat dikonsumsi tepat satu kali sebagai input transaksi baru. Meskipun sangat kuat untuk transfer mata uang kripto, "
            "model UTXO memiliki keterbatasan struktural apabila diterapkan pada sistem registri status kredensial akademik publik, "
            "sebagaimana dirangkum dalam Tabel 7."
        )

    # Subchapter 4.5 role clarification & Table 8 intro
    if "EVM mengkategorikan akun ke dalam dua entitas:" in p.text:
        p.text = (
            "Keterkaitan dengan P3, P5 & Model Akun EVM: Untuk memenuhi luaran P3 (desain smart contract) dan P5 (analisis performa gas mendalam), "
            "subbab ini membedah model komputasi akun EVM. EVM mengkategorikan akun ke dalam dua entitas: Externally Owned Account (EOA) yang dikendalikan oleh "
            "pasangan kunci privat/publik kurva secp256k1, dan Contract Account yang dikendalikan oleh kode bytecode tersimpan. "
            "Komposisi field transaksi issueBatch dan kueri verifikasi dirangkum dalam Tabel 8."
        )

    # Table 9 intro in paragraph 63
    if "Perhitungan Ketat Komponen Gas issueBatch:" in p.text:
        p.text = (
            "Perhitungan Ketat Komponen Gas issueBatch: Sesuai prinsip eksekusi EVM, konsumsi gas transaksi tidak boleh dilaporkan "
            "secara mentah tanpa pemisahan komponen. Gas eksekusi murni internal kontrak dihitung dengan formula baku: "
            "Gas_Eksekusi = gasUsed (Receipt) - 21.000 (Intrinsic Tx) - Biaya_Calldata. Biaya calldata dihitung langsung dari payload "
            "tx.data aktual sesuai aturan EIP-2028 [11] (16 gas per byte non-nol dan 4 gas per byte nol), sebagaimana dirinci pada Tabel 9:"
        )

    # Calldata 84 gas claim softening
    if "Pembuktian Sumber Selisih Calldata 84 Gas:" in p.text:
        p.text = p.text.replace(
            "Pengukuran empiris membuktikan bahwa selisih gas sebesar 84 gas antara batch N=6 dan N=1.000 sama sekali bukan berasal dari eksekusi smart contract, melainkan murni dari akumulasi tiga parameter calldata ABI transaksi:",
            "Pengukuran empiris menunjukkan bahwa selisih gas sebesar 84 gas antara batch N=6 dan N=1.000 dapat dijelaskan secara deterministik melalui akumulasi tiga parameter calldata ABI transaksi:"
        )

    # Table 10 intro
    if "sebagaimana dirangkum dalam Matriks Ancaman STRIDE." in p.text:
        p.text = p.text.replace(
            "sebagaimana dirangkum dalam Matriks Ancaman STRIDE.",
            "sebagaimana dirangkum dalam Tabel 10 (Matriks Analisis Ancaman STRIDE)."
        )

    # Table 11 intro
    if "sebagaimana dirangkum dalam Tabel Kriteria Penerimaan." in p.text:
        p.text = p.text.replace(
            "sebagaimana dirangkum dalam Tabel Kriteria Penerimaan.",
            "sebagaimana dirangkum dalam Tabel 11."
        )

    # Table 12 intro
    if "sebagaimana dirangkum pada Tabel 9." in p.text:
        p.text = p.text.replace("Tabel 9.", "Tabel 12.")

    # Table 13 intro
    if "dirangkum pada Tabel B-08." in p.text:
        p.text = p.text.replace("Tabel B-08.", "Tabel 13.")

    # Hardware specs in limitation section
    if "Intel Core i5-12450H, 16 GB RAM" in p.text:
        p.text = p.text.replace(
            "workstation pengembang (Intel Core i5-12450H, 16 GB RAM)",
            "workstation pengembang (12th Gen Intel Core i5-12450H 12 vCPU, 16 GB RAM / 15 GiB tersedia, Ubuntu 24.04 LTS x86_64, Node.js v24.14.0)"
        )

    # Soften claims in Paragraph 6 (Executive Summary)
    if "kriteria kelayakan performa dan keamanan terbukti berhasil dipenuhi" in p.text:
        p.text = p.text.replace(
            "kriteria kelayakan performa dan keamanan terbukti berhasil dipenuhi, membuktikan kelayakan implementasi",
            "kriteria kelayakan performa dan keamanan pada lingkungan uji ini berhasil dipenuhi, menunjukkan kelayakan implementasi"
        )
    if "guna menjamin hak penghapusan data pribadi (Right to Erasure, Pasal 8 dan Pasal 43 UU PDP No. 27/2022)" in p.text:
        p.text = p.text.replace(
            "guna menjamin hak penghapusan data pribadi (Right to Erasure, Pasal 8 dan Pasal 43 UU PDP No. 27/2022) [10]",
            "guna mendukung keselarasan dengan hak pemusnahan/penghapusan data pribadi (Right to Erasure, Pasal 8, Pasal 9, dan Pasal 43 UU PDP No. 27/2022) [10]"
        )
    if "terbukti secara matematis berasal dari akumulasi parameter calldata EIP-2028 [11]" in p.text:
        p.text = p.text.replace(
            "terbukti secara matematis berasal dari akumulasi parameter calldata EIP-2028 [11]",
            "dapat dijelaskan secara matematis melalui akumulasi parameter calldata EIP-2028 [11]"
        )

    # Soften entropy / test data claims
    if "guna menjamin sifat unik daun komitmen tanpa kebocoran entropi." in p.text:
        p.text = p.text.replace(
            "guna menjamin sifat unik daun komitmen tanpa kebocoran entropi.",
            "guna menjaga keunikan daun komitmen tanpa kebocoran entropi."
        )
    if "guna menjamin tidak adanya data pribadi riil yang terpapar selama proses riset." in p.text:
        p.text = p.text.replace(
            "guna menjamin tidak adanya data pribadi riil yang terpapar selama proses riset.",
            "untuk memastikan tidak adanya data pribadi riil yang terpapar selama proses riset."
        )

    # Soften metadataURI storage claim
    if "Gas eksekusi transaksi issueBatch terbukti konstan (164.911 gas)" in p.text:
        p.text = p.text.replace(
            "Gas eksekusi transaksi issueBatch terbukti konstan (164.911 gas)",
            "Gas eksekusi transaksi issueBatch terukur konstan (164.911 gas)"
        )

    # Soften Kesimpulan claims
    if "terbukti konstan secara eksak sebesar 164.911 gas (deviasi 0,0000%, true O(1))" in p.text:
        p.text = p.text.replace(
            "terbukti konstan secara eksak sebesar 164.911 gas (deviasi 0,0000%, true O(1)) untuk seluruh variasi ukuran batch",
            "terukur konstan secara eksak sebesar 164.911 gas (deviasi 0,0000%, true O(1)) pada lingkungan uji ini untuk seluruh variasi ukuran batch"
        )
    if "Selisih 84 gas pada tanda terima transaksi (receipt) terbukti 100% bersumber dari" in p.text:
        p.text = p.text.replace(
            "Selisih 84 gas pada tanda terima transaksi (receipt) terbukti 100% bersumber dari penambahan panjang parameter calldata ABI transaksi",
            "Selisih 84 gas pada tanda terima transaksi (receipt) dapat dijelaskan secara deterministik melalui penambahan panjang parameter calldata ABI transaksi"
        )
    if "selisih 84 gas sepenuhnya berasal dari biaya intrinsik calldata" in p.text:
        p.text = p.text.replace(
            "selisih 84 gas sepenuhnya berasal dari biaya intrinsik calldata",
            "selisih 84 gas secara deterministik berasal dari biaya intrinsik calldata"
        )

    # Permendikbudristek & UU PDP in Section 4.7 roadmap
    if "Pertimbangan Etika, Regulasi, & Roadmap:" in p.text:
        p.text = (
            "Pertimbangan Etika, Regulasi, & Roadmap: Implementasi sistem ini menegakkan prinsip keadilan sosial dan non-diskriminasi. "
            "Biaya verifikasi yang ditetapkan 0 gas dirancang agar lulusan dari keluarga prasejahtera dan instansi UMKM/pemberi kerja "
            "lokal dapat memverifikasi keabsahan dokumen tanpa hambatan finansial [2]. "
            "Secara regulasi, desain arsitektur sistem dirancang selaras dengan prinsip keterverifikasian dokumen akademik pada "
            "Peraturan Menteri Pendidikan, Kebudayaan, Riset, dan Teknologi No. 6 Tahun 2022 tentang Ijazah, Sertifikat Kompetensi, "
            "Sertifikat Profesi, Gelar, dan Kesetaraan Ijazah Perguruan Tinggi Negara Lain [13], "
            "serta dirancang selaras dengan perlindungan hak privasi alumni di bawah naungan UU No. 27 Tahun 2022 (UU PDP) [10]. "
            "Roadmap pengembangan masa depan mencakup integrasi skema W3C Bitstring Status List v1.0 [8] untuk kompresi pencabutan tingkat lanjut "
            "dan penerapan Zero-Knowledge Proofs (BBS+ Signatures) untuk Selective Disclosure (misal membuktikan 'IPK >= 3.50' tanpa membuka angka IPK eksak)."
        )

    # Kesimpulan 1
    if "Sistem verifikasi kredensial akademik berbasis blockchain konsorsium permissioned (Hyperledger Besu / EVM) dan pohon Merkle terbukti layak" in p.text:
        p.text = p.text.replace(
            "terbukti layak (feasible), aman, dan sangat terukur",
            "pada lingkungan uji ini menunjukkan kelayakan teknis (feasible), keandalan kontrol akses, dan skalabilitas yang tinggi"
        )

    # Kesimpulan 2
    if "berhasil menjamin kepatuhan penuh terhadap hak penghapusan data pribadi (Right to Erasure, Pasal 8 dan Pasal 43 UU PDP No. 27/2022)" in p.text:
        p.text = p.text.replace(
            "berhasil menjamin kepatuhan penuh terhadap hak penghapusan data pribadi (Right to Erasure, Pasal 8 dan Pasal 43 UU PDP No. 27/2022) [10]",
            "dirancang selaras dengan pemenuhan hak penghapusan data pribadi (Pasal 8, Pasal 9, dan Pasal 43 UU PDP No. 27/2022) [10]"
        )

    # Kesimpulan 5
    if "Keamanan sistem terbukti tangguh melalui penolakan seketika" in p.text:
        p.text = p.text.replace(
            "Keamanan sistem terbukti tangguh melalui penolakan seketika",
            "Pada lingkungan uji ini, mekanisme keamanan smart contract menunjukkan ketahanan melalui penolakan seketika"
        )

# 4. UPDATE CLAIMS & VALUES IN TABLES
# Table 2: Catatan Pelaksanaan (doc.tables[2])
t2 = doc.tables[2]
# Row 2 (Tahap 2): Include B-01 gas
t2.rows[2].cells[2].text = "Kontrak aktif di alamat 0x5FbDB2315678afecb367f032d93F642f64180aa3, Tx: 0x145b5523..., Gas: 1.039.368 unit [B-01]"
# Row 4 (Tahap 4): Include B-06 and B-07 gas
t2.rows[4].cells[2].text = (
    "Root terdaftar Block #2 tx 0x1737c359... [B-03]; verifikasi valid 0 gas [B-04]; "
    "manipulasi ditolak [B-05A/B]; cabut ijazah (Gas: 56.359 unit) [B-06]; "
    "jeda darurat pause (Gas: 48.214 unit) [B-07], Tabel 8, Tabel 10, Tabel 12"
)
# Row 5 (Tahap 5): Ensure wrap doesn't create standalone 'Tabel 11'
t2.rows[5].cells[2].text = (
    "Gas eksekusi murni issueBatch konstan 164.911 gas (O(1)), bukti selisih calldata deterministik tepat 84 gas, "
    "model kelayakan verifikasi linear 7.800 + 251*k gas, kueri publik 0 gas. "
    "Rujukan: B-08, Tabel 9, Tabel 11, Tabel 13 (results/perf-output.txt)"
)

# Table 3: Claims in Table 3
t3 = doc.tables[3]
for r in t3.rows:
    for c in r.cells:
        if "Mencegah single point of failure dan menjamin ketersediaan verifikasi" in c.text:
            c.text = c.text.replace("menjamin ketersediaan", "mendukung ketersediaan")
        if "menjamin biaya penjangkaran O(1) konstan" in c.text:
            c.text = c.text.replace("menjamin biaya penjangkaran", "menghasilkan biaya penjangkaran")

# Table 4: Table 4 privacy compliance
t4 = doc.tables[4]
for r in t4.rows:
    for c in r.cells:
        if "Kepatuhan terhadap Pasal 8 dan Pasal 43 UU PDP [10]" in c.text:
            c.text = c.text.replace("Kepatuhan terhadap Pasal 8 dan Pasal 43 UU PDP [10]", "Selaras dengan Pasal 8, 9, dan 43 UU PDP [10]")

# Table 7: Remove [Kasus 4]
t7 = doc.tables[7]
for r in t7.rows:
    for c in r.cells:
        if "[Kasus 4]" in c.text:
            c.text = c.text.replace("[Kasus 4]", "Evaluasi UTXO:")

# Table 11: Tone down claims in criteria table
t11 = doc.tables[11]
for r in t11.rows:
    for c in r.cells:
        if "selisih gas transaksi riil terbukti murni berasal dari payload calldata ABI" in c.text:
            c.text = c.text.replace(
                "selisih gas transaksi riil terbukti murni berasal dari payload calldata ABI",
                "selisih gas transaksi riil pada pengujian ini terbukti bersumber dari payload calldata ABI"
            )

# 5. ADD PERMENDIKBUDRISTEK NO. 6/2022 TO DAFTAR PUSTAKA
p12_idx = -1
for i, p in enumerate(doc.paragraphs):
    if p.text.strip().startswith("[12]"):
        p12_idx = i
        break

if p12_idx != -1:
    has_13 = any(p.text.strip().startswith("[13]") for p in doc.paragraphs)
    if not has_13:
        p13 = doc.add_paragraph()
        p13.text = (
            '[13] Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi Republik Indonesia, '
            '"Peraturan Menteri Pendidikan, Kebudayaan, Riset, dan Teknologi Republik Indonesia Nomor 6 Tahun 2022 '
            'tentang Ijazah, Sertifikat Kompetensi, Sertifikat Profesi, Gelar, dan Kesetaraan Ijazah Perguruan Tinggi Negara Lain," '
            'Berita Negara Republik Indonesia Tahun 2022 Nomor 168, Jakarta, Feb. 2022. [Daring]. Tersedia: '
            'https://peraturan.bpk.go.id/Details/204859/permendikbudristek-no-6-tahun-2022. [Diakses: 4 Oktober 2026].'
        )
        p13.paragraph_format.space_before = Pt(3)
        p13.paragraph_format.space_after = Pt(3)
        for r in p13.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(8.5)
        doc.paragraphs[p12_idx]._element.addnext(p13._element)

# 6. INSERT NUMBERED TABLE CAPTIONS (TABLES 1 THROUGH 13)
captions = {
    1: "Tabel 1. Komponen Lingkungan Pengujian dan Reproduksibilitas Sistem",
    2: "Tabel 2. Catatan Pelaksanaan Mini-Project Perancangan Sistem Blockchain",
    3: "Tabel 3. Perbandingan Karakteristik Basis Data Terpusat vs Blockchain Konsorsium",
    4: "Tabel 4. Partisi Komponen Data On-Chain vs Off-Chain dan Kepatuhan Privasi",
    5: "Tabel 5. Struktur Data Record Daun Merkle Kredensial Akademik Uji Coba",
    6: "Tabel 6. Analisis Komparatif Mekanisme Konsensus Terdistribusi",
    7: "Tabel 7. Evaluasi Transaksi Berbasis UTXO Bitcoin dan Batasan OP_RETURN",
    8: "Tabel 8. Parameter Field Transaksi Penjangkaran EVM pada Node Lokal",
    9: "Tabel 9. Rincian Komponen Konsumsi Gas Transaksi issueBatch (N = 6, 100, 1.000)",
    10: "Tabel 10. Matriks Analisis Ancaman STRIDE dan Kontrol Mitigasi Sistem",
    11: "Tabel 11. Evaluasi Kriteria Penerimaan dan Ketercapaian Luaran OBE",
    12: "Tabel 12. Ringkasan Hasil Eksekusi Pengujian Unit Test Otomatis (T-01 s.d. T-08)",
    13: "Tabel 13. Rekapitulasi Metrik Pengujian Performa 30 Run Terukur"
}

for idx, cap_text in captions.items():
    t = doc.tables[idx]
    p = doc.add_paragraph()
    p.text = cap_text
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    for r in p.runs:
        r.font.name = 'Arial'
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
    t._element.addprevious(p._element)

# 7. INTRODUCTORY SENTENCE FOR HEADING 3 (BEFORE TABEL 2)
for i, p in enumerate(doc.paragraphs):
    if p.text.strip() == "3 Catatan Pelaksanaan":
        p_intro = doc.add_paragraph()
        p_intro.text = "Pelaksanaan mini-project perancangan dan evaluasi sistem verifikasi kredensial akademik berbasis blockchain konsorsium ini dirangkum dalam Tabel 2."
        p_intro.paragraph_format.space_before = Pt(2)
        p_intro.paragraph_format.space_after = Pt(4)
        for r in p_intro.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(9)
        p._element.addnext(p_intro._element)
        break

# 8. LAYOUT OPTIMIZATION (PREVENT ORPHAN DIAGRAM CAPTIONS & STANDALONE TOP-OF-PAGE \x0c)
# Keep Diagram images with their captions
for i, p in enumerate(doc.paragraphs):
    if "Diagram 1:" in p.text or "Diagram 2:" in p.text or "Diagram 3:" in p.text:
        p.paragraph_format.keep_with_next = True
        # also set keep_with_next on previous paragraph (image container)
        if i > 0:
            doc.paragraphs[i-1].paragraph_format.keep_with_next = True

# Also keep heading 4.7 with paragraph 81 so Tabel 11 has preceding text
for p in doc.paragraphs:
    if p.text.strip().startswith("4.7 Implementasi Prototipe"):
        p.paragraph_format.keep_with_next = True
    if "sebagaimana dirangkum dalam Tabel 11." in p.text:
        p.paragraph_format.keep_with_next = True

# Save as v6
doc.save(OUT_DOCX)
print(f"v6 DOCX saved successfully to {OUT_DOCX}")

# Compile to PDF using LibreOffice
cmd = ["soffice", "--headless", "--convert-to", "pdf", OUT_DOCX, "--outdir", "uts-blockchain-submission"]
subprocess.run(cmd, check=True)

# Copy to final submission name
subprocess.run(["cp", OUT_PDF, SUBMISSION_PDF], check=True)
print(f"v6 PDF compiled successfully and synced to {SUBMISSION_PDF}")
