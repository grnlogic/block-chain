#!/usr/bin/env python3
"""Skrip otomatisasi untuk mereproduksi dokumen laporan naskah akhir v7.5 (.docx dan .pdf)."""

import os
import re
import subprocess
import docx
from docx.shared import Pt, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT

SRC_DOCX = "uts-blockchain-submission/Laporan_UTS_Blockchain_237006079.docx"
if not os.path.exists(SRC_DOCX):
    SRC_DOCX = "_arsip_kerja/Laporan_UTS_Blockchain_237006079.docx"
OUT_DOCX = "v7_workspace/Laporan_UTS_Blockchain_237006079_v7.5.docx"
OUT_PDF = "v7_workspace/Laporan_UTS_Blockchain_237006079_v7.5.pdf"

def parse_demo_log(filepath="prototype/results/demo-output.txt"):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Berkas log demo '{filepath}' tidak ditemukan.")
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    m_addr = re.search(r"Alamat Kontrak\s*:\s*(0x[a-fA-F0-9]{40})", text)
    assert m_addr, "Alamat kontrak tidak ditemukan di demo log."
    contract_addr = m_addr.group(1)

    m_tx_deploy = re.search(r"Tx Hash Deployment\s*:\s*(0x[a-fA-F0-9]{64})", text)
    assert m_tx_deploy, "Tx deployment tidak ditemukan di demo log."
    tx_deploy = m_tx_deploy.group(1)

    m_root = re.search(r"Merkle Root Terhitung\s*:\s*(0x[a-fA-F0-9]{64})", text) or \
             re.search(r"Root Tersimpan State\s*:\s*(0x[a-fA-F0-9]{64})", text)
    assert m_root, "Merkle root tidak ditemukan di demo log."
    merkle_root = m_root.group(1)

    m_tx_issue = re.search(r"Tx Hash Penerbitan\s*:\s*(0x[a-fA-F0-9]{64})", text)
    assert m_tx_issue, "Tx penerbitan tidak ditemukan di demo log."
    tx_issue = m_tx_issue.group(1)

    leaf_hashes = {}
    for i in range(1, 7):
        gid = f"G-{i:02d}"
        m_leaf = re.search(rf"\[{gid}\][^|]*\|[^|]*\|[^|]*\|\s*Leaf:\s*(0x[0-9a-fA-F]+)", text)
        assert m_leaf, f"Hash daun {gid} tidak ditemukan di demo log."
        leaf_hashes[gid] = m_leaf.group(1)

    m_orig = re.search(r"Leaf Asli\s*:\s*(0x[a-fA-F0-9]{64})", text)
    assert m_orig, "Leaf Asli tidak ditemukan di demo log."
    leaf_original = m_orig.group(1)

    m_tamper = re.search(r"Leaf Hasil Manipulasi\s*:\s*(0x[a-fA-F0-9]{64})", text)
    assert m_tamper, "Leaf Hasil Manipulasi tidak ditemukan di demo log."
    leaf_tampered = m_tamper.group(1)

    assert leaf_original.startswith(leaf_hashes["G-01"]), \
        f"Leaf Asli {leaf_original} tidak cocok dengan G-01 {leaf_hashes['G-01']}"

    return {
        "contract_addr": contract_addr,
        "tx_deploy": tx_deploy,
        "merkle_root": merkle_root,
        "tx_issue": tx_issue,
        "leaf_hashes": leaf_hashes,
        "leaf_original": leaf_original,
        "leaf_tampered": leaf_tampered,
    }

def replace_in_paragraph(p, old, new, preserve_format=True, counts=None):
    if old not in p.text:
        return False
    if counts is not None:
        counts[old] = counts.get(old, 0) + 1

    if not p.runs:
        p.text = p.text.replace(old, new)
        return True

    for r in p.runs:
        if old in r.text:
            r.text = r.text.replace(old, new)
            return True

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

def update_document_metadata(doc):
    doc.core_properties.author = "Fajar Geran Arifin"
    doc.core_properties.title = "UTS Blockchain - Rancangan Sistem Verifikasi Kredensial Akademik"

def update_footer(doc):
    for sec in doc.sections:
        for p in sec.footer.paragraphs:
            if "Template Laporan Kegiatan Blockchain" in p.text:
                p.text = "Laporan UTS Blockchain | TA 2026/2027"

def clear_table_cant_split(doc):
    for t in doc.tables:
        for r in t.rows:
            trPr = r._tr.get_or_add_trPr()
            cs = trPr.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}cantSplit")
            if cs is not None:
                trPr.remove(cs)

def update_section_headings(doc):
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

