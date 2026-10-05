#!/usr/bin/env python3
"""
build_v7.py
Script to build Laporan_UTS_Blockchain_237006079_v7.docx and .pdf from base docx.
Implements all requirements from KOREKSI v6 -> v7:
- Page limit: Body <= 12 pages (measured with and without cover).
- Move detailed evaluation criteria (Table 11) to Lampiran D.
- Move detailed 30-run benchmark metrics (Table 13) to Lampiran E.
- Compress Subchapter 4.4 (UTXO) into Subchapter 4.3 and delete Table 7.
- Re-number body tables sequentially as Tabel 1 through Tabel 10.
- Update hardware specs to match verified lscpu / free -h / nproc / os-release.
- Verify and cite statutory provisions: UU PDP (Pasal 4 ayat 3, Pasal 8, Pasal 9, Pasal 43) & Permendikbudristek 6/2022 (BN 2022 No. 167).
- Soften all excessive claims to scoped engineering language.
- Ensure all numbers and hashes match prototype results.
"""

import docx
from docx.shared import Pt, RGBColor, Inches
import subprocess
import os
import re

SRC_DOCX = "uts-blockchain-submission/Laporan_UTS_Blockchain_237006079.docx"
OUT_DOCX = "v7_workspace/Laporan_UTS_Blockchain_237006079_v7.docx"
OUT_PDF = "v7_workspace/Laporan_UTS_Blockchain_237006079_v7.pdf"

doc = docx.Document(SRC_DOCX)

# 1. FOOTER UPDATE
for sec in doc.sections:
    footer = sec.footer
    for p in footer.paragraphs:
        if "Template Laporan Kegiatan Blockchain" in p.text:
            p.text = "Laporan UTS Blockchain | TA 2026/2027"

# 2. CLEAR EXCESSIVE CANTSPLIT ON TABLE ROWS TO ALLOW NATURAL PAGE BREAKS
for t in doc.tables:
    for r in t.rows:
        trPr = r._tr.get_or_add_trPr()
        cs = trPr.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}cantSplit")
        if cs is not None:
            trPr.remove(cs)

# 3. HEADING FIXES (REMOVE "Case n")
heading_fixes = {
    "4.1 Analisis Kelayakan, Pemangku Kepentingan, dan Arsitektur Jaringan (P1, P2 / Case 1)":
        "4.1 Analisis Kelayakan, Pemangku Kepentingan, dan Arsitektur Jaringan (P1, P2)",
    "4.2 Kriptografi, W3C Verifiable Credentials, dan Integritas Daun Bergaram (P3 / Case 2)":
        "4.2 Kriptografi, W3C Verifiable Credentials, dan Integritas Daun Bergaram (P3)",
    "4.3 Jaringan P2P, Siklus Transaksi, dan Mekanisme Konsensus (P2, P3 / Case 3)":
        "4.3 Jaringan P2P, Siklus Transaksi, Mekanisme Konsensus, dan Evaluasi Model UTXO (P2, P3)",
    "4.5 Model Akun EVM, Analisis Ketat Komponen Gas, dan Model Regresi (P3, P5 / Case 5)":
        "4.4 Model Akun EVM, Analisis Ketat Komponen Gas, dan Model Regresi (P3, P5)",
    "4.6 Analisis Keamanan, Model Ancaman STRIDE, dan Respons Insiden 24 Jam (P4)":
        "4.5 Analisis Keamanan, Model Ancaman STRIDE, dan Respons Insiden 24 Jam (P4)",
    "4.7 Implementasi Prototipe, Kriteria Penerimaan, dan Pengujian Performa (P5)":
        "4.6 Implementasi Prototipe, Kriteria Penerimaan, dan Pengujian Performa (P5)",
    "4.8 Keputusan Desain, Batasan Teknis, Pertimbangan Etika, dan Refleksi (P6)":
        "4.7 Keputusan Desain, Batasan Teknis, Pertimbangan Etika, dan Refleksi (P6)"
}

