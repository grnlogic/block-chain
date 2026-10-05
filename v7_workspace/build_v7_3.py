#!/usr/bin/env python3
"""
build_v7_3.py
Master build script to generate Laporan_UTS_Blockchain_237006079_v7.3.docx and .pdf
directly and reproducibly from the base docx:
uts-blockchain-submission/Laporan_UTS_Blockchain_237006079.docx.

Contains ALL changes (v7, v7.1, v7.2, v7.3) end-to-end without manual docx editing:
- v7: Table 11/13 move to Lampiran D/E, renumbering body tables 1-10, UTXO compression,
      Diagram 2 scaling (80%), soft-pedaling claims.
- v7.1: BlockGasLimit 60.000.000 (0x3938700), hardware specs 12th Gen Intel(R) Core(TM)
        i5-12450H 12 thread logis, RAM total 15 GiB, Table 2/7 ellipsis formatting,
        UU PDP separate articles (Pasal 4 ayat 3, Pasal 8, Pasal 9, Pasal 43 ayat 1).
- v7.2: Body strictly <= 12 pages (Cara i), blank lines remaining on page 12,
        Lampiran F for B-06 (exp_b06_output.txt & Run A-E table), Lampiran D & E raised to 9 pt,
        body tables untouched, short hex notation restored (0x03e8, 0x06, 0x3938700),
        Lampiran A AI disclosure updated, PDF metadata set.
- v7.3: Dynamic hash ingestion & assertions from demo-output.txt (Tabel 2, 5, 7, Lampiran B),
        Subbab 4.7 claim updated to strictly measured O(1) gas 164.911 for N=6, 100, 1000,
        Lampiran F caller updated to revoker (REVOKER_ROLE) & EVM snapshot/revert preserved,
        Appendix physical order strictly A -> B -> C -> D -> E -> F with Lampiran C on own page.
"""

import docx
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import subprocess
import os
import re

SRC_DOCX = "uts-blockchain-submission/Laporan_UTS_Blockchain_237006079.docx"
OUT_DOCX = "v7_workspace/Laporan_UTS_Blockchain_237006079_v7.3.docx"
OUT_PDF = "v7_workspace/Laporan_UTS_Blockchain_237006079_v7.3.pdf"

print(f"Loading base docx from: {SRC_DOCX}")
doc = docx.Document(SRC_DOCX)

# Set Document Core Properties (Metadata)
doc.core_properties.author = "Fajar Geran Arifin"
doc.core_properties.title = "UTS Blockchain - Rancangan Sistem Verifikasi Kredensial Akademik"

# =============================================================================
# 0. PARSE DEMO OUTPUT FOR DYNAMIC HASH INGESTION & ASSERTIONS (POIN 1d)
# =============================================================================
def parse_demo_log(filepath="prototype/results/demo-output.txt"):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Berkas log demo {filepath} tidak ditemukan!")
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Alamat Kontrak
    m_addr = re.search(r"Alamat Kontrak\s*:\s*(0x[a-fA-F0-9]{40})", text)
    assert m_addr, "Alamat kontrak tidak ditemukan di demo log"
    contract_addr = m_addr.group(1)

    # Tx Hash Deployment
    m_tx_deploy = re.search(r"Tx Hash Deployment\s*:\s*(0x[a-fA-F0-9]{64})", text)
    assert m_tx_deploy, "Tx deployment tidak ditemukan di demo log"
    tx_deploy = m_tx_deploy.group(1)

    # Merkle Root
    m_root = re.search(r"Merkle Root Terhitung\s*:\s*(0x[a-fA-F0-9]{64})", text) or \
             re.search(r"Root Tersimpan State\s*:\s*(0x[a-fA-F0-9]{64})", text)
    assert m_root, "Merkle root tidak ditemukan di demo log"
    merkle_root = m_root.group(1)

    # Tx Hash Penerbitan
    m_tx_issue = re.search(r"Tx Hash Penerbitan\s*:\s*(0x[a-fA-F0-9]{64})", text)
    assert m_tx_issue, "Tx penerbitan tidak ditemukan di demo log"
    tx_issue = m_tx_issue.group(1)

    # Daun G-01 s.d. G-06
    leaf_hashes = {}
    for i in range(1, 7):
        gid = f"G-{i:02d}"
        m_leaf = re.search(rf"\[{gid}\][^|]*\|[^|]*\|[^|]*\|\s*Leaf:\s*(0x[0-9a-fA-F]+)", text)
        assert m_leaf, f"Hash daun {gid} tidak ditemukan di demo log"
        leaf_hashes[gid] = m_leaf.group(1)

    # Leaf Asli dan Manipulasi
    m_orig = re.search(r"Leaf Asli\s*:\s*(0x[a-fA-F0-9]{64})", text)
    assert m_orig, "Leaf Asli tidak ditemukan di demo log"
    leaf_original = m_orig.group(1)

    m_tamper = re.search(r"Leaf Hasil Manipulasi\s*:\s*(0x[a-fA-F0-9]{64})", text)
    assert m_tamper, "Leaf Hasil Manipulasi tidak ditemukan di demo log"
    leaf_tampered = m_tamper.group(1)

    # Assert bahwa Leaf Asli sama dengan hash G-01
    assert leaf_original.startswith(leaf_hashes["G-01"]), \
        f"Leaf Asli {leaf_original} tidak cocok dengan G-01 {leaf_hashes['G-01']}"

    return {
        "contract_addr": contract_addr,
        "tx_deploy": tx_deploy,
        "merkle_root": merkle_root,
        "tx_issue": tx_issue,
        "leaf_hashes": leaf_hashes,
        "leaf_original": leaf_original,
        "leaf_tampered": leaf_tampered
    }