def compress_utxo_subchapter(doc):
    p_utxo_heading = None
    p_utxo_p1 = None
    p_utxo_p2 = None

    for i, p in enumerate(doc.paragraphs):
        if p.text.strip().startswith("4.4 Evaluasi Model UTXO Bitcoin"):
            p_utxo_heading = p
            if i + 1 < len(doc.paragraphs):
                p_utxo_p1 = doc.paragraphs[i + 1]
            if i + 2 < len(doc.paragraphs):
                p_utxo_p2 = doc.paragraphs[i + 2]
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

    tbl7_utxo = doc.tables[7]
    tbl7_utxo._element.getparent().remove(tbl7_utxo._element)

def extract_appendix_tables(doc):
    tbl_criteria = None
    tbl_bench = None
    for t in doc.tables:
        first_cell = t.rows[0].cells[0].text.strip()
        if "Kelompok Uji" in first_cell:
            tbl_criteria = t
        elif "Parameter Pengujian" in first_cell:
            tbl_bench = t

    tbl_criteria._element.getparent().remove(tbl_criteria._element)
    tbl_bench._element.getparent().remove(tbl_bench._element)

    p_lamp_d = doc.add_paragraph()
    p_lamp_d.text = "Lampiran D: Matriks Evaluasi Lengkap Kriteria Penerimaan dan Luaran OBE (T-01 s.d. T-08)"
    p_lamp_d.paragraph_format.space_before = Pt(14)
    p_lamp_d.paragraph_format.space_after = Pt(4)
    p_lamp_d.paragraph_format.keep_with_next = True
    for r in p_lamp_d.runs:
        r.font.name = "Arial"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)

    p_lamp_e = doc.add_paragraph()
    p_lamp_e.text = "Lampiran E: Rekapitulasi Lengkap Metrik Pengujian Performa 30 Run Terukur"
    p_lamp_e.paragraph_format.space_before = Pt(14)
    p_lamp_e.paragraph_format.space_after = Pt(4)
    p_lamp_e.paragraph_format.keep_with_next = True
    for r in p_lamp_e.runs:
        r.font.name = "Arial"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)

    p_lamp_d._element.getparent().remove(p_lamp_d._element)
    p_lamp_e._element.getparent().remove(p_lamp_e._element)

    return tbl_criteria, tbl_bench, p_lamp_d, p_lamp_e

def update_hardware_specifications(doc):
    t1 = doc.tables[1]
    for r in t1.rows:
        if "Perangkat Keras Node" in r.cells[0].text:
            r.cells[1].text = "12th Gen Intel(R) Core(TM) i5-12450H (8 fisik / 12 thread logis), RAM total 15 GiB (15.700.320 kB), OS Linux x86_64 Kernel 6.6"

def update_table_catatan_pelaksanaan(doc, demo_data):
    t2 = doc.tables[2]
    t2.rows[2].cells[2].text = (
        f"Kontrak aktif di alamat {demo_data['contract_addr'][:12]}..., "
        f"Tx: {demo_data['tx_deploy'][:10]}..., Gas: 1.039.368 unit [B-01]"
    )
    t2.rows[3].cells[2].text = (
        f"Pohon Merkle (129,44 ms off-chain, B-02); 6 daun bergaram, "
        f"Root: {demo_data['merkle_root'][:10]}... (Tabel 5, Diagram 3, results/demo-output.txt)"
    )
    t2.rows[4].cells[2].text = (
        f"Root terdaftar Block #2 tx {demo_data['tx_issue'][:10]}... [B-03]; verifikasi valid 0 gas [B-04]; "
        f"pencegahan non-issuer [B-05B]; pencabutan 56.359 gas [B-06]; jeda darurat 48.214 gas [B-07]"
    )
    t2.rows[5].cells[2].text = (
        "Gas eksekusi murni issueBatch konstan 164.911 gas (O(1)), bukti selisih calldata deterministik tepat 84 gas. "
        "Rujukan: B-08, Tabel 8, Lampiran D, Lampiran E (results/perf-output.txt)"
    )

def update_table_merkle_records(doc, demo_data):
    t5 = None
    for t in doc.tables:
        if "Record / Daun" in t.rows[0].cells[0].text:
            t5 = t
            break

    if t5 is not None:
        for idx in range(1, 7):
            gid = f"G-{idx:02d}"
            expected_leaf = demo_data["leaf_hashes"][gid]
            assert expected_leaf in t5.rows[idx].cells[3].text or expected_leaf[:16] in t5.rows[idx].cells[3].text, \
                f"Tabel 5 Row {idx} hash {t5.rows[idx].cells[3].text} does not match {expected_leaf}"
            t5.rows[idx].cells[3].text = f"{expected_leaf[:18]}... (32 byte)"