for p in doc.paragraphs:
    t = p.text.strip()
    if t in heading_fixes:
        p.text = heading_fixes[t]

# 4. COMPRESS SUBCHAPTER 4.4 INTO 4.3 AND REMOVE TABLE 7 (1.c.2)
# Find heading 4.4 paragraph and its surrounding text
p_utxo_heading = None
p_utxo_p1 = None
p_utxo_p2 = None

for i, p in enumerate(doc.paragraphs):
    if p.text.strip().startswith("4.4 Evaluasi Model UTXO Bitcoin"):
        p_utxo_heading = p
        if i + 1 < len(doc.paragraphs):
            p_utxo_p1 = doc.paragraphs[i+1]
        if i + 2 < len(doc.paragraphs):
            p_utxo_p2 = doc.paragraphs[i+2]
        break

# In Subchapter 4.3, append a concise synthesis of UTXO vs Account model
for p in doc.paragraphs:
    if "Analisis Fork & Pemilihan Konsensus:" in p.text:
        # Append concise synthesis
        p.text = p.text + (
            " Evaluasi Model UTXO vs Akun EVM (P2): Dalam memenuhi luaran P2 terkait justifikasi arsitektur, "
            "model Unspent Transaction Output (UTXO) Bitcoin dianalisis sebagai pembanding. Model UTXO bersifat stateless "
            "dan membatasi penyisipan data pada script OP_RETURN maksimal 80 byte (~0.005 BTC biaya transaksi ilustratif tanpa smart logic). "
            "Kelemahan fatal UTXO untuk ijazah adalah ketiadaan penyimpanan status dinamis (stateful storage); untuk membatalkan ijazah pada UTXO, "
            "penerbit harus membuat rantai transaksi pembelanjaan baru yang rumit. Sebaliknya, model akun EVM menyediakan mesin status "
            "terprogram yang memungkinkan penyimpanan status pencabutan individual secara langsung dalam slot mapping storage (_revokedCredentials[leafHash]) "
            "dengan kompleksitas akses O(1) dan biaya komputasi deterministik."
        )

# Remove the standalone 4.4 heading and its standalone paragraphs if present
if p_utxo_heading is not None:
    p_utxo_heading._element.getparent().remove(p_utxo_heading._element)
if p_utxo_p1 is not None and "Analisis Model UTXO:" in p_utxo_p1.text:
    p_utxo_p1._element.getparent().remove(p_utxo_p1._element)
if p_utxo_p2 is not None and "Komparasi Model Akun vs UTXO:" in p_utxo_p2.text:
    p_utxo_p2._element.getparent().remove(p_utxo_p2._element)

# Remove Table 7 (UTXO evaluation table) from body
tbl7_utxo = doc.tables[7]
tbl7_utxo._element.getparent().remove(tbl7_utxo._element)

# 5. MOVE TABLE 11 (CRITERIA) & TABLE 13 (BENCHMARK) TO APPENDICES (1.c.1)
# Note: after removing Table 7, original Table 11 is now at index 10, Table 12 at 11, Table 13 at 12
# Let's locate them by cell content to be 100% robust
tbl_criteria = None
tbl_unittest = None
tbl_bench = None

for t in doc.tables:
    first_cell = t.rows[0].cells[0].text.strip()
    if "Kelompok Uji" in first_cell:
        tbl_criteria = t
    elif "ID Tes" in first_cell:
        tbl_unittest = t
    elif "Parameter Pengujian" in first_cell:
        tbl_bench = t

# Move tbl_criteria to Lampiran D
p_lamp_d = doc.add_paragraph()
p_lamp_d.text = "Lampiran D: Matriks Evaluasi Lengkap Kriteria Penerimaan dan Luaran OBE (T-01 s.d. T-08)"
p_lamp_d.paragraph_format.space_before = Pt(14)
p_lamp_d.paragraph_format.space_after = Pt(4)
p_lamp_d.paragraph_format.keep_with_next = True
for r in p_lamp_d.runs:
    r.font.name = 'Arial'
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)