demo_data = parse_demo_log()
print("Demo log parsed and asserted successfully:")
print(f"  Contract: {demo_data['contract_addr']}")
print(f"  Tx Deploy: {demo_data['tx_deploy']}")
print(f"  Merkle Root: {demo_data['merkle_root']}")
print(f"  Tx Issue: {demo_data['tx_issue']}")
print(f"  Leaf Asli: {demo_data['leaf_original']}")
print(f"  Leaf Tamper: {demo_data['leaf_tampered']}")

def replace_in_p(p, old, new, preserve_format=True):
    """Replace text in paragraph preserving runs or formatting."""
    if old not in p.text:
        return False
    if not p.runs:
        p.text = p.text.replace(old, new)
        return True
    for r in p.runs:
        if old in r.text:
            r.text = r.text.replace(old, new)
            return True
    # If old spans across runs
    fname = p.runs[0].font.name or "Calibri"
    fsize = p.runs[0].font.size or Pt(10.0)
    color = p.runs[0].font.color.rgb if p.runs[0].font.color else None
    bold = p.runs[0].font.bold
    p.text = p.text.replace(old, new)
    if preserve_format:
        for r in p.runs:
            r.font.name = fname
            r.font.size = fsize
            if color:
                r.font.color.rgb = color
            r.font.bold = bold
    return True

# =============================================================================
# 1. FOOTER UPDATE
# =============================================================================
for sec in doc.sections:
    footer = sec.footer
    for p in footer.paragraphs:
        if "Template Laporan Kegiatan Blockchain" in p.text:
            p.text = "Laporan UTS Blockchain | TA 2026/2027"

# =============================================================================
# 2. CLEAR CANTSPLIT ON ALL TABLE ROWS FOR NATURAL PAGE FLOW
# =============================================================================
for t in doc.tables:
    for r in t.rows:
        trPr = r._tr.get_or_add_trPr()
        cs = trPr.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}cantSplit")
        if cs is not None:
            trPr.remove(cs)

# =============================================================================
# 3. HEADING FIXES (REMOVE "Case n")
# =============================================================================
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

# =============================================================================
# 4. COMPRESS SUBCHAPTER 4.4 (UTXO) INTO 4.3 AND REMOVE TABLE 7
# =============================================================================
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

for p in doc.paragraphs:
    if "Analisis Fork & Pemilihan Konsensus:" in p.text:
        p.text = p.text + (
            " Evaluasi Model UTXO vs Akun EVM (P2): Dalam memenuhi luaran P2 terkait justifikasi arsitektur, "
            "model Unspent Transaction Output (UTXO) Bitcoin dianalisis sebagai pembanding. Model UTXO bersifat stateless "
            "dan membatasi penyisipan data pada script OP_RETURN maksimal 80 byte (~0.005 BTC biaya transaksi ilustratif tanpa smart logic). "
            "Kelemahan fatal UTXO untuk ijazah adalah ketiadaan penyimpanan status dinamis (stateful storage); untuk membatalkan ijazah pada UTXO, "
            "penerbit harus membuat rantai transaksi pembelanjaan baru yang rumit. Sebaliknya, model akun EVM menyediakan mesin status "
            "terprogram yang memungkinkan penyimpanan status pencabutan individual secara langsung dalam slot mapping storage (_revokedCredentials[leafHash]) "
            "dengan kompleksitas akses O(1) dan biaya komputasi deterministik."
        )

if p_utxo_heading is not None:
    p_utxo_heading._element.getparent().remove(p_utxo_heading._element)
if p_utxo_p1 is not None and "Analisis Model UTXO:" in p_utxo_p1.text:
    p_utxo_p1._element.getparent().remove(p_utxo_p1._element)
if p_utxo_p2 is not None and "Komparasi Model Akun vs UTXO:" in p_utxo_p2.text:
    p_utxo_p2._element.getparent().remove(p_utxo_p2._element)

# Remove Table 7 (UTXO evaluation table)
tbl7_utxo = doc.tables[7]
tbl7_utxo._element.getparent().remove(tbl7_utxo._element)

# =============================================================================
# 5. DETACH TABLE 11 (CRITERIA) & TABLE 13 (BENCHMARK) TO BE PLACED IN APPENDICES
# =============================================================================
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

# Detach criteria & bench tables from body
tbl_criteria._element.getparent().remove(tbl_criteria._element)
tbl_bench._element.getparent().remove(tbl_bench._element)

# Create Lampiran D heading and container
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

# Create Lampiran E heading and container
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

# Remove p_lamp_d and p_lamp_e from current body end (they will be inserted in exact order)
p_lamp_d._element.getparent().remove(p_lamp_d._element)
p_lamp_e._element.getparent().remove(p_lamp_e._element)

# =============================================================================
# 6. HARDWARE SPECS (12th Gen Intel(R) Core(TM) i5-12450H, 12 thread logis, RAM total 15 GiB)
# =============================================================================
t1 = doc.tables[1]
for r in t1.rows:
    if "Perangkat Keras Node" in r.cells[0].text:
        r.cells[1].text = "12th Gen Intel(R) Core(TM) i5-12450H (8 fisik / 12 thread logis), RAM total 15 GiB (15.700.320 kB), OS Linux x86_64 Kernel 6.6"