def update_table_evm_transaction(doc, demo_data):
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
                            r.font.name = "Calibri"
                            r.font.size = Pt(7.5)
            break

def apply_body_text_updates(doc, counts):
    for p in doc.paragraphs:
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

        if "guna menjamin hak penghapusan " in p.text:
            replace_in_paragraph(p, "guna menjamin hak penghapusan data pribadi (Right to Erasure, Pasal 8 dan Pasal 43 UU PDP) [10]", "guna mendukung hak penghapusan data pribadi (Right to Erasure, Pasal 8 dan Pasal 43 UU PDP) [10]", counts=counts)

        replace_in_paragraph(p, "3 validator utama", "6 node anggota konsorsium")
        replace_in_paragraph(p, "4 node konsorsium", "6 node anggota konsorsium")
        replace_in_paragraph(p, "Hyperledger Besu berprofil genesis", "Hyperledger Besu berprofil QBFT")

        if "Dengan desain ini, kepatuhan mutlak terh" in p.text:
            replace_in_paragraph(
                p,
                "Dengan desain ini, kepatuhan mutlak terhadap hak penghapusan data pribadi pada Pasal 8 serta kewajiban penghapusan pada Pasal 43 dan Pasal 44 UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP) [10] terpenuhi: jika alumni mengajukan hak penghapusan data, universitas dan alumni cukup memusnahkan dokumen lokal dan nilai salt, sehingga daun hash pada blockchain menjadi artefak komputasi acak semu yang mustahil direkonstruksi kembali (cryptographic erasure).",
                "Dengan desain ini, data pribadi tidak disimpan pada rantai; jika alumni menggunakan hak penghapusan (Pasal 8) atau pengendali data wajib menghapus dan memusnahkan data (Pasal 43 dan 44 UU No. 27 Tahun 2022 [10]), universitas dapat memusnahkan dokumen lokal dan nilai salt sehingga hash pada rantai dirancang tidak lagi mudah dikaitkan dengan subjek data; status hukum residu hash on-chain memerlukan telaah hukum lebih lanjut.",
                counts=counts
            )

        if "Standar W3C VC & Kepatuhan Hak Hapus:" in p.text:
            p_w3c = doc.add_paragraph()
            p_w3c.text = (
                "Batas lingkup prototipe: prototipe memvalidasi kanonikalisasi (RFC 8785), komitmen salted hash, "
                "pohon Merkle, dan verifikasi pada EVM. Envelope JSON-LD W3C VC v2.0, tanda tangan digital penerbit, "
                "dan DID resolver merupakan arsitektur rujukan target produksi dan belum diimplementasikan pada prototipe."
            )
            p_w3c.paragraph_format.space_before = Pt(3)
            p_w3c.paragraph_format.space_after = Pt(2)
            for r in p_w3c.runs:
                r.font.name = "Calibri"
                r.font.size = Pt(9.5)
            p._element.addnext(p_w3c._element)

        if "Kepatuhan Regulasi Privasi Data Pribadi (P3):" in p.text:
            p.text = (
                "Kepatuhan Regulasi Privasi Data Pribadi (P3): Desain ini secara ketat mematuhi ketentuan UU PDP No. 27/2022 [10] "
                "dan Permendikbudristek No. 6/2022 [13]. Data pribadi lulusan diklasifikasikan sebagai data spesifik dan umum (Pasal 4 ayat 3). "
                "Penyimpanan hash bergaram pada ledger publik memastikan hak penghapusan data (Right to Erasure, Pasal 8 UU PDP) "
                "serta kewajiban pengendali data untuk menghapus rekaman pribadi saat retensi berakhir (Pasal 43 ayat 1) dapat dipenuhi tanpa merusak "
                "integritas bukti penjangkaran Merkle. Pemrosesan data pribadi juga senantiasa berlandaskan dasar pemrosesan yang sah "
                "dan persetujuan eksplisit (Pasal 9 UU PDP)."
            )

        if "Pertimbangan Etika, Regulasi, & Roadmap:" in p.text:
            replace_in_paragraph(
                p,
                "Peraturan Menteri Pendidikan, Kebudayaan, Riset, dan Teknologi No. 6 Tahun 2022 tentang Ijazah, Sertifikat Kompetensi, dan Sertifikat Profesi Jenjang Pendidikan Tinggi, serta menjamin hak privasi alumni terlindungi sepenuhnya di bawah naungan UU No. 27 Tahun 2022 (UU PDP) [10].",
                "Peraturan Menteri Pendidikan, Kebudayaan, Riset, dan Teknologi Nomor 6 Tahun 2022 Tentang Ijazah, Sertifikat Kompetensi, Sertifikat Profesi, Gelar, dan Kesetaraan Ijazah Perguruan Tinggi Negara Lain [13], serta dirancang untuk mengurangi keterkaitan data pribadi; status hukum hash on-chain memerlukan telaah hukum lebih lanjut di bawah naungan UU No. 27 Tahun 2022 (UU PDP) [10].",
                counts=counts
            )

        if "• 1. Instant Finality: Ketunta" in p.text:
            replace_in_paragraph(
                p,
                "• 1. Instant Finality: Ketuntasan Mutlak Seketika (Deterministic Instant Finality): Sekali blok di-commit oleh 2F + 1 validator, blok tersebut mustahil mengalami reorg atau percabangan, memberikan kepastian hukum langsung bagi ijazah yang diterbitkan.",
                "• 1. Instant Finality: Ketuntasan Deterministik Seketika (Deterministic Instant Finality): Sekali blok di-commit oleh 2F + 1 validator, blok tersebut tidak mengalami reorg atau percabangan secara probabilistik, memberikan kepastian hukum langsung bagi ijazah yang diterbitkan.",
                counts=counts
            )

        if "sejalan dengan standar institusi pendidikan hijau" in p.text:
            replace_in_paragraph(
                p,
                ", sangat ramah lingkungan dan sejalan dengan standar institusi pendidikan hijau.",
                " dan sangat ramah lingkungan.",
                counts=counts
            )

        if "Perbandingan Toleransi Kesalahan:" in p.text:
            p.text = (
                "Perbandingan Toleransi Kesalahan: Model konsensus dievaluasi berdasarkan kebutuhan integritas ijazah nasional. "
                "Proof-of-Work (PoW) dieliminasi karena inefisiensi energi dan risiko 51% attack. Raft memiliki throughput tinggi "
                "tetapi rentan (Crash Fault Tolerant, tidak tahan serangan jahat). QBFT (IBFT 2.0) pada Hyperledger Besu dipilih "
                "karena menjamin toleransi kesalahan Byzantine hingga F < N/3 node jahat, dengan finalitas deterministik seketika (zero probabilistic fork)."
            )

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

        if "Kriteria penerimaan (acceptance criteria) disusun dengan merujuk pada standar ilmiah" in p.text:
            p.text = (
                "Kriteria penerimaan (acceptance criteria) disusun dengan merujuk pada standar ilmiah W3C VC [1], Ethereum JSON-RPC eth_call [2], "
                "OpenZeppelin Contracts v5 [3], Paten Pohon Merkle 1982 [4], Prinsip Least Privilege Saltzer-Schroeder 1975 [5], "
                "Keccak Reference [6], Nielsen Norman Group [7], W3C Bitstring Status List v1.0 [8], UU PDP No. 27/2022 [10], EIP-2028 [11], "
                "dan RFC 8785 [9]. Rincian matriks evaluasi lengkap kriteria penerimaan terhadap luaran OBE disajikan pada Lampiran D. "
                "Seluruh kriteria fungsional, keamanan, dan batas komputasi terpenuhi 100% pada lingkungan uji coba Hardhat."
            )

        if "Pengujian performa mendalam dilakukan melalui 30 run terukur" in p.text:
            p.text = (
                "Pengujian performa mendalam dilakukan melalui 30 run terukur (+ 2 run warm-up) pada skrip scripts/perf-benchmark.js "
                "untuk mengevaluasi konsumsi gas, panjang bukti pembuktian (proof length), waktu pembuatan Merkle tree, "
                "dan latensi verifikasi read-only (eth_call) pada tiga skala batch lulusan: N = 6, N = 100, dan N = 1.000. "
                "Rekapitulasi lengkap metrik statistik benchmark 30 run dirangkum pada Lampiran E."
            )

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

        replace_in_paragraph(p, "• 1. Lingkungan Node: Lingkungan Single-Node Hardhat:", "• 1. Lingkungan Single-Node In-Process:")
        replace_in_paragraph(p, "• 2. Data Uji: Data Sintetis Fiktif:", "• 2. Data Uji Sintetis:")
        replace_in_paragraph(p, "• 3. Perangkat Keras: Karakteristik Mesin Uji Tunggal:", "• 3. Karakteristik Mesin Uji Tunggal:")
        replace_in_paragraph(p, "• 4. Simulasi Gas: Hakikat Nilai estimateGas:", "• 4. Hakikat Nilai estimateGas:")
        replace_in_paragraph(p, "• 5. Slot Storage URI: Alokasi Slot Storage metadataURI:", "• 5. Alokasi Slot Storage metadataURI:")
        replace_in_paragraph(p, "• 5. Slot Storage URI: Alokasi Slot Storage URI:", "• 5. Alokasi Slot Storage metadataURI:")
        replace_in_paragraph(p, "• 6. Batas Gas Blok: Parameter Node Lokal Hardhat vs Hipotesis Konsorsium:", "• 6. Batas Gas Blok Node Lokal vs Konsorsium:")
        replace_in_paragraph(p, "• 7. Pembulatan Calldata: Efek Pembulatan Rata-Rata Calldata (83 vs 84 gas):", "• 7. Efek Pembulatan Calldata (83 vs 84 gas):")

        if "• 6. Batas Gas Blok" in p.text:
            p.text = (
                "• 6. Batas Gas Blok Node Lokal vs Konsorsium: Pengukuran aktual pada node lokal Hardhat melalui RPC "
                "eth_getBlockByNumber menghasilkan blockGasLimit sebesar 60.000.000 gas (0x3938700). Angka 30.000.000 gas "
                "dijadikan contoh hipotetis jaringan konsorsium untuk simulasi kapasitas blok. Penjangkaran individual "
                "1.000 ijazah (~20 juta gas) akan menyerap sepertiga (33,3%) dari batas blok 60 juta gas atau dua pertiga "
                "(66,7%) dari contoh hipotetis 30 juta gas, sedangkan skema Merkle batching pada prototipe ini hanya "
                "memerlukan 211.084 gas (< 0,36% dari batas blok 60 juta gas)."
            )

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
                r.font.name = "Arial"
                r.font.size = Pt(9.0)