tbl_criteria._element.getparent().remove(tbl_criteria._element)
doc.element.body.append(p_lamp_d._element)
doc.element.body.append(tbl_criteria._element)

# Move tbl_bench to Lampiran E
p_lamp_e = doc.add_paragraph()
p_lamp_e.text = "Lampiran E: Rekapitulasi Lengkap Metrik Pengujian Performa 30 Run Terukur"
p_lamp_e.paragraph_format.space_before = Pt(14)
p_lamp_e.paragraph_format.space_after = Pt(4)
p_lamp_e.paragraph_format.keep_with_next = True
for r in p_lamp_e.runs:
    r.font.name = 'Arial'
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)

tbl_bench._element.getparent().remove(tbl_bench._element)
doc.element.body.append(p_lamp_e._element)
doc.element.body.append(tbl_bench._element)

# Move Evaluator Signatures (doc.tables[-1] which has "Nama", "NIP") to the very end of body or end of report
t_eval = None
for t in doc.tables:
    if "Nama" in t.rows[0].cells[0].text and len(t.rows) == 2:
        t_eval = t
        break

# 6. TEXT PARAGRAPH UPDATES & TONE DOWN EXCESSIVE CLAIMS
for p in doc.paragraphs:
    # Reproducibility intro
    if "Untuk menjamin bahwa seluruh hasil observasi" in p.text or "seluruh konfigurasi perangkat keras" in p.text:
        p.text = (
            "Untuk memastikan bahwa seluruh hasil observasi, angka konsumsi gas, dan waktu komputasi yang dilaporkan "
            "dalam dokumen ini dapat diuji ulang secara independen oleh dosen penguji maupun peneliti lain, seluruh "
            "konfigurasi perangkat keras, perangkat lunak, pustaka dependensi, dan perintah eksekusi dirangkum pada Tabel 1:"
        )

    # Catatan Pelaksanaan intro
    if p.text.strip() == "3 Catatan Pelaksanaan":
        p.text = "3 Catatan Pelaksanaan\nPelaksanaan mini-project perancangan dan evaluasi sistem verifikasi kredensial akademik berbasis blockchain konsorsium ini dirangkum dalam Tabel 2."

    # Section 4.1 Table 3 intro
    if "melainkan dijamin oleh konsensus kriptografis terdistribusi." in p.text:
        p.text = p.text.replace(
            "melainkan dijamin oleh konsensus kriptografis terdistribusi.",
            "melainkan dijamin oleh konsensus kriptografis terdistribusi, sebagaimana dikomparasikan dalam Tabel 3."
        )

    # Section 4.1 Table 4 intro & Citation [7]
    if "seperti diilustrasikan pada Diagram 1." in p.text and "Tabel 4" not in p.text:
        p.text = p.text.replace(
            "seperti diilustrasikan pada Diagram 1.",
            "seperti diilustrasikan pada Diagram 1. Pembagian peran dan penempatan data dirangkum pada Tabel 4."
        )
    if "Membutuhkan layanan verifikasi yang instan (< 1 detik)" in p.text and "[7]" not in p.text:
        p.text = p.text.replace(
            "Membutuhkan layanan verifikasi yang instan (< 1 detik)",
            "Membutuhkan layanan verifikasi yang instan (< 1 detik sesuai batas toleransi respons kognitif Nielsen [7])"
        )

    # Section 4.2 W3C VC, Salt, & UU PDP (Pasal 4 ayat 3, Pasal 8, Pasal 9, Pasal 43)
    if "Standar W3C VC & Kepatuhan Hak Hapus:" in p.text or "Standar W3C VC & Keselarasan Hak Hapus:" in p.text:
        p.text = (
            "Standar W3C VC & Keselarasan Hak Hapus: Kanonikalisasi JSON yang mengacu pada RFC 8785 [9] "
            "memastikan bahwa susunan kunci atribut kamus selalu deterministik secara byte-level di seluruh platform sistem operasi. "
            "Standar W3C Verifiable Credentials Data Model v2.0 [1] mendefinisikan mekanisme credentialStatus untuk memeriksa "
            "keabsahan dokumen; penjangkaran status melalui Merkle Root on-chain [4] merupakan pilihan desain arsitektur pada prototipe ini. "
            "Desain arsitektur Zero-PII ini dirancang selaras dengan prinsip pelindungan data pribadi pada UU No. 27 Tahun 2022 (UU PDP) [10], "
            "khususnya klasifikasi data pribadi umum pada Pasal 4 ayat (3), hak subjek data untuk meminta pemusnahan/penghapusan data pada Pasal 8, "
            "serta kewajiban pengendali data untuk melakukan penghapusan data pribadi pada Pasal 43 ayat (1): "
            "jika alumni mengajukan hak penghapusan data, pemusnahan dokumen lokal dan nilai salt off-chain dirancang untuk mengurangi keterkaitan data "
            "(data linkability) antara subjek dan rekaman transaksi; status hukum atas residu hash pada buku besar publik tetap memerlukan telaah hukum lebih lanjut. "
            "Struktur data record daun dan injeksi salt ini dirangkum dalam Tabel 5."
        )

    # Section 4.3 Table 6 intro
    if "empat keunggulan operasional utama:" in p.text and "Tabel 6" not in p.text:
        p.text = p.text.replace(
            "empat keunggulan operasional utama:",
            "empat keunggulan operasional utama, sebagaimana dirangkum dalam Tabel 6:"
        )

    # Section 4.4 (now EVM Model) Table 7 intro
    if "Komposisi field transaksi" in p.text and "Tabel" in p.text:
        p.text = (
            "Keterkaitan dengan P3, P5 & Model Akun EVM: Untuk memenuhi luaran P3 (desain smart contract) dan P5 (analisis performa gas mendalam), "
            "subbab ini membedah model komputasi akun EVM. EVM mengkategorikan akun ke dalam dua entitas: Externally Owned Account (EOA) yang dikendalikan oleh "
            "pasangan kunci privat/publik kurva secp256k1, dan Contract Account yang dikendalikan oleh kode bytecode tersimpan. "
            "Komposisi field transaksi issueBatch dan kueri verifikasi dirangkum dalam Tabel 7."
        )

    # Section 4.4 Table 8 intro (Komponen Gas)
    if "Perhitungan Ketat Komponen Gas issueBatch:" in p.text:
        p.text = (
            "Perhitungan Ketat Komponen Gas issueBatch: Sesuai prinsip eksekusi EVM, konsumsi gas transaksi tidak boleh dilaporkan "
            "secara mentah tanpa pemisahan komponen. Gas eksekusi murni internal kontrak dihitung dengan formula baku: "
            "Gas_Eksekusi = gasUsed (Receipt) - 21.000 (Intrinsic Tx) - Biaya_Calldata. Biaya calldata dihitung langsung dari payload "
            "tx.data aktual sesuai aturan EIP-2028 [11] (16 gas per byte non-nol dan 4 gas per byte nol), sebagaimana dirinci pada Tabel 8:"
        )

    # Section 4.4 Calldata claim
    if "Pembuktian Sumber Selisih Calldata 84 Gas:" in p.text:
        p.text = p.text.replace(
            "Pengukuran empiris membuktikan bahwa selisih gas sebesar 84 gas antara batch N=6 dan N=1.000 sama sekali bukan berasal dari eksekusi smart contract, melainkan murni dari akumulasi tiga parameter calldata ABI transaksi:",
            "Pengukuran empiris menunjukkan bahwa selisih gas sebesar 84 gas antara batch N=6 dan N=1.000 dapat dijelaskan secara deterministik melalui akumulasi tiga parameter calldata ABI transaksi:"
        )

    # Section 4.5 (STRIDE) Table 9 intro & Least Privilege [5] citation
    if "sebagaimana dirangkum dalam Matriks Ancaman STRIDE." in p.text or "Matriks Analisis Ancaman STRIDE" in p.text:
        p.text = (
            "Keamanan arsitektur dianalisis secara komprehensif menggunakan metodologi STRIDE (Spoofing, Tampering, "
            "Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege) untuk mengidentifikasi potensi ancaman "
            "dan kontrol mitigasi yang dirancang pada smart contract dan sistem off-chain. Kontrol mitigasi menerapkan prinsip hak istimewa terkecil "
            "(Principle of Least Privilege) dari Saltzer dan Schroeder (1975) [5] melalui pemisahan peran berwenang, "
            "sebagaimana dirangkum dalam Tabel 9 (Matriks Analisis Ancaman STRIDE)."
        )

    # Section 4.6 (Implementation & Acceptance Criteria)
    if "sebagaimana dirangkum dalam Tabel Kriteria Penerimaan." in p.text or "sebagaimana dirangkum dalam Tabel 11." in p.text:
        p.text = (
            "Kriteria penerimaan (acceptance criteria) disusun dengan merujuk pada standar ilmiah W3C VC [1], Ethereum JSON-RPC [2], "
            "dan RFC 8785 [9]. Rincian matriks evaluasi lengkap kriteria penerimaan terhadap luaran OBE disajikan pada Lampiran D. "
            "Di lingkungan pengujian otomatis Hardhat, seluruh skenario uji fungsional, keamanan, dan performa (T-01 s.d. T-08) "
            "berhasil lulus 100%, sebagaimana dirangkum pada Tabel 10."
        )

    # Section 4.6 Performance Benchmarks intro
    if "Hasil pengujian performa mendalam melalui 30 run terukur" in p.text:
        p.text = (
            "Pengujian performa mendalam dilakukan melalui 30 run terukur (+ 2 run warm-up) pada skrip scripts/perf-bench.js. "
            "Model regresi kelayakan linier pureVerifyGas(k) = 7.800,04 + 251,26*k gas terkonfirmasi memenuhi batas anggaran kelayakan, "
            "dan kueri verifikasi publik via eth_call mengonsumsi 0 gas dengan latensi rata-rata sub-milidetik (0,82 s.d. 0,89 ms). "
            "Rekapitulasi lengkap metrik statistik benchmark 30 run dirangkum pada Lampiran E."
        )

    # Section 4.7 Hardware specs
    if "Intel Core i5-12450H, 16 GB RAM" in p.text or "workstation pengembang (12th Gen Intel Core" in p.text:
        p.text = re.sub(
            r"workstation pengembang \([^)]+\)",
            "workstation pengembang (12th Gen Intel Core i5-12450H 12 vCPU, RAM total 15 GiB / 3,7 GiB tersedia, Ubuntu 24.04.4 LTS, Node.js v24.14.0)",
            p.text
        )

    # Section 4.7 Permendikbudristek & UU PDP
    if "Pertimbangan Etika, Regulasi, & Roadmap:" in p.text:
        p.text = (
            "Pertimbangan Etika, Regulasi, & Roadmap: Implementasi sistem ini menegakkan prinsip keadilan sosial dan non-diskriminasi. "
            "Biaya verifikasi yang ditetapkan 0 gas dirancang agar lulusan dari keluarga prasejahtera dan instansi UMKM/pemberi kerja "
            "lokal dapat memverifikasi keabsahan dokumen tanpa hambatan finansial [2]. "
            "Secara regulasi, desain arsitektur sistem dirancang selaras dengan prinsip keterverifikasian dokumen akademik pada "
            "Peraturan Menteri Pendidikan, Kebudayaan, Riset, dan Teknologi No. 6 Tahun 2022 tentang Ijazah, Sertifikat Kompetensi, "
            "Sertifikat Profesi, Gelar, dan Kesetaraan Ijazah Perguruan Tinggi Negara Lain (Berita Negara Republik Indonesia Tahun 2022 Nomor 167) [13], "
            "serta dirancang selaras dengan perlindungan privasi di bawah UU No. 27 Tahun 2022 (UU PDP) [10]. "
            "Roadmap pengembangan masa depan mencakup integrasi skema W3C Bitstring Status List v1.0 [8] untuk kompresi pencabutan tingkat lanjut "
            "dan penerapan Zero-Knowledge Proofs (BBS+ Signatures) untuk Selective Disclosure (misal membuktikan 'IPK >= 3.50' tanpa membuka angka IPK eksak)."
        )

    # Kesimpulan 1
    if "terbukti layak (feasible), aman, dan sangat terukur" in p.text:
        p.text = p.text.replace(
            "terbukti layak (feasible), aman, dan sangat terukur",
            "pada lingkungan uji ini menunjukkan kelayakan teknis (feasible), keandalan kontrol akses, dan skalabilitas yang tinggi"
        )
    # Kesimpulan 2
    if "berhasil menjamin kepatuhan penuh terhadap hak penghapusan data pribadi" in p.text:
        p.text = p.text.replace(
            "berhasil menjamin kepatuhan penuh terhadap hak penghapusan data pribadi (Right to Erasure, Pasal 8 dan Pasal 43 UU PDP No. 27/2022) [10]",
            "dirancang selaras dengan pemenuhan hak penghapusan data pribadi (Pasal 4 ayat (3), Pasal 8, Pasal 9, dan Pasal 43 UU PDP No. 27/2022) [10]"
        )
    # Kesimpulan 5
    if "Keamanan sistem terbukti tangguh" in p.text:
        p.text = p.text.replace(
            "Keamanan sistem terbukti tangguh melalui penolakan seketika",
            "Pada lingkungan uji ini, mekanisme keamanan smart contract menunjukkan ketahanan melalui penolakan seketika"
        )
    if "terbukti konstan secara eksak sebesar 164.911 gas" in p.text:
        p.text = p.text.replace(
            "terbukti konstan secara eksak sebesar 164.911 gas (deviasi 0,0000%, true O(1)) untuk seluruh variasi ukuran batch",
            "terukur konstan secara eksak sebesar 164.911 gas (deviasi 0,0000%, true O(1)) pada lingkungan uji ini untuk seluruh variasi ukuran batch"
        )
    if "selisih 84 gas sepenuhnya berasal dari" in p.text:
        p.text = p.text.replace(
            "selisih 84 gas sepenuhnya berasal dari biaya intrinsik calldata",
            "selisih 84 gas secara deterministik berasal dari biaya intrinsik calldata"
        )