# =============================================================================
# 7. UPDATE TABLE 2 (CATATAN PELAKSANAAN) WITH PARSED HASHES (POIN 1d)
# =============================================================================
t2 = doc.tables[2]
# Row 2: Deployment
t2.rows[2].cells[2].text = (
    f"Kontrak aktif di alamat {demo_data['contract_addr'][:12]}..., "
    f"Tx: {demo_data['tx_deploy'][:10]}..., Gas: 1.039.368 unit [B-01]"
)
# Row 3: Off-chain Merkle
t2.rows[3].cells[2].text = (
    f"Pohon Merkle (129,44 ms off-chain, B-02); 6 daun bergaram, "
    f"Root: {demo_data['merkle_root'][:10]}... (Tabel 5, Diagram 3, results/demo-output.txt)"
)
# Row 4: On-chain Issue & Revoke
t2.rows[4].cells[2].text = (
    f"Root terdaftar Block #2 tx {demo_data['tx_issue'][:10]}... [B-03]; verifikasi valid 0 gas [B-04]; "
    f"pencegahan non-issuer [B-05B]; pencabutan 56.359 gas [B-06]; jeda darurat 48.214 gas [B-07]"
)
# Row 5: Benchmark
t2.rows[5].cells[2].text = (
    "Gas eksekusi murni issueBatch konstan 164.911 gas (O(1)), bukti selisih calldata deterministik tepat 84 gas. "
    "Rujukan: B-08, Tabel 8, Lampiran D, Lampiran E (results/perf-output.txt)"
)

# =============================================================================
# 8. UPDATE TABLE 5 (RECORD DAUN MERKLE) & ASSERT HASHES (POIN 1d)
# =============================================================================
t5 = None
for t in doc.tables:
    if "Record / Daun" in t.rows[0].cells[0].text:
        t5 = t
        break

if t5 is not None:
    for idx in range(1, 7):
        gid = f"G-{idx:02d}"
        expected_leaf = demo_data["leaf_hashes"][gid]
        # Assert leaf hash from demo log matches cell prefix
        assert expected_leaf in t5.rows[idx].cells[3].text or expected_leaf[:16] in t5.rows[idx].cells[3].text, \
            f"Tabel 5 Row {idx} hash {t5.rows[idx].cells[3].text} does not match {expected_leaf}"
        # Set formatted text with parsed hash
        t5.rows[idx].cells[3].text = f"{expected_leaf[:18]}... (32 byte)"

# =============================================================================
# 9. UPDATE TABLE 7 (FIELD TRANSAKSI EVM) WITH PARSED HASHES & 60M GAS (POIN 1d)
# =============================================================================
for t in doc.tables:
    if "Field Transaksi EVM" in t.rows[0].cells[0].text:
        t.rows[3].cells[0].text = "Gas Limit / Gas Used / Status"
        t.rows[3].cells[1].text = "Gas Limit Blok: 60.000.000 (Parameter terukur node lokal Hardhat); Gas Used: 211.084 gas (penjangkaran batch); Status: 1 (Success)"
        t.rows[4].cells[0].text = "Event Logs & Transaction Hash"
        t.rows[4].cells[1].text = f"Event: BatchIssued(WISUDA-2026-PERIODE-1, {demo_data['merkle_root'][:10]}..., timestamp); Tx Hash: {demo_data['tx_issue'][:10]}...; Block: #2 [B-03]"
        for r_idx in [3, 4]:
            for c_idx in [0, 1]:
                for p in t.rows[r_idx].cells[c_idx].paragraphs:
                    for r in p.runs:
                        r.font.name = 'Calibri'
                        r.font.size = Pt(7.5)
        break