def insert_limitations_and_b06(doc):
    for p in doc.paragraphs:
        if "• 7. Efek Pembulatan Calldata" not in p.text:
            continue

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
            r.font.name = "Arial"
            r.font.size = Pt(9.0)

        p_b09 = doc.add_paragraph()
        p_b09.text = (
            "• 9. Desain Pencabutan revokeCredential: revokeCredential(leafHash, batchId, reason) hanya memeriksa "
            "bahwa batchId terdaftar dan belum memeriksa bahwa leafHash merupakan anggota Merkle root batch tersebut; "
            "pilihan ini menghemat gas pencabut karena tidak perlu mengirim Merkle proof. Keamanan verifikasi tidak "
            "bergantung pada pemeriksaan itu: verifyCredential tetap mewajibkan Merkle proof yang valid dan memeriksa "
            "status pencabutan. Konsekuensinya, pemegang REVOKER_ROLE dapat mencatat hash yang bukan anggota batch; "
            "dampaknya terbatas pada hash tersebut, tindakan itu tercatat pada event CredentialRevoked, dan penerbitan "
            "serta pencabutan dapat dihentikan melalui Pausable. Pemeriksaan keanggotaan leaf saat pencabutan menjadi "
            "pengembangan lanjutan."
        )
        p_b09.paragraph_format.space_before = Pt(3)
        p_b09.paragraph_format.space_after = Pt(2)
        for r in p_b09.runs:
            r.font.name = "Arial"
            r.font.size = Pt(9.0)

        p_b10 = doc.add_paragraph()
        p_b10.text = (
            "• 10. Pengungkapan Dokumen Penuh: Prototipe menghitung satu daun Merkle dari seluruh isi kredensial "
            "(computeCredentialLeaf), sehingga verifikator menerima seluruh isi dokumen dan salt. Selective disclosure "
            "per field (daun dan salt per field) dirancang sebagai pengembangan lanjutan dan belum diimplementasikan."
        )
        p_b10.paragraph_format.space_before = Pt(3)
        p_b10.paragraph_format.space_after = Pt(2)
        for r in p_b10.runs:
            r.font.name = "Arial"
            r.font.size = Pt(9.0)

        p_b11 = doc.add_paragraph()
        p_b11.text = (
            "• 11. Pembuktian Kepemilikan: Prototipe memverifikasi integritas dan penerbit, belum memverifikasi bahwa "
            "penyaji adalah pemegang sah. Tanda tangan pemegang dengan challenge dari verifikator (mis. Verifiable "
            "Presentation) baru berupa rancangan."
        )
        p_b11.paragraph_format.space_before = Pt(3)
        p_b11.paragraph_format.space_after = Pt(2)
        for r in p_b11.runs:
            r.font.name = "Arial"
            r.font.size = Pt(9.0)

        p_b12 = doc.add_paragraph()
        p_b12.text = (
            "• 12. Cakupan Jenis Kredensial: Prototipe menguji data ijazah. Sertifikat kompetensi dan transkrip dirancang "
            "memakai mekanisme yang sama dengan atribut berbeda (properti type pada W3C VC) dan belum diuji."
        )
        p_b12.paragraph_format.space_before = Pt(3)
        p_b12.paragraph_format.space_after = Pt(2)
        for r in p_b12.runs:
            r.font.name = "Arial"
            r.font.size = Pt(9.0)

        p._element.addnext(p_b06._element)
        p_b06._element.addnext(p_b09._element)
        p_b09._element.addnext(p_b10._element)
        p_b10._element.addnext(p_b11._element)
        p_b11._element.addnext(p_b12._element)
        break