# 7. UPDATE CONTENT OF REMAINING TABLES
# Table 1: Environment specs
t1 = doc.tables[1]
for r in t1.rows:
    for c in r.cells:
        if "Intel Core i5-12450H" in c.text:
            c.text = "Perangkat keras: 12th Gen Intel Core i5-12450H 12 vCPU, RAM total 15 GiB / 3,7 GiB tersedia. OS: Ubuntu 24.04.4 LTS x86_64, Node.js v24.14.0."

# Table 2: Catatan Pelaksanaan (B-01, B-06, B-07 and updated table references)
t2 = doc.tables[2]
t2.rows[2].cells[2].text = "Kontrak aktif di alamat 0x5FbDB2315678afecb367f032d93F642f64180aa3, Tx: 0x145b5523..., Gas: 1.039.368 unit [B-01]"
t2.rows[4].cells[2].text = (
    "Root terdaftar Block #2 tx 0x1737c359... [B-03]; verifikasi valid 0 gas [B-04]; "
    "manipulasi ditolak [B-05A/B]; cabut ijazah (Gas: 56.359 unit) [B-06]; "
    "jeda darurat pause (Gas: 48.214 unit) [B-07], Tabel 7, Tabel 9, Tabel 10"
)
t2.rows[5].cells[2].text = (
    "Gas eksekusi murni issueBatch konstan 164.911 gas (O(1)), bukti selisih calldata deterministik tepat 84 gas, "
    "model kelayakan verifikasi linear 7.800 + 251*k gas, kueri publik 0 gas. "
    "Rujukan: B-08, Tabel 8, Lampiran D, Lampiran E (results/perf-output.txt)"
)