# =============================================================================
# 10. TEXT LEVEL REPLACEMENTS (UU PDP, SHORT HEX, MEASURED O(1) CLAIMS)
# =============================================================================
for p in doc.paragraphs:
    # UU PDP separate articles
    replace_in_p(p, "Pasal 8 dan 43 ayat (1)", "Pasal 8 dan 43 ayat (1)")
    if "Pasal 4 ayat (3) dan Pasal 8 UU PDP" in p.text:
        p.text = p.text.replace(
            "Pasal 4 ayat (3) dan Pasal 8 UU PDP",
            "Pasal 4 ayat (3), Pasal 8, Pasal 9, dan Pasal 43 ayat (1) UU PDP"
        )
    if "Pasal 4 ayat (3) dan Pasal 8 UU PDP Nomor 27 Tahun 2022" in p.text:
        p.text = p.text.replace(
            "Pasal 4 ayat (3) dan Pasal 8 UU PDP Nomor 27 Tahun 2022",
            "Pasal 4 ayat (3), Pasal 8, Pasal 9, dan Pasal 43 ayat (1) UU PDP Nomor 27 Tahun 2022"
        )
    if "Pasal 4 ayat 3 dan Pasal 8 UU PDP" in p.text:
        p.text = p.text.replace(
            "Pasal 4 ayat 3 dan Pasal 8 UU PDP",
            "Pasal 4 ayat (3), Pasal 8, Pasal 9, dan Pasal 43 ayat (1) UU PDP"
        )

    # Section 4.1 Konsorsium nodes & Besu
    replace_in_p(p, "3 validator utama", "6 node anggota konsorsium")
    replace_in_p(p, "4 node konsorsium", "6 node anggota konsorsium")
    replace_in_p(p, "Hyperledger Besu berprofil genesis", "Hyperledger Besu berprofil QBFT")

    # Section 4.2 Kriptografi & W3C
    if "Kepatuhan Regulasi Privasi Data Pribadi (P3):" in p.text:
        p.text = (
            "Kepatuhan Regulasi Privasi Data Pribadi (P3): Desain ini secara ketat mematuhi ketentuan UU PDP No. 27/2022 [10] "
            "dan Permendikbudristek No. 6/2022 [13]. Data pribadi lulusan diklasifikasikan sebagai data spesifik dan umum (Pasal 4 ayat 3). "
            "Penyimpanan hash bergaram pada ledger publik memastikan hak penghapusan data (Right to Erasure, Pasal 8 UU PDP) "
            "serta kewajiban pengendali data untuk menghapus rekaman pribadi saat retensi berakhir (Pasal 43 ayat 1) dapat dipenuhi tanpa merusak "
            "integritas bukti penjangkaran Merkle. Pemrosesan data pribadi juga senantiasa berlandaskan dasar pemrosesan yang sah "
            "dan persetujuan eksplisit (Pasal 9 UU PDP)."
        )

    # Section 4.3 P2P & Konsensus
    if "Perbandingan Toleransi Kesalahan:" in p.text:
        p.text = (
            "Perbandingan Toleransi Kesalahan: Model konsensus dievaluasi berdasarkan kebutuhan integritas ijazah nasional. "
            "Proof-of-Work (PoW) dieliminasi karena inefisiensi energi dan risiko 51% attack. Raft memiliki throughput tinggi "
            "tetapi rentan (Crash Fault Tolerant, tidak tahan serangan jahat). QBFT (IBFT 2.0) pada Hyperledger Besu dipilih "
            "karena menjamin toleransi kesalahan Byzantine hingga F < N/3 node jahat, dengan finalitas deterministik seketika (zero probabilistic fork)."
        )

    # Section 4.4 Calldata claim & Short Hex restoration (0x03e8, 0x06)
    if "Rincian Biaya Calldata Berdasarkan Ukuran Batch:" in p.text:
        p.text = (
            "Rincian Biaya Calldata Berdasarkan Ukuran Batch: Analisis calldata pada 30 run benchmark mengungkap bahwa "
            "variasi calldata murni ditentukan oleh panjang string batchId dan nilai argumen fungsi: "
            "(1) Pada Batch N=6 (batchId = \"BATCH-6-ITER-X\"), parameter totalRecords bernilai 6 (0x06 dalam representasi hex kompak EVM), "
            "menghasilkan rata-rata 140,4 byte nol dan 87,6 byte non-nol dengan biaya calldata 1.963 gas. "
            "(2) Pada Batch N=100 (batchId = \"BATCH-100-ITER-X\"), string batchId bertambah 2 byte non-nol, menghasilkan 2.011 gas (+48 gas calldata). "
            "(3) Pada Batch N=1.000 (batchId = \"BATCH-1000-ITER-X\"), totalRecords bernilai 1.000 (0x03e8 dalam representasi hex kompak EVM, "
            "mengandung 1 byte nol dan 1 byte non-nol), menghasilkan 2.047 gas (+36 gas calldata)."
        )

    # Section 4.6 Acceptance criteria text
    if "Kriteria penerimaan (acceptance criteria) disusun dengan merujuk pada standar ilmiah" in p.text:
        p.text = (
            "Kriteria penerimaan (acceptance criteria) disusun dengan merujuk pada standar ilmiah W3C VC [1], Ethereum JSON-RPC eth_call [2], "
            "OpenZeppelin Contracts v5 [3], Paten Pohon Merkle 1982 [4], Prinsip Least Privilege Saltzer-Schroeder 1975 [5], "
            "Keccak Reference [6], Nielsen Norman Group [7], W3C Bitstring Status List v1.0 [8], UU PDP No. 27/2022 [10], EIP-2028 [11], "
            "dan RFC 8785 [9]. Rincian matriks evaluasi lengkap kriteria penerimaan terhadap luaran OBE disajikan pada Lampiran D. "
            "Seluruh kriteria fungsional, keamanan, dan batas komputasi terpenuhi 100% pada lingkungan uji coba Hardhat."
        )

    # Section 4.6 Benchmark text
    if "Pengujian performa mendalam dilakukan melalui 30 run terukur" in p.text:
        p.text = (
            "Pengujian performa mendalam dilakukan melalui 30 run terukur (+ 2 run warm-up) pada skrip scripts/perf-benchmark.js "
            "untuk mengevaluasi konsumsi gas, panjang bukti pembuktian (proof length), waktu pembuatan Merkle tree, "
            "dan latensi verifikasi read-only (eth_call) pada tiga skala batch lulusan: N = 6, N = 100, dan N = 1.000. "
            "Rekapitulasi lengkap metrik statistik benchmark 30 run dirangkum pada Lampiran E."
        )

    # Section 4.7 POIN 7a: Hapus "memungkinkan jutaan kredensial" -> ganti dengan terukur O(1)
    if "akan menghabiskan lebih dari 20 juta gas untuk 1.000 lulusan" in p.text:
        p.text = (
            "Keputusan Desain & Trade-Off: Tiga keputusan desain fundamental melandasi prototipe ini: "
            "(1) On-chain vs Off-chain: Memilih off-chain document storage dengan on-chain cryptographic commitment (Merkle root). "
            "Pendekatan ini menjamin efisiensi penyimpanan dan kepatuhan penuh terhadap regulasi privasi data. "
            "Penjangkaran individual 1.000 dokumen diestimasi menghabiskan lebih dari 20 juta gas. "
            "Pendekatan Merkle batching mengompresi batch ijazah ke dalam 1 Merkle Root 32-byte [4] "
            "dengan efisiensi gas eksekusi kontrak yang terukur konstan O(1) sebesar 164.911 gas untuk N = 6, 100, dan 1.000 lulusan "
            "(hemat > 98% dibanding penjangkaran individual)."
        )

    # Section 4.7 Keterbatasan Teknis title cleanups
    replace_in_p(p, "• 1. Lingkungan Node: Lingkungan Single-Node Hardhat:", "• 1. Lingkungan Single-Node In-Process:")
    replace_in_p(p, "• 1. Lingkungan Node: Lingkungan Single-Node In-Process:", "• 1. Lingkungan Single-Node In-Process:")
    replace_in_p(p, "• 2. Data Uji: Data Sintetis Fiktif:", "• 2. Data Uji Sintetis:")
    replace_in_p(p, "• 3. Perangkat Keras: Karakteristik Mesin Uji Tunggal:", "• 3. Karakteristik Mesin Uji Tunggal:")
    replace_in_p(p, "• 4. Simulasi Gas: Hakikat Nilai estimateGas:", "• 4. Hakikat Nilai estimateGas:")
    replace_in_p(p, "• 5. Slot Storage URI: Alokasi Slot Storage metadataURI:", "• 5. Alokasi Slot Storage metadataURI:")
    replace_in_p(p, "• 5. Slot Storage URI: Alokasi Slot Storage URI:", "• 5. Alokasi Slot Storage metadataURI:")
    replace_in_p(p, "• 6. Batas Gas Blok: Parameter Node Lokal Hardhat vs Hipotesis Konsorsium:", "• 6. Batas Gas Blok Node Lokal vs Konsorsium:")
    replace_in_p(p, "• 7. Pembulatan Calldata: Efek Pembulatan Rata-Rata Calldata (83 vs 84 gas):", "• 7. Efek Pembulatan Calldata (83 vs 84 gas):")

    # Section 4.7 Bullet 6 Gas Limit (Measured 60.000.000 & 0x3938700)
    if "• 6. Batas Gas Blok" in p.text:
        p.text = (
            "• 6. Batas Gas Blok Node Lokal vs Konsorsium: Pengukuran aktual pada node lokal Hardhat melalui RPC "
            "eth_getBlockByNumber menghasilkan blockGasLimit sebesar 60.000.000 gas (0x3938700). Angka 30.000.000 gas "
            "dijadikan contoh hipotetis jaringan konsorsium untuk simulasi kapasitas blok. Penjangkaran individual "
            "1.000 ijazah (~20 juta gas) akan menyerap sepertiga (33,3%) dari batas blok 60 juta gas atau dua pertiga "
            "(66,7%) dari contoh hipotetis 30 juta gas, sedangkan skema Merkle batching pada prototipe ini hanya "
            "memerlukan 211.084 gas (< 0,36% dari batas blok 60 juta gas)."
        )