def update_bibliographic_references(doc):
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

    has_ref13 = any(p.text.startswith("[13]") for p in doc.paragraphs)
    if not has_ref13:
        last_ref_idx = None
        for idx, p in enumerate(doc.paragraphs):
            if p.text.startswith("[12]"):
                last_ref_idx = idx
                break
            elif p.text.startswith("[11]"):
                last_ref_idx = idx

        if last_ref_idx is not None:
            p13 = doc.add_paragraph()
            p13.text = (
                '[13] Kementerian Pendidikan, Kebudayaan, Riset, dan Teknologi Republik Indonesia, "Peraturan Menteri Pendidikan, '
                'Kebudayaan, Riset, dan Teknologi Nomor 6 Tahun 2022 Tentang Ijazah, Sertifikat Kompetensi, '
                'Sertifikat Profesi, Gelar, dan Kesetaraan Ijazah Perguruan Tinggi Negara Lain," Berita Negara Republik Indonesia '
                'Tahun 2022 Nomor 167, Jakarta, Feb. 2022. [Daring]. Tersedia: https://peraturan.go.id/id/permendikbudristek-no-6-tahun-2022. '
                '[Diakses: 5 Oktober 2026].'
            )
            p13.paragraph_format.space_before = Pt(2)
            p13.paragraph_format.space_after = Pt(2)
            for r in p13.runs:
                r.font.name = "Arial"
                r.font.size = Pt(8.5)
            doc.paragraphs[last_ref_idx]._element.addnext(p13._element)