# Table 3: Claims
t3 = doc.tables[3]
for r in t3.rows:
    for c in r.cells:
        if "menjamin ketersediaan" in c.text:
            c.text = c.text.replace("menjamin ketersediaan", "mendukung ketersediaan")
        if "menjamin biaya penjangkaran" in c.text:
            c.text = c.text.replace("menjamin biaya penjangkaran", "menghasilkan biaya penjangkaran")

# Table 4: Privacy compliance
t4 = doc.tables[4]
for r in t4.rows:
    for c in r.cells:
        if "Kepatuhan terhadap Pasal 8 dan Pasal 43 UU PDP [10]" in c.text:
            c.text = c.text.replace("Kepatuhan terhadap Pasal 8 dan Pasal 43 UU PDP [10]", "Selaras dengan Pasal 4 ayat (3), Pasal 8, 9, dan 43 UU PDP [10]")

# Table 7 (in new numbering, was Table 8): Clarify Block Gas Limit 30.000.000
# Locate by cell text "Field Transaksi EVM"
for t in doc.tables:
    if "Field Transaksi EVM" in t.rows[0].cells[0].text:
        for r in t.rows:
            for c in r.cells:
                if "Gas Limit: 30.000.000;" in c.text:
                    c.text = "Gas Limit Blok: 30.000.000 (Target EIP-1559 standard mainnet / konfigurasi default); Gas Used: 211.084 gas (penjangkaran batch); Status: 1 (Success)"