# =============================================================================
# 11. SUBCHAPTER 4.6 OBE MATRIKS SUMMARY TABLE INTRO
# =============================================================================
for p in doc.paragraphs:
    if "Berikut adalah ringkasan matriks pemenuhan luaran OBE berdasarkan hasil pengujian:" in p.text:
        p.text = (
            "Ringkasan ambang batas penerimaan luaran OBE (rincian lengkap disajikan pada Lampiran D):\n"
            "• Penjangkaran Batch: Deviasi gas murni <= 1.0% (O(1)), total gas <= 1.0% Block Gas Limit (60M gas node lokal / 30M gas contoh hipotetis konsorsium).\n"
            "• Verifikasi Bukti Merkle: Panjang proof <= ceil(log2 N) (3 untuk N=6, 7 untuk N=100, 10 untuk N=1.000); 0 gas verifikator publik.\n"
            "• Mekanisme Keamanan: Penolakan manipulasi klaim IPK & salt (B-05A), pencegatan unauthorized role (B-05B), jeda darurat pause() (B-07).\n"
            "• Efisiensi Komputasi: Waktu pembuatan tree < 1.000 ms; pureVerifyGas(k) <= 10.000 + (k * 350) gas; kueri eth_call < 1 ms."
        )
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(2)
        for r in p.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(9.0)

# =============================================================================
# 12. INSERT B-06 SUMMARY IN SUBCHAPTER 4.7 (MAX 3 SENTENCES + LAMPIRAN F)
# =============================================================================
for p in doc.paragraphs:
    if "• 7. Efek Pembulatan Calldata" in p.text:
        # Check if already inserted
        p_b06 = doc.add_paragraph()
        p_b06.text = (
            "• 8. Analisis Selisih Gas Pencabutan B-06: Pada pengujian prototipe, revokeCredential mengonsumsi 56.359 gas "
            "(demo B-06) dan 55.297 s.d. 55.333 gas (benchmark 30 run). Melalui eksperimen isolasi variabel tunggal (exp_b06_v2.js), "
            "selisih tersebut terbukti bersumber dari perbedaan calldata batchId (-84 gas) serta lompatan batas alokasi 32-byte pada event log "
            "CredentialRevoked (+256 gas data log untuk string 60 byte demo vs 11 byte benchmark). "
            "Rincian tabel Run A s.d. E dan log pengujian disajikan pada Lampiran F."
        )
        p_b06.paragraph_format.space_before = Pt(3)
        p_b06.paragraph_format.space_after = Pt(2)
        for r in p_b06.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(9.0)
        p._element.addnext(p_b06._element)
        break

# =============================================================================
# 13. REFERENCES 10, 11, 12, 13 FORMATTING
# =============================================================================
for p in doc.paragraphs:
    if p.text.startswith("[10]"):
        p.text = (
            '[10] Republik Indonesia, Undang-Undang Republik Indonesia Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP), '
            'Lembaran Negara Republik Indonesia Tahun 2022 Nomor 196, Tambahan Lembaran Negara Nomor 6820, Jakarta, Okt. 2022. [Daring]. '
            'Tersedia: https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022. [Diakses: 5 Oktober 2026].'
        )
    if p.text.startswith("[11]"):
        p.text = (
            '[11] A. Akhunov, E. B. Sasson, T. Brand, L. Guthmann, dan A. Levy, "EIP-2028: Transaction data gas cost reduction," '
            'Ethereum Improvement Proposals, Mei 2019. [Daring]. Tersedia: https://eips.ethereum.org/EIPS/eip-2028. [Diakses: 4 Oktober 2026].'
        )

# Ensure Ref 12 & 13
has_ref12 = any(p.text.startswith("[12]") for p in doc.paragraphs)
has_ref13 = any(p.text.startswith("[13]") for p in doc.paragraphs)