def update_lampiran_a(doc):
    for i, p in enumerate(doc.paragraphs):
        if "Lampiran A: Pengungkapan Penggunaan Alat Bantu AI" not in p.text:
            continue
        for j in range(i + 1, min(i + 10, len(doc.paragraphs))):
            pj = doc.paragraphs[j]
            if "• 2. Google Antigravity Agent:" in pj.text:
                p_ai = doc.add_paragraph()
                p_ai.text = (
                    "• 3. Siklus Koreksi & Verifikasi Laporan (v7 s.d. v7.5): Tahap koreksi v7 sampai v7.5 "
                    "dikerjakan dengan agent (Google Antigravity) atas arahan saya, dan peninjauan serta penyusunan "
                    "instruksi koreksi dibantu Claude (asisten AI Anthropic); kode kontrak, hasil uji, dan angka "
                    "pengukuran tidak diubah."
                )
                p_ai.paragraph_format.space_before = Pt(2)
                p_ai.paragraph_format.space_after = Pt(2)
                for r in p_ai.runs:
                    r.font.name = "Arial"
                    r.font.size = Pt(8.5)
                pj._element.addnext(p_ai._element)
            if "• 3. Tanggung Jawab Penulis:" in pj.text:
                pj.text = pj.text.replace("• 3. Tanggung Jawab Penulis:", "• 4. Tanggung Jawab Penulis:")
                for r in pj.runs:
                    r.font.name = "Arial"
                    r.font.size = Pt(8.5)
        break

def insert_table_captions(doc):
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
        ("ID Tes", "Tabel 10. Ringkasan Hasil Eksekusi Pengujian Unit Test Otomatis (T-01 s.d. T-08)"),
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
                r.font.name = "Arial"
                r.font.size = Pt(9.5)
                r.font.bold = True
                r.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
            target_tbl._element.addprevious(p_cap._element)

def rescale_diagrams(doc, scale=0.80):
    for p in doc.paragraphs:
        for r in p.runs:
            extents = r._r.xpath(".//wp:extent")
            for ext in extents:
                cx = int(ext.attrib.get("cx", 0))
                cy = int(ext.attrib.get("cy", 0))
                if cy > 3000000:
                    ext.attrib["cx"] = str(int(cx * scale))
                    ext.attrib["cy"] = str(int(cy * scale))

def format_lampiran_d_e(tbl_criteria, tbl_bench):
    for t in [tbl_criteria, tbl_bench]:
        for r in t.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    for run in p.runs:
                        run.font.name = "Arial"
                        run.font.size = Pt(9.0)
                        if "30M gas" in run.text:
                            run.text = run.text.replace("30M gas", "60M gas node lokal / 30M gas contoh hipotetis konsorsium")