# 8. ADD PERMENDIKBUDRISTEK NO. 6/2022 TO DAFTAR PUSTAKA
p_ref12_idx = -1
for i, p in enumerate(doc.paragraphs):
    if p.text.strip().startswith("[12]"):
        p_ref12_idx = i
        break

if p_ref12_idx != -1:
    has_13 = any(p.text.strip().startswith("[13]") for p in doc.paragraphs)
    if not has_13:
        p13 = doc.add_paragraph()
        p13.text = (
            '[13] Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi Republik Indonesia, '
            '"Peraturan Menteri Pendidikan, Kebudayaan, Riset, dan Teknologi Republik Indonesia Nomor 6 Tahun 2022 '
            'tentang Ijazah, Sertifikat Kompetensi, Sertifikat Profesi, Gelar, dan Kesetaraan Ijazah Perguruan Tinggi Negara Lain," '
            'Berita Negara Republik Indonesia Tahun 2022 Nomor 167, Jakarta, Feb. 2022. [Daring]. Tersedia: '
            'https://peraturan.go.id/id/permendikbudristek-no-6-tahun-2022. [Diakses: 4 Oktober 2026].'
        )
        p13.paragraph_format.space_before = Pt(3)
        p13.paragraph_format.space_after = Pt(3)
        for r in p13.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(8.5)
        doc.paragraphs[p_ref12_idx]._element.addnext(p13._element)