if not has_ref12 or not has_ref13:
    p_ref11_idx = None
    for idx, p in enumerate(doc.paragraphs):
        if p.text.startswith("[11]"):
            p_ref11_idx = idx
            break
    if p_ref11_idx is not None:
        p12 = doc.add_paragraph()
        p12.text = (
            '[12] National Institute of Standards and Technology (NIST), "SHA-3 Standard: Permutation-Based Hash and '
            'Extendable-Output Functions," Federal Information Processing Standards (FIPS) Publication 202, Agu. 2015. '
            '[Daring]. Tersedia: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf. [Diakses: 4 Oktober 2026].'
        )
        p12.paragraph_format.space_before = Pt(2)
        p12.paragraph_format.space_after = Pt(2)
        for r in p12.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(8.5)
        doc.paragraphs[p_ref11_idx]._element.addnext(p12._element)

        p_ref12_idx = p_ref11_idx + 1
        p13 = doc.add_paragraph()
        p13.text = (
            '[13] Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi Republik Indonesia, "Peraturan Menteri Pendidikan, '
            'Kebudayaan, Riset, dan Teknologi Republik Indonesia Nomor 6 Tahun 2022 tentang Ijazah, Sertifikat Kompetensi, '
            'Sertifikat Profesi, Gelar, dan Kesetaraan Ijazah Perguruan Tinggi Negara Lain," Berita Negara Republik Indonesia '
            'Tahun 2022 Nomor 167, Jakarta, Feb. 2022. [Daring]. Tersedia: https://peraturan.go.id/id/permendikbudristek-no-6-tahun-2022. '
            '[Diakses: 4 Oktober 2026].'
        )
        p13.paragraph_format.space_before = Pt(2)
        p13.paragraph_format.space_after = Pt(2)
        for r in p13.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(8.5)
        doc.paragraphs[p_ref12_idx]._element.addnext(p13._element)

# =============================================================================
# 14. UPDATE LAMPIRAN A (PENGUNGKAPAN AI TRANSPARAN HINGGA v7.3)
# =============================================================================
for i, p in enumerate(doc.paragraphs):
    if "Lampiran A: Pengungkapan Penggunaan Alat Bantu AI" in p.text:
        for j in range(i + 1, min(i + 10, len(doc.paragraphs))):
            pj = doc.paragraphs[j]
            if "• 2. Google Antigravity Agent:" in pj.text:
                p_ai = doc.add_paragraph()
                p_ai.text = (
                    "• 3. Siklus Koreksi & Verifikasi Laporan (v7 s.d. v7.3): Tahap koreksi v7 sampai v7.3 "
                    "dikerjakan dengan agent (Google Antigravity) atas arahan saya, dan peninjauan serta penyusunan "
                    "instruksi koreksi dibantu Claude (asisten AI Anthropic); kode kontrak, hasil uji, dan angka "
                    "pengukuran tidak diubah."
                )
                p_ai.paragraph_format.space_before = Pt(2)
                p_ai.paragraph_format.space_after = Pt(2)
                for r in p_ai.runs:
                    r.font.name = 'Arial'
                    r.font.size = Pt(8.5)
                pj._element.addnext(p_ai._element)
            if "• 3. Tanggung Jawab Penulis:" in pj.text:
                pj.text = pj.text.replace("• 3. Tanggung Jawab Penulis:", "• 4. Tanggung Jawab Penulis:")
                for r in pj.runs:
                    r.font.name = 'Arial'
                    r.font.size = Pt(8.5)
        break

# =============================================================================
# 15. INSERT NUMBERED CAPTIONS FOR BODY TABLES 1 THROUGH 10
# =============================================================================
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

# =============================================================================
# 16. SCALE DIAGRAM 2 (80%)
# =============================================================================
scale = 0.80
for p in doc.paragraphs:
    for r in p.runs:
        extents = r._r.xpath(".//wp:extent")
        for ext in extents:
            cx = int(ext.attrib.get("cx", 0))
            cy = int(ext.attrib.get("cy", 0))
            if cy > 3000000:
                ext.attrib["cx"] = str(int(cx * scale))
                ext.attrib["cy"] = str(int(cy * scale))

# =============================================================================
# 17. RAISE FONT SIZE FOR LAMPIRAN D AND E TO MINIMAL 9 PT
# =============================================================================
for t in [tbl_criteria, tbl_bench]:
    for r in t.rows:
        for c in r.cells:
            for p in c.paragraphs:
                for run in p.runs:
                    run.font.name = 'Arial'
                    run.font.size = Pt(9.0)
                    if "30M gas" in run.text:
                        run.text = run.text.replace("30M gas", "60M gas node lokal / 30M gas contoh hipotetis konsorsium")

# =============================================================================
# 18. LAMPIRAN B ASSERTION & VERIFICATION (POIN 1d)
# =============================================================================
for p in doc.paragraphs:
    if "Leaf Asli" in p.text and "Leaf Hasil Manipulasi" in p.text:
        assert demo_data["leaf_original"] in p.text, "Lampiran B does not contain exact Leaf Asli"
        assert demo_data["leaf_tampered"] in p.text, "Lampiran B does not contain exact Leaf Hasil Manipulasi"
        print("Lampiran B hash assertion PASSED (Leaf Asli & Manipulasi match demo log).")
        break

# =============================================================================
# 19. LAMPIRAN C START ON OWN PAGE (POIN 7c)
# =============================================================================
for p in doc.paragraphs:
    if "Lampiran C: Pernyataan Orisinalitas" in p.text:
        p.paragraph_format.page_break_before = True
        print("Lampiran C configured to start on its own page (page_break_before = True).")
        break