def verify_lampiran_b_hashes(doc, demo_data):
    for p in doc.paragraphs:
        if "Leaf Asli" in p.text and "Leaf Hasil Manipulasi" in p.text:
            assert demo_data["leaf_original"] in p.text, "Lampiran B tidak memuat hash Leaf Asli yang tepat."
            assert demo_data["leaf_tampered"] in p.text, "Lampiran B tidak memuat hash Leaf Hasil Manipulasi yang tepat."
            break

def configure_lampiran_c(doc):
    for p in doc.paragraphs:
        if "Lampiran C: Pernyataan Orisinalitas" in p.text:
            p.paragraph_format.page_break_before = True
            break

def construct_lampiran_f(doc):
    p_heading = doc.add_paragraph()
    p_heading.text = "Lampiran F: Eksperimen Isolasi Variabel Selisih Gas revokeCredential (B-06)"
    p_heading.paragraph_format.space_before = Pt(16)
    p_heading.paragraph_format.space_after = Pt(4)
    p_heading.paragraph_format.keep_with_next = True
    for r in p_heading.runs:
        r.font.name = "Arial"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)

    p_intro = doc.add_paragraph()
    p_intro.text = (
        "Eksperimen isolasi variabel tunggal (exp_b06_v2.js) dirancang untuk memverifikasi akar penyebab matematis "
        "perbedaan konsumsi gas fungsi revokeCredential antara skrip demo (56.359 gas pada Bukti B-06) dan hasil benchmark "
        "(55.297 s.d. 55.333 gas). Seluruh run dieksekusi pada smart contract yang sama (AcademicCredentialRegistry.sol), "
        "pemanggil yang sama (akun pencabut berwenang: revoker dengan peran REVOKER_ROLE), dan status state awal yang identik "
        "melalui mekanisme EVM snapshot/revert. Panjang parameter diukur secara eksak menggunakan Buffer.byteLength() dan "
        "komponen calldata dihitung sesuai aturan EIP-2028."
    )
    p_intro.paragraph_format.space_before = Pt(2)
    p_intro.paragraph_format.space_after = Pt(4)
    for r in p_intro.runs:
        r.font.name = "Arial"
        r.font.size = Pt(9.0)

    log_path = "uts-blockchain-submission/tools/exp_b06_output.txt"
    if not os.path.exists(log_path):
        log_path = "uts-blockchain-submission/pendukung/tools/exp_b06_output.txt"
    with open(log_path, "r", encoding="utf-8") as f:
        b06_text = f.read()

    assert "2212" in b06_text and "56359" in b06_text
    assert "2128" in b06_text and "56275" in b06_text
    assert "1496" in b06_text and "55381" in b06_text

    table_data = [
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
        ["Run E (Bench N=1000)", "BATCH-1000-ITER-1 (32 B, 17 non-0)", "Sidang Etik (11 B UTF-8)", "1.448 gas", "55.333 gas", "-1.026 gas", "-764 gas", "-262 gas"],
    ]

    tbl_f = doc.add_table(rows=len(table_data), cols=len(table_data[0]))
    tbl_f.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(table_data):
        for c_idx, text in enumerate(row):
            cell = tbl_f.cell(r_idx, c_idx)
            cell.text = text
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                for r in p.runs:
                    r.font.name = "Arial"
                    r.font.size = Pt(8.0)
                    if r_idx == 0:
                        r.font.bold = True

    p_analysis = doc.add_paragraph()
    p_analysis.text = (
        "Analisis Hasil Eksperimen dan Temuan Matematis Terukur:\n"
        "1. Resolusi Panjang String: String reason demo terkonfirmasi berukuran tepat 60 karakter / 60 byte UTF-8 "
        "(perbedaan dengan angka 61 pada laporan sebelumnya terselesaikan sebagai salah hitung manual).\n"
        "2. Variasi batchId (Run B): Perubahan batchId dari format demo ke benchmark menghasilkan selisih tepat -84 gas, "
        "yang 100% cocok dengan penurunan 7 byte non-nol calldata EIP-2028 (7 * 12 gas = 84 gas) dengan SISA = 0 gas.\n"
        "3. Lompatan Batas 32-Byte Event Log Data (Run D): Pada pengujian Run D, saat panjang string reason dinaikkan dari "
        "32 byte menjadi 33 byte, terjadi lonjakan tepat 262 gas pada komponen non-calldata (nilai SISA berubah dari -262 menjadi 0). "
        "Lompatan 262 gas ini terkonfirmasi terdiri atas 256 gas (satu word 32 byte tambahan data log; 8 gas x 32) ditambah 6 gas yang belum dirinci.\n"
        "4. SISA Non-Nol: Komponen di luar biaya calldata EIP-2028 dan alokasi data event log dinyatakan belum dijelaskan."
    )
    p_analysis.paragraph_format.space_before = Pt(6)
    p_analysis.paragraph_format.space_after = Pt(4)
    for r in p_analysis.runs:
        r.font.name = "Arial"
        r.font.size = Pt(9.0)

    p_log_hdr = doc.add_paragraph()
    p_log_hdr.text = f"Keluaran Mentah Eksekusi Terminal ({log_path}):"
    p_log_hdr.paragraph_format.space_before = Pt(6)
    p_log_hdr.paragraph_format.space_after = Pt(2)
    for r in p_log_hdr.runs:
        r.font.name = "Arial"
        r.font.size = Pt(9.0)
        r.font.bold = True

    p_log = doc.add_paragraph()
    p_log.text = b06_text
    p_log.paragraph_format.space_before = Pt(2)
    p_log.paragraph_format.space_after = Pt(4)
    for r in p_log.runs:
        r.font.name = "Courier New"
        r.font.size = Pt(8.0)

    p_heading._element.getparent().remove(p_heading._element)
    p_intro._element.getparent().remove(p_intro._element)
    tbl_f._element.getparent().remove(tbl_f._element)
    p_analysis._element.getparent().remove(p_analysis._element)
    p_log_hdr._element.getparent().remove(p_log_hdr._element)
    p_log._element.getparent().remove(p_log._element)

    return [p_heading, p_intro, tbl_f, p_analysis, p_log_hdr, p_log]