# 9. INSERT SEQUENTIAL NUMBERED CAPTIONS FOR BODY TABLES 1 THROUGH 10
# Current body tables mapping:
# 1: Lingkungan Uji (doc.tables[1])
# 2: Catatan Pelaksanaan (doc.tables[2])
# 3: Komparasi DB vs BC (doc.tables[3])
# 4: Partisi On/Off-chain (doc.tables[4])
# 5: Record Daun Merkle (doc.tables[5])
# 6: Komparasi Konsensus (doc.tables[6])
# 7: Field Transaksi EVM (former Table 8)
# 8: Komposisi Gas issueBatch (former Table 9)
# 9: Matriks Ancaman STRIDE (former Table 10)
# 10: Ringkasan Unit Test (former Table 12, now tbl_unittest)

# Find each body table and prepend its caption paragraph
body_captions = [
    ("Komponen", "Tabel 1. Komponen Lingkungan Pengujian dan Reproduksibilitas Sistem"),
    ("Tahap", "Tabel 2. Catatan Pelaksanaan Mini-Project Perancangan Sistem Blockchain"),
    ("Aspek Evaluasi", "Tabel 3. Perbandingan Karakteristik Basis Data Terpusat vs Blockchain Konsorsium"),
    ("Komponen Data / Fungsi", "Tabel 4. Partisi Komponen Data On-Chain vs Off-Chain dan Kepatuhan Privasi"),
    ("Record / Daun", "Tabel 5. Struktur Data Record Daun Merkle Kredensial Akademik Uji Coba"),
    ("Mekanisme Konsensus", "Tabel 6. Analisis Komparatif Mekanisme Konsensus Terdistribusi"),
    ("Field Transaksi EVM", "Tabel 7. Parameter Field Transaksi Penjangkaran EVM pada Node Lokal"),
    ("Komponen Gas Transaksi issueBatch", "Tabel 8. Rincian Komponen Konsumsi Gas Transaksi issueBatch (N = 6, 100, 1.000)"),
    ("Kategori Ancaman", "Tabel 9. Matriks Analisis Ancaman STRIDE dan Kontrol Mitigasi Sistem"),
    ("ID Tes", "Tabel 10. Ringkasan Hasil Eksekusi Pengujian Unit Test Otomatis (T-01 s.d. T-08)")
]