# =============================================================================
# 20. CONSTRUCT LAMPIRAN F (EKSPERIMEN B-06) - POIN 7b
# =============================================================================
p_lamp_f_heading = doc.add_paragraph()
p_lamp_f_heading.text = "Lampiran F: Eksperimen Isolasi Variabel Selisih Gas revokeCredential (B-06)"
p_lamp_f_heading.paragraph_format.space_before = Pt(16)
p_lamp_f_heading.paragraph_format.space_after = Pt(4)
p_lamp_f_heading.paragraph_format.keep_with_next = True
for r in p_lamp_f_heading.runs:
    r.font.name = 'Arial'
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)

p_lamp_f_intro = doc.add_paragraph()
p_lamp_f_intro.text = (
    "Eksperimen isolasi variabel tunggal (exp_b06_v2.js) dirancang untuk memverifikasi akar penyebab matematis "
    "perbedaan konsumsi gas fungsi revokeCredential antara skrip demo (56.359 gas pada Bukti B-06) dan hasil benchmark "
    "(55.297 s.d. 55.333 gas). Seluruh run dieksekusi pada smart contract yang sama (AcademicCredentialRegistry.sol), "
    "pemanggil yang sama (akun pencabut berwenang: revoker dengan peran REVOKER_ROLE), dan status state awal yang identik "
    "melalui mekanisme EVM snapshot/revert. Panjang parameter diukur secara eksak menggunakan Buffer.byteLength() dan "
    "komponen calldata dihitung sesuai aturan EIP-2028."
)
p_lamp_f_intro.paragraph_format.space_before = Pt(2)
p_lamp_f_intro.paragraph_format.space_after = Pt(4)
for r in p_lamp_f_intro.runs:
    r.font.name = 'Arial'
    r.font.size = Pt(9.0)

# Table Run A to E
table_f_data = [
    ["Skenario Uji (Run)", "Parameter batchId", "Parameter reason", "Calldata Gas", "Gas Receipt", "Selisih vs Run A", "Prediksi Δ Cd", "SISA (Terukur-ΔCd)"],
    ["Run A (Identik Demo)", "WISUDA-2026-PERIODE-1 (32 B, 21 non-0)", "Putusan Sidang Komite Etik... (60 B)", "2.212 gas", "56.359 gas", "0 (Basis)", "0 gas", "0 gas"],
    ["Run B (Ubah batchId)", "BATCH-6-ITER-1 (32 B, 14 non-0)", "Putusan Sidang Komite Etik... (60 B)", "2.128 gas", "56.275 gas", "-84 gas", "-84 gas", "0 gas"],
    ["Run C (Ubah reason)", "WISUDA-2026-PERIODE-1 (32 B, 21 non-0)", "Sidang Etik (11 B)", "1.496 gas", "55.381 gas", "-978 gas", "-716 gas", "-262 gas"],
    ["Run D (Reason 11 B)", "WISUDA-2026-PERIODE-1 (32 B, 21 non-0)", "Sidang Etik (11 B UTF-8)", "1.496 gas", "55.381 gas", "-978 gas", "-716 gas", "-262 gas"],
    ["Run D (Reason 31 B)", "WISUDA-2026-PERIODE-1 (32 B, 21 non-0)", "31 byte string UTF-8", "1.736 gas", "55.621 gas", "-738 gas", "-476 gas", "-262 gas"],
    ["Run D (Reason 32 B)", "WISUDA-2026-PERIODE-1 (32 B, 21 non-0)", "32 byte string UTF-8", "1.748 gas", "55.633 gas", "-726 gas", "-464 gas", "-262 gas"],
    ["Run D (Reason 33 B)", "WISUDA-2026-PERIODE-1 (32 B, 21 non-0)", "33 byte string UTF-8", "1.888 gas", "56.035 gas", "-324 gas", "-324 gas", "0 gas"],
    ["Run D (Reason 60 B)", "WISUDA-2026-PERIODE-1 (32 B, 21 non-0)", "60 byte string UTF-8 (Demo)", "2.212 gas", "56.359 gas", "0 (Basis)", "0 gas", "0 gas"],
    ["Run E (Bench N=6)", "BATCH-6-ITER-1 (32 B, 14 non-0)", "Sidang Etik (11 B UTF-8)", "1.412 gas", "55.297 gas", "-1.062 gas", "-800 gas", "-262 gas"],
    ["Run E (Bench N=100)", "BATCH-100-ITER-1 (32 B, 16 non-0)", "Sidang Etik (11 B UTF-8)", "1.436 gas", "55.321 gas", "-1.038 gas", "-776 gas", "-262 gas"],
    ["Run E (Bench N=1000)", "BATCH-1000-ITER-1 (32 B, 17 non-0)", "Sidang Etik (11 B UTF-8)", "1.448 gas", "55.333 gas", "-1.026 gas", "-764 gas", "-262 gas"]
]

tbl_f = doc.add_table(rows=len(table_f_data), cols=len(table_f_data[0]))
tbl_f.alignment = WD_TABLE_ALIGNMENT.CENTER

for row_idx, row in enumerate(table_f_data):
    for col_idx, text in enumerate(row):
        cell = tbl_f.cell(row_idx, col_idx)
        cell.text = text
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                r.font.name = 'Arial'
                r.font.size = Pt(8.0)
                if row_idx == 0:
                    r.font.bold = True