def assemble_document_appendices(doc, appendix_elements):
    sectPr = doc.element.body.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sectPr")
    for el in appendix_elements:
        sectPr.addprevious(el._element)

def clean_paragraphs_and_spacing(doc):
    to_remove = []
    for p in doc.paragraphs:
        if "Seluruh rangkaian unit test otomatis (T-01 s.d. T-08)" in p.text:
            to_remove.append(p)
        elif p.text.strip() == "" and "drawing" not in p._p.xml:
            to_remove.append(p)

    for p in to_remove:
        p._element.getparent().remove(p._element)

    for p in doc.paragraphs:
        if p.paragraph_format.space_before and p.paragraph_format.space_before.pt > 4:
            p.paragraph_format.space_before = Pt(3)
        if p.paragraph_format.space_after and p.paragraph_format.space_after.pt > 3:
            p.paragraph_format.space_after = Pt(2)

def export_docx_and_pdf(doc, out_docx, out_pdf):
    doc.save(out_docx)
    print(f"DOCX tersimpan di {out_docx}")

    cmd = ["soffice", "--headless", "--convert-to", "pdf", out_docx, "--outdir", os.path.dirname(out_pdf)]
    subprocess.run(cmd, check=True)
    print(f"PDF terkompilasi di {out_pdf}")

    exif_cmd = [
        "exiftool",
        "-Author=Fajar Geran Arifin",
        "-Title=UTS Blockchain - Rancangan Sistem Verifikasi Kredensial Akademik",
        "-Subject=Rancangan Sistem Verifikasi Kredensial Akademik Berbasis Blockchain Konsorsium",
        "-overwrite_original",
        out_pdf
    ]
    subprocess.run(exif_cmd, check=True)
    print("Metadata PDF berhasil diterapkan.")

def main():
    print(f"Membaca berkas dasar: {SRC_DOCX}")
    doc = docx.Document(SRC_DOCX)
    demo_data = parse_demo_log()

    update_document_metadata(doc)
    update_footer(doc)
    clear_table_cant_split(doc)
    update_section_headings(doc)
    compress_utxo_subchapter(doc)

    tbl_criteria, tbl_bench, p_lamp_d, p_lamp_e = extract_appendix_tables(doc)

    update_hardware_specifications(doc)
    update_table_catatan_pelaksanaan(doc, demo_data)
    update_table_merkle_records(doc, demo_data)
    update_table_evm_transaction(doc, demo_data)

    counts = {}
    apply_body_text_updates(doc, counts)
    insert_limitations_and_b06(doc)
    update_bibliographic_references(doc)
    update_lampiran_a(doc)
    insert_table_captions(doc)
    rescale_diagrams(doc, scale=0.80)
    format_lampiran_d_e(tbl_criteria, tbl_bench)
    verify_lampiran_b_hashes(doc, demo_data)
    configure_lampiran_c(doc)

    lamp_f_elements = construct_lampiran_f(doc)

    appendix_elements = [
        p_lamp_d,
        tbl_criteria,
        p_lamp_e,
        tbl_bench,
    ] + lamp_f_elements

    assemble_document_appendices(doc, appendix_elements)
    clean_paragraphs_and_spacing(doc)
    export_docx_and_pdf(doc, OUT_DOCX, OUT_PDF)

if __name__ == "__main__":
    main()