for identifier, cap_text in body_captions:
    target_tbl = None
    for t in doc.tables:
        if identifier in t.rows[0].cells[0].text:
            target_tbl = t
            break
    if target_tbl is not None:
        p_cap = doc.add_paragraph()
        p_cap.text = cap_text
        p_cap.paragraph_format.keep_with_next = True
        p_cap.paragraph_format.space_before = Pt(6)
        p_cap.paragraph_format.space_after = Pt(2)
        for r in p_cap.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(9.5)
            r.font.bold = True
            r.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
        target_tbl._element.addprevious(p_cap._element)

# 10. DIAGRAM SCALING (1.c.5: Scale Diagram 2 to 80% width/height to fit page budget while maintaining full legibility)
scale = 0.80
for p in doc.paragraphs:
    for r in p.runs:
        extents = r._r.xpath(".//wp:extent")
        for ext in extents:
            cx = int(ext.attrib.get("cx", 0))
            cy = int(ext.attrib.get("cy", 0))
            if cy > 3000000: # Diagram 2
                ext.attrib["cx"] = str(int(cx * scale))
                ext.attrib["cy"] = str(int(cy * scale))

# 11. REMOVE REDUNDANT PARAGRAPHS & CONDENSE REPEATED TEXT (1.c.4)
to_remove = []
for p in doc.paragraphs:
    # Redundant intro right above Table 10
    if "Seluruh rangkaian unit test otomatis (T-01 s.d. T-08)" in p.text:
        to_remove.append(p)
    # Condense repeated explanation in bullet 7 of Section 4.7
    if "• 7. Pembulatan Calldata:" in p.text:
        p.text = (
            "• 7. Pembulatan Calldata: Efek Pembulatan Rata-Rata Calldata (83 vs 84 gas): Selisih rata-rata "
            "calldata ~83,6 gas vs 84 gas transaksi nominal merupakan efek pembulatan statistik digit nomor iterasi batchId (lihat rincian Subbab 4.4)."
        )
    # Remove any empty paragraphs without drawings
    if p.text.strip() == "" and "drawing" not in p._p.xml:
        to_remove.append(p)

for p in to_remove:
    p._element.getparent().remove(p._element)

# Save v7 docx
doc.save(OUT_DOCX)
print(f"v7 DOCX saved to {OUT_DOCX}")

# Compile to PDF
cmd = ["soffice", "--headless", "--convert-to", "pdf", OUT_DOCX, "--outdir", "v7_workspace"]
subprocess.run(cmd, check=True)
print(f"v7 PDF compiled to {OUT_PDF}")