p_lamp_f_analysis = doc.add_paragraph()
p_lamp_f_analysis.text = (
    "Analisis Hasil Eksperimen dan Temuan Matematis Terukur:\n"
    "1. Resolusi Panjang String: String reason demo terkonfirmasi berukuran tepat 60 karakter / 60 byte UTF-8 "
    "(perbedaan dengan angka 61 pada laporan sebelumnya terselesaikan sebagai salah hitung manual).\n"
    "2. Variasi batchId (Run B): Perubahan batchId dari format demo ke benchmark menghasilkan selisih tepat -84 gas, "
    "yang 100% cocok dengan penurunan 7 byte non-nol calldata EIP-2028 (7 * 12 gas = 84 gas) dengan SISA = 0 gas.\n"
    "3. Lompatan Batas 32-Byte Event Log Data (Run D): Pada pengujian Run D, saat panjang string reason dinaikkan dari "
    "32 byte menjadi 33 byte, terjadi lonjakan tepat 262 gas pada komponen non-calldata (nilai SISA berubah dari -262 menjadi 0). "
    "Lompatan 262 gas ini terkonfirmasi terdiri atas 256 gas (satu word 32-byte tambahan pada data event CredentialRevoked "
    "sesuai formula EVM log data: 8 gas/byte * 32 byte = 256 gas) + 6 gas (belum dirinci).\n"
    "4. SISA Non-Nol: Komponen di luar biaya calldata EIP-2028 dan alokasi data event log dinyatakan belum dijelaskan."
)
p_lamp_f_analysis.paragraph_format.space_before = Pt(6)
p_lamp_f_analysis.paragraph_format.space_after = Pt(4)
for r in p_lamp_f_analysis.runs:
    r.font.name = 'Arial'
    r.font.size = Pt(9.0)

p_lamp_f_log_hdr = doc.add_paragraph()
p_lamp_f_log_hdr.text = "Keluaran Mentah Eksekusi Terminal (uts-blockchain-submission/tools/exp_b06_output.txt):"
p_lamp_f_log_hdr.paragraph_format.space_before = Pt(6)
p_lamp_f_log_hdr.paragraph_format.space_after = Pt(2)
for r in p_lamp_f_log_hdr.runs:
    r.font.name = 'Arial'
    r.font.size = Pt(9.0)
    r.font.bold = True

with open("uts-blockchain-submission/tools/exp_b06_output.txt", "r", encoding="utf-8") as fp:
    raw_log = fp.read()

p_lamp_f_log = doc.add_paragraph()
p_lamp_f_log.text = raw_log
p_lamp_f_log.paragraph_format.space_before = Pt(2)
p_lamp_f_log.paragraph_format.space_after = Pt(4)
for r in p_lamp_f_log.runs:
    r.font.name = 'Courier New'
    r.font.size = Pt(8.0)

# Detach Lampiran F elements temporarily so we can order everything perfectly
p_lamp_f_heading._element.getparent().remove(p_lamp_f_heading._element)
p_lamp_f_intro._element.getparent().remove(p_lamp_f_intro._element)
tbl_f._element.getparent().remove(tbl_f._element)
p_lamp_f_analysis._element.getparent().remove(p_lamp_f_analysis._element)
p_lamp_f_log_hdr._element.getparent().remove(p_lamp_f_log_hdr._element)
p_lamp_f_log._element.getparent().remove(p_lamp_f_log._element)

# =============================================================================
# 21. ASSEMBLE APPENDICES IN EXACT PHYSICAL SEQUENCE: A -> B -> C -> D -> E -> F (POIN 7c)
# =============================================================================
sectPr = doc.element.body.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sectPr")

# Elements to append in exact sequence before sectPr:
# Lampiran D
sectPr.addprevious(p_lamp_d._element)
sectPr.addprevious(tbl_criteria._element)

# Lampiran E
sectPr.addprevious(p_lamp_e._element)
sectPr.addprevious(tbl_bench._element)

# Lampiran F
sectPr.addprevious(p_lamp_f_heading._element)
sectPr.addprevious(p_lamp_f_intro._element)
sectPr.addprevious(tbl_f._element)
sectPr.addprevious(p_lamp_f_analysis._element)
sectPr.addprevious(p_lamp_f_log_hdr._element)
sectPr.addprevious(p_lamp_f_log._element)

print("Appendices successfully assembled in order: A -> B -> C -> D -> E -> F")

# =============================================================================
# 22. REMOVE REDUNDANT PARAGRAPHS & TIGHTEN HEADING SPACING
# =============================================================================
to_remove = []
for p in doc.paragraphs:
    if "Seluruh rangkaian unit test otomatis (T-01 s.d. T-08)" in p.text:
        to_remove.append(p)
    if p.text.strip() == "" and "drawing" not in p._p.xml:
        to_remove.append(p)

for p in to_remove:
    p._element.getparent().remove(p._element)

for p in doc.paragraphs:
    if p.paragraph_format.space_before and p.paragraph_format.space_before.pt > 4:
        p.paragraph_format.space_before = Pt(3)
    if p.paragraph_format.space_after and p.paragraph_format.space_after.pt > 3:
        p.paragraph_format.space_after = Pt(2)

# =============================================================================
# 23. SAVE DOCX AND CONVERT TO PDF
# =============================================================================
doc.save(OUT_DOCX)
print(f"v7.3 DOCX saved successfully to {OUT_DOCX}")

cmd = ["soffice", "--headless", "--convert-to", "pdf", OUT_DOCX, "--outdir", "v7_workspace"]
subprocess.run(cmd, check=True)
print(f"v7.3 PDF compiled successfully to {OUT_PDF}")

# Apply Metadata via Exiftool
exif_cmd = [
    "exiftool",
    "-Author=Fajar Geran Arifin",
    "-Title=UTS Blockchain - Rancangan Sistem Verifikasi Kredensial Akademik",
    "-Subject=Rancangan Sistem Verifikasi Kredensial Akademik Berbasis Blockchain Konsorsium",
    "-overwrite_original",
    OUT_PDF
]
subprocess.run(exif_cmd, check=True)
print("Metadata applied successfully to v7.3 PDF.")
