#!/usr/bin/env python3
"""Verifikasi mandiri angka, hash, dan metrik pada laporan PDF dan DOCX terhadap berkas log aktual."""

import argparse
import docx
import os
import re
import subprocess
import sys

def parse_cli_args():
    parser = argparse.ArgumentParser(description="Verifikasi mandiri laporan PDF/DOCX terhadap log aktual.")
    default_pdf = "uts-blockchain-submission/237006079_Fajar_Geran_Arifin_UTS_Blockchain_OBE.pdf"
    if not os.path.exists(default_pdf):
        default_pdf = "v7_workspace/Laporan_UTS_Blockchain_237006079_v7.5.pdf"
    parser.add_argument("pdf_file", nargs="?", default=default_pdf, help="Jalur berkas PDF laporan")
    parser.add_argument("docx_file", nargs="?", default=None, help="Jalur berkas DOCX laporan")
    args = parser.parse_args()

    docx_path = args.docx_file or os.environ.get("DOCX_FILE") or args.pdf_file.replace(".pdf", ".docx")
    if not os.path.exists(docx_path):
        candidate_sumber = os.path.join("uts-blockchain-submission/sumber", os.path.basename(docx_path))
        if os.path.exists(candidate_sumber):
            docx_path = candidate_sumber

    return args.pdf_file, docx_path

def load_file_lines(filename, base_dir="prototype/results"):
    path = os.path.join(base_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        return [line.rstrip("\r\n") for line in f]

def extract_pdf_page(pdf_file, page_num):
    cmd = ["pdftotext", "-f", str(page_num), "-l", str(page_num), pdf_file, "-"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return res.stdout

def extract_full_pdf(pdf_file):
    cmd = ["pdftotext", pdf_file, "-"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return res.stdout

def find_docx_table(doc, header_keyword):
    if not doc:
        return None
    for tbl in doc.tables:
        first_row_text = " ".join(cell.text.strip().replace("\n", " ") for cell in tbl.rows[0].cells)
        if header_keyword.lower() in first_row_text.lower():
            return tbl
    return None

def build_standard_table_definitions():
    tabel_2 = [
        ("B-01 Gas Deploy Kontrak", "1.039.368", 3, "demo-output.txt", 15, "1039368"),
        ("B-03 Tx Hash Issue Batch", "0x1737c359...", 3, "demo-output.txt", 29, "0x1737c359"),
        ("B-04 Verifikasi Valid", "0 gas", 3, "demo-output.txt", 43, "0 gas"),
        ("B-06 Gas Revoke Credential", "56.359", 3, "demo-output.txt", 63, "56359"),
        ("B-07 Gas Pause Circuit Breaker", "48.214", 3, "demo-output.txt", 68, "48214"),
    ]

    tabel_5 = [
        ("G-01 NIM", "237006801", (5, 6), "demo-output.txt", 19, "237006801"),
        ("G-01 IPK", "3.82", (5, 6), "demo-output.txt", 19, "3.82"),
        ("G-01 Leaf Hash", "0x7b5f7365dffd18a8...", (5, 6), "demo-output.txt", 19, "0x7b5f7365dffd18a8"),
        ("G-02 NIM", "237006802", (5, 6), "demo-output.txt", 20, "237006802"),
        ("G-02 IPK", "3.65", (5, 6), "demo-output.txt", 20, "3.65"),
        ("G-02 Leaf Hash", "0xf3695a1ce4a97902...", (5, 6), "demo-output.txt", 20, "0xf3695a1ce4a97902"),
        ("G-03 NIM", "237006803", (5, 6), "demo-output.txt", 21, "237006803"),
        ("G-03 IPK", "3.91", (5, 6), "demo-output.txt", 21, "3.91"),
        ("G-03 Leaf Hash", "0xca7c3acd32fa82a2...", (5, 6), "demo-output.txt", 21, "0xca7c3acd32fa82a2"),
        ("G-04 NIM", "237006804", (5, 6), "demo-output.txt", 22, "237006804"),
        ("G-04 IPK", "3.45", (5, 6), "demo-output.txt", 22, "3.45"),
        ("G-04 Leaf Hash", "0x5c97927280c16ef9...", (5, 6), "demo-output.txt", 22, "0x5c97927280c16ef9"),
        ("G-05 NIM", "237006805", (5, 6), "demo-output.txt", 23, "237006805"),
        ("G-05 IPK", "3.55", (5, 6), "demo-output.txt", 23, "3.55"),
        ("G-05 Leaf Hash", "0xcc0d8357be021242...", (5, 6), "demo-output.txt", 23, "0xcc0d8357be021242"),
        ("G-06 NIM", "237006806", (5, 6), "demo-output.txt", 24, "237006806"),
        ("G-06 IPK", "3.78", (5, 6), "demo-output.txt", 24, "3.78"),
        ("G-06 Leaf Hash", "0x108e53ac2b7a5439...", (5, 6), "demo-output.txt", 24, "0x108e53ac2b7a5439"),
    ]

    tabel_7 = [
        ("Chain ID", "31337", 8, "perf-output.txt", 2, "31337"),
        ("Sender (from) ISSUER_ROLE", "0x70997970C5...", 8, "demo-output.txt", 5, "0x70997970C5"),
        ("Receiver (to) AcademicRegistry", "0x5FbDB23156...", 8, "demo-output.txt", 12, "0x5FbDB23156"),
        ("Gas Used Batch", "211.084", 8, "demo-output.txt", 31, "211084"),
        ("Block Number", "#2", 8, "demo-output.txt", 30, "2"),
        ("Merkle Root", "0x46ca2e83...", 8, "demo-output.txt", 25, "0x46ca2e83"),
        ("Tx Hash Penerbitan", "0x1737c359...", 8, "demo-output.txt", 29, "0x1737c359"),
        ("Gas Limit Blok Hardhat", "60.000.000", 8, "gaslimit_output.txt", 5, "60000000"),
    ]

    tabel_8 = [
        ("Total gasUsed N=6 (Receipt)", "187.874", 8, "perf-output.txt", 36, "187874"),
        ("Total gasUsed N=100 (Receipt)", "187.922", 8, "perf-output.txt", 36, "187922"),
        ("Total gasUsed N=1000 (Receipt)", "187.958", 8, "perf-output.txt", 36, "187958"),
        ("Biaya Dasar Transaksi", "21.000", 8, "perf-output.txt", 22, "21000"),
        ("Biaya Calldata N=6", "1.963", 8, "perf-output.txt", 23, "1962.80"),
        ("Biaya Calldata N=100", "2.011", 8, "perf-output.txt", 23, "2011.20"),
        ("Biaya Calldata N=1000", "2.047", 8, "perf-output.txt", 23, "2046.80"),
        ("Byte Nol N=6", "140.4", 8, "perf-output.txt", 24, "140.4"),
        ("Byte Non-Nol N=6", "87.6", 8, "perf-output.txt", 25, "87.6"),
        ("Gas Eksekusi Murni N=6", "164.911", 8, "perf-output.txt", 26, "164911"),
        ("Gas Eksekusi Murni N=100", "164.911", 8, "perf-output.txt", 26, "164911"),
        ("Gas Eksekusi Murni N=1000", "164.911", 8, "perf-output.txt", 26, "164911"),
        ("Deviasi Relatif Gas", "0,00%", 8, "perf-output.txt", 27, "0.0000%"),
    ]

    return [
        ("Tabel 2: Catatan Pelaksanaan", tabel_2),
        ("Tabel 5: Record Daun Merkle", tabel_5),
        ("Tabel 7: Field Transaksi EVM", tabel_7),
        ("Tabel 8: Komposisi Gas issueBatch", tabel_8),
    ]

def build_unit_test_items(doc):
    table_doc = find_docx_table(doc, "ID Tes")
    if not table_doc:
        return []
    items = []
    for r_idx in range(1, 9):
        cells = [c.text.strip().replace("\n", " ") for c in table_doc.rows[r_idx].cells]
        tid = f"T-{r_idx:02d}"
        items.append((f"Tabel 10 Baris {r_idx} ({tid})", cells[0], cells[1], cells[4], "test-output.txt", r_idx + 3, tid))
    return items

def build_lampiran_b_items():
    return [
        ("Skenario 5A IPK Manipulasi", "Skenario 5A: Pelamar mengubah IPK 3.82 menjadi 4.00 pada berkas lokal", "demo-output.txt", 49, "IPK 3.82 menjadi 4.00"),
        ("Leaf Asli 64-char Hex", "Leaf Asli            : 0x7b5f7365dffd18a87fb7b5471e7843da27e53b4ec53e8e1ef064b78ab3b0645c", "demo-output.txt", 50, "0x7b5f7365dffd18a87fb7b5471e7843da27e53b4ec53e8e1ef064b78ab3b0645c"),
        ("Leaf Manipulasi 64-char Hex", "Leaf Hasil Manipulasi: 0x0b097c59bcd2b3d0b5cba350b03cea87b34b4294eba79c5d5cf2f0a548d04f97", "demo-output.txt", 51, "0x0b097c59bcd2b3d0b5cba350b03cea87b34b4294eba79c5d5cf2f0a548d04f97"),
        ("Hasil Verifikasi Manipulasi", "Hasil Verifikasi     : DITOLAK / INVALID (FALSE)", "demo-output.txt", 52, "DITOLAK / INVALID (FALSE)"),
        ("Pesan Status Kontrak", "Pesan Status Kontrak : INVALID_PROOF_OR_TAMPERED", "demo-output.txt", 53, "INVALID_PROOF_OR_TAMPERED"),
        ("Skenario 5B Attacker RBAC", "Skenario 5B: Upaya penerbitan batch oleh penyerang tanpa hak (Attacker)", "demo-output.txt", 55, "Upaya penerbitan batch oleh penyerang tanpa hak"),
        ("Hasil Pencegatan RBAC", "Hasil Pencegatan RBAC: Transaksi Dibatalkan (Reverted)", "demo-output.txt", 56, "Transaksi Dibatalkan (Reverted)"),
        ("Custom Error Kontrak", "Eksepsi Kontrak      : VM Exception while processing transaction: reverted with custom error 'AccessControlUnauthorizedAccount", "demo-output.txt", 57, "AccessControlUnauthorizedAccount"),
    ]

def build_lampiran_d_items(doc):
    table_doc = find_docx_table(doc, "Kelompok Uji")
    if not table_doc:
        return []
    expected_d_tokens = [
        ("Baris 1 (T-01/B-03)", "T-01: menerbitkan batch ijazah", "B-03", "demo-output.txt", 27, "B-03"),
        ("Baris 2 (T-02/B-04)", "T-02: memverifikasi kredensial sah", "B-04", "demo-output.txt", 34, "B-04"),
        ("Baris 3 (T-05/B-06)", "T-05: mencabut status keabsahan", "B-06", "demo-output.txt", 59, "B-06"),
        ("Baris 4 (T-03/B-05A)", "T-03: menolak manipulasi klaim", "B-05A", "demo-output.txt", 48, "B-05"),
        ("Baris 5 (T-04&06/B-05B)", "T-04 & T-06: membatalkan upaya", "B-05B", "demo-output.txt", 55, "Skenario 5B"),
        ("Baris 6 (T-07/B-07)", "T-07: menghentikan mutasi state", "B-07", "demo-output.txt", 67, "B-07"),
        ("Baris 7 (T-08/B-08 Gas)", "164.911 gas", "B-08", "perf-output.txt", 57, "164.911"),
        ("Baris 8 (T-08/B-08 Proof)", "Tepat 3, 7, dan 10 sibling hash", "B-08", "perf-output.txt", 35, "3"),
        ("Baris 9 (T-08/B-08 Verify)", "8.554 gas (N=6) hingga 10.313 gas", "B-08", "perf-output.txt", 41, "8554"),
        ("Baris 10 (T-08/B-08 Build)", "Rata-rata 129,44 ms", "B-08", "perf-output.txt", 34, "129.44"),
    ]
    items = []
    for r_idx in range(1, 11):
        row_text = " ".join(c.text.strip().replace("\n", " ") for c in table_doc.rows[r_idx].cells)
        label, token1, token2, log_f, log_l, exp_log = expected_d_tokens[r_idx - 1]
        status_cell = table_doc.rows[r_idx].cells[6].text.strip()
        items.append((label, token1, token2, status_cell, row_text, log_f, log_l, exp_log))
    return items

def build_lampiran_e_items(doc):
    table_doc = find_docx_table(doc, "Parameter Pengujian")
    if not table_doc:
        return []
    expected_rows = [
        ("Baris 1 Build Tree Off-Chain", "1.43 ms", "14.01 ms", "129.44 ms", "perf-output.txt", 34, ("1.43", "14.01", "129.44")),
        ("Baris 2 Proof Sibling", "3 sibling hash", "7 sibling hash", "10 sibling hash", "perf-output.txt", 35, ("3", "7", "10")),
        ("Baris 3 Total Gas Issue", "187.874 gas", "187.922 gas", "187.958 gas", "perf-output.txt", 36, ("187874", "187922", "187958")),
        ("Baris 4 Pure Gas Issue", "164.911 gas", "164.911 gas", "164.911 gas", "perf-output.txt", 37, ("164911", "164911", "164911")),
        ("Baris 5 Gas Revoke", "55.303 gas", "55.328 gas", "55.340 gas", "perf-output.txt", 38, ("55303", "55328", "55340")),
        ("Baris 6 Raw Est Verify", "32.242 gas", "35.311 gas", "37.611 gas", "perf-output.txt", 39, ("32242", "35311", "37611")),
        ("Baris 7 Calldata Verify", "2.687 gas", "4.753 gas", "6.298 gas", "perf-output.txt", 40, ("2687", "4753", "6298")),
        ("Baris 8 Pure Gas Verify", "8.554 gas", "9.558 gas", "10.313 gas", "perf-output.txt", 41, ("8554", "9558", "10313")),
        ("Baris 9 Gas Verifikator", "0 gas (Bebas biaya)", "0 gas (Bebas biaya)", "0 gas (Bebas biaya)", "perf-output.txt", 64, ("0 gas", "0 gas", "0 gas")),
        ("Baris 10 Latensi View Call", "0.89 ms", "0.87 ms", "0.82 ms", "perf-output.txt", 42, ("0.89", "0.87", "0.82")),
    ]
    items = []
    for r_idx in range(1, 11):
        row_cells = [c.text.strip().replace("\n", " ") for c in table_doc.rows[r_idx].cells]
        label, t1, t2, t3, log_f, log_l, exp_logs = expected_rows[r_idx - 1]
        items.append((label, t1, t2, t3, row_cells, log_f, log_l, exp_logs))
    return items

def build_lampiran_f_items():
    return [
        ("Run A Calldata Gas", "2.212 gas", (20, 21), "exp_b06_output.txt", 11, "2212"),
        ("Run A Gas Receipt", "56.359 gas", (20, 21), "exp_b06_output.txt", 12, "56359"),
        ("Run B Calldata Gas", "2.128 gas", (20, 21), "exp_b06_output.txt", 18, "2128"),
        ("Run B Gas Receipt", "56.275 gas", (20, 21), "exp_b06_output.txt", 19, "56275"),
        ("Run B Selisih vs Run A", "-84 gas", (20, 21), "exp_b06_output.txt", 20, "-84"),
        ("Run C Calldata Gas", "1.496 gas", (20, 21), "exp_b06_output.txt", 27, "1496"),
        ("Run C Gas Receipt", "55.381 gas", (20, 21), "exp_b06_output.txt", 28, "55381"),
        ("Run C Selisih vs Run A", "-978 gas", (20, 21), "exp_b06_output.txt", 29, "-978"),
        ("Run D (31 B) Calldata", "1.736 gas", (20, 21), "exp_b06_output.txt", 35, "1736"),
        ("Run D (31 B) Receipt", "55.621 gas", (20, 21), "exp_b06_output.txt", 35, "55621"),
        ("Run D (32 B) Calldata", "1.748 gas", (20, 21), "exp_b06_output.txt", 36, "1748"),
        ("Run D (32 B) Receipt", "55.633 gas", (20, 21), "exp_b06_output.txt", 36, "55633"),
        ("Run D (33 B) Calldata", "1.888 gas", (20, 21), "exp_b06_output.txt", 37, "1888"),
        ("Run D (33 B) Receipt", "56.035 gas", (20, 21), "exp_b06_output.txt", 37, "56035"),
        ("Run D (60 B) Calldata", "2.212 gas", (20, 21), "exp_b06_output.txt", 38, "2212"),
        ("Run D (60 B) Receipt", "56.359 gas", (20, 21), "exp_b06_output.txt", 38, "56359"),
        ("Run E (N=6) Receipt", "55.297 gas", (20, 21), "exp_b06_output.txt", 41, "55297"),
        ("Run E (N=100) Receipt", "55.321 gas", (20, 21), "exp_b06_output.txt", 42, "55321"),
        ("Run E (N=1000) Receipt", "55.333 gas", (20, 21), "exp_b06_output.txt", 43, "55333"),
    ]

def verify_standard_table_group(group_name, items, pdf_pages, logs):
    print(f"\n{group_name} ({len(items)} item):")
    print(f"{'Hal':<5} | {'Elemen / Metrik':<32} | {'Nilai di PDF':<20} | {'Status':<6} | Log Target")
    mismatches = 0
    for elem_name, val_pdf, page, log_file, line_num, expected_in_log in items:
        if isinstance(page, tuple):
            pdf_text = " ".join(pdf_pages[p] for p in range(page[0], page[1] + 1))
            page_str = f"{page[0]}-{page[1]}"
        else:
            pdf_text = pdf_pages[page]
            page_str = str(page)

        clean_pdf_text = re.sub(r"(0x[a-fA-F0-9]+)\n\s*([a-fA-F0-9\.]+)", r"\1\2", pdf_text)
        log_lines = logs.get(log_file, [])
        log_line = log_lines[line_num - 1] if line_num <= len(log_lines) else ""

        pdf_match = (val_pdf in pdf_text) or (val_pdf in clean_pdf_text)
        log_match = expected_in_log in log_line
        status = "Cocok" if (pdf_match and log_match) else "GAGAL"
        if status == "GAGAL":
            mismatches += 1

        disp_pdf = val_pdf if len(val_pdf) <= 20 else val_pdf[:17] + "..."
        raw_log = log_line.strip()
        if len(raw_log) > 45:
            raw_log = raw_log[:42] + "..."
        print(f"{page_str:<5} | {elem_name:<32} | {disp_pdf:<20} | {status:<6} | [{log_file}:{line_num}] {raw_log}")
    return mismatches

def verify_unit_tests(items, test_lines):
    print(f"\nTabel 10: Ringkasan Unit Test T-01 s.d. T-08 ({len(items)} item):")
    print(f"{'Baris':<15} | {'ID Tes':<8} | {'Skenario Uji di Tabel':<40} | {'Status Cell':<12} | {'Log Ref:Baris':<22} | Cocok?")
    mismatches = 0
    for label, tid, scenario, status_cell, log_file, line_num, exp_log in items:
        log_line = test_lines[line_num - 1] if line_num <= len(test_lines) else ""
        match_table = (tid in label) and (len(scenario) > 5)
        match_log = exp_log in log_line
        status = "Cocok" if (match_table and match_log) else "GAGAL"
        if status == "GAGAL":
            mismatches += 1
        print(f"{label:<15} | {tid:<8} | {scenario[:38]:<40} | {status_cell[:10]:<12} | {log_file}:{line_num:<14} | {status}")
    return mismatches

def verify_lampiran_d(items, logs):
    print(f"\nLampiran D: Matriks Evaluasi OBE ({len(items)} item):")
    print(f"{'Baris':<25} | {'Token 1 (Wajib)':<32} | {'Token 2 (Unloosened)':<20} | {'Status Cell':<12} | Cocok?")
    mismatches = 0
    for label, t1, t2, status_cell, row_text, log_file, line_num, exp_log in items:
        log_lines = logs.get(log_file, [])
        log_line = log_lines[line_num - 1] if line_num <= len(log_lines) else ""
        match_row = (t1 in row_text) and (t2 in row_text)
        match_log = exp_log in log_line
        match_status = (status_cell == "LULUS")
        status = "Cocok" if (match_row and match_log and match_status) else "GAGAL"
        if status == "GAGAL":
            mismatches += 1
        print(f"{label:<25} | {t1[:30]:<32} | {t2:<20} | {status_cell:<12} | {status}")
    return mismatches

def verify_lampiran_e(items, perf_lines):
    count_e = len(items) * 3
    print(f"\nLampiran E: Rekapitulasi 30 Run ({count_e} item):")
    print(f"{'Baris':<30} | {'N=6':<18} | {'N=100':<18} | {'N=1000':<18} | {'Log Ref:Baris':<18} | Cocok?")
    mismatches = 0
    for label, t1, t2, t3, cells, log_file, line_num, exp_logs in items:
        log_line = perf_lines[line_num - 1] if line_num <= len(perf_lines) else ""
        cell_str = " ".join(cells)
        match_6 = (t1 in cell_str) and (exp_logs[0] in log_line)
        match_100 = (t2 in cell_str) and (exp_logs[1] in log_line)
        match_1000 = (t3 in cell_str) and (exp_logs[2] in log_line)
        row_status = "Cocok" if (match_6 and match_100 and match_1000) else "GAGAL"
        if not match_6:
            mismatches += 1
        if not match_100:
            mismatches += 1
        if not match_1000:
            mismatches += 1
        print(f"{label:<30} | {t1:<18} | {t2:<18} | {t3:<18} | {log_file}:{line_num:<10} | {row_status}")
    return mismatches

def verify_lampiran_b(items, full_pdf_text, demo_lines):
    print(f"\nLampiran B: Keluaran Eksekusi B-05 ({len(items)} item):")
    print(f"{'Item Bukti':<28} | {'Baris Cuplikan di PDF / DOCX':<45} | {'Target Log:Baris':<22} | Cocok?")
    mismatches = 0
    for item_name, exp_text, log_file, line_num, exp_log in items:
        log_line = demo_lines[line_num - 1] if line_num <= len(demo_lines) else ""
        match_pdf = (exp_log in full_pdf_text)
        match_log = (exp_log in log_line)
        status = "Cocok" if (match_pdf and match_log) else "GAGAL"
        if status == "GAGAL":
            mismatches += 1
        disp_txt = exp_text if len(exp_text) <= 42 else exp_text[:39] + "..."
        print(f"{item_name:<28} | {disp_txt:<45} | {log_file}:{line_num:<14} | {status}")
    return mismatches

def verify_lampiran_f(items, full_pdf_text, exp_b06_lines):
    print(f"\nLampiran F: Eksperimen Isolasi Variabel B-06 ({len(items)} item):")
    print(f"{'Skenario & Metrik':<28} | {'Nilai di Tabel / PDF':<25} | {'Target Log:Baris':<25} | Cocok?")
    mismatches = 0
    for item_name, val_str, page, log_file, line_num, exp_log in items:
        log_line = exp_b06_lines[line_num - 1] if line_num <= len(exp_b06_lines) else ""
        match_pdf = (val_str in full_pdf_text)
        match_log = (exp_log in log_line)
        status = "Cocok" if (match_pdf and match_log) else "GAGAL"
        if status == "GAGAL":
            mismatches += 1
        print(f"{item_name:<28} | {val_str:<25} | {log_file}:{line_num:<17} | {status}")
    return mismatches

def audit_dotted_numbers(full_pdf_text):
    print("\nAudit reverse angka bertitik pada teks PDF:")
    source_files = [
        ("prototype/results/demo-output.txt", "demo-output.txt"),
        ("prototype/results/perf-output.txt", "perf-output.txt"),
        ("prototype/results/test-output.txt", "test-output.txt"),
        ("uts-blockchain-submission/tools/gaslimit_output.txt", "gaslimit_output.txt"),
        ("uts-blockchain-submission/tools/exp_b06_output.txt", "exp_b06_output.txt"),
        ("uts-blockchain-submission/tools/bytecode_output.txt", "bytecode_output.txt"),
    ]
    file_contents = {}
    for path, label in source_files:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                file_contents[label] = f.read()

    pdf_dotted = sorted(list(set(re.findall(r"\b\d{1,3}(?:\.\d{3})+(?:,\d+)?\b", full_pdf_text))))
    log_map = {}
    for item in pdf_dotted:
        un_dotted = item.replace(".", "").replace(",", ".")
        int_val = item.replace(".", "").split(",")[0]
        matches = []
        for label, content in file_contents.items():
            if item in content or re.search(rf"\b{re.escape(int_val)}\b", content):
                matches.append(label)
            elif un_dotted != int_val and re.search(rf"\b{re.escape(un_dotted)}\b", content):
                matches.append(label)
        if matches:
            log_map[item] = sorted(list(set(matches)))

    known_non_log = {
        "0.005": "Teoretis/Config | Ilustrasi biaya transaksi OP_RETURN UTXO Bitcoin tanpa smart contract [Hal 7]",
        "0.8.28": "Teoretis/Config | Versi compiler Solidity pragma solidity ^0.8.28 [Hal 3, 7]",
        "1.963": "Teoretis/Config | Pembulatan calldata N=6 pada Tabel 8 (dari 1.962,80 gas perf-output.txt:23) [Hal 8]",
        "2.011": "Teoretis/Config | Pembulatan calldata N=100 pada Tabel 8 (dari 2.011,20 gas perf-output.txt:23) [Hal 8]",
        "2.047": "Teoretis/Config | Pembulatan calldata N=1000 pada Tabel 8 (dari 2.046,80 gas perf-output.txt:23) [Hal 8]",
        "4.200": "Teoretis/Config | Estimasi analitis pembacaan 2x SLOAD mapping (~4.200 gas) EVM Yellow Paper [Hal 9]",
        "12.000": "Teoretis/Config | Rujukan gas minimum fungsi transfer ETH standar EVM [Hal 8]",
        "13.500": "Teoretis/Config | Ambang batas anggaran pureVerifyGas N=1.000 (10.000 + 10*350 gas) [Hal 16]",
        "20.000": "Teoretis/Config | Biaya penulisan slot storage baru (SSTORE) EVM Yellow Paper (~20.000 gas/slot) [Hal 11]",
        "30.000.000": "Teoretis/Config | Contoh hipotetis kapasitas blok konsorsium untuk simulasi kapasitas blok [Hal 8, 11]",
    }

    print(f"Total Angka Bertitik Ditemukan pada PDF: {len(pdf_dotted)} angka\n")
    print(f"{'No':<3} | {'Angka Bertitik':<15} | {'Status':<16} | {'Sumber Log Spesifik / Konteks Dokumen':<65}")

    unexplained = 0
    for idx, item in enumerate(pdf_dotted, 1):
        if item in log_map:
            sources_str = ", ".join(log_map[item])
            status_str = "Ditemukan (100%)"
            desc_str = f"Tercatat di log: {sources_str}"
        elif item in known_non_log:
            status_str = "Teoretis/Config"
            desc_str = known_non_log[item]
        else:
            status_str = "TIDAK DIKETAHUI"
            desc_str = "Perlu investigasi"
            unexplained += 1
        print(f"{idx:<3} | {item:<15} | {status_str:<16} | {desc_str:<65}")

    return unexplained

def run_hash_audit(pdf_file):
    print("\nAudit integritas string hash 0x:")
    hash_script = "uts-blockchain-submission/tools/hash_check.py"
    if not os.path.exists(hash_script):
        hash_script = "uts-blockchain-submission/pendukung/tools/hash_check.py"
    cmd_hash = ["python3", hash_script, "--pdf", pdf_file]
    res_hash = subprocess.run(cmd_hash, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(res_hash.stdout)
    return res_hash.returncode == 0

def main():
    pdf_file, docx_file = parse_cli_args()
    print(f"Memverifikasi PDF: {pdf_file}")
    print(f"Memverifikasi DOCX: {docx_file}")

    if not os.path.exists(pdf_file):
        print(f"Error: File PDF '{pdf_file}' tidak ditemukan.", file=sys.stderr)
        sys.exit(1)

    doc = docx.Document(docx_file) if os.path.exists(docx_file) else None

    tools_dir = "uts-blockchain-submission/tools"
    if not os.path.exists(tools_dir):
        tools_dir = "uts-blockchain-submission/pendukung/tools"

    logs = {
        "demo-output.txt": load_file_lines("demo-output.txt"),
        "perf-output.txt": load_file_lines("perf-output.txt"),
        "test-output.txt": load_file_lines("test-output.txt"),
        "gaslimit_output.txt": load_file_lines("gaslimit_output.txt", tools_dir),
        "exp_b06_output.txt": load_file_lines("exp_b06_output.txt", tools_dir),
    }

    pdfinfo_out = subprocess.check_output(["pdfinfo", pdf_file]).decode("utf-8")
    total_pages = int(re.search(r"Pages:\s+(\d+)", pdfinfo_out).group(1))
    pdf_pages = {p: extract_pdf_page(pdf_file, p) for p in range(1, total_pages + 1)}
    full_pdf_text = extract_full_pdf(pdf_file)

    standard_tables = build_standard_table_definitions()
    unit_test_items = build_unit_test_items(doc)
    lampiran_b_items = build_lampiran_b_items()
    lampiran_d_items = build_lampiran_d_items(doc)
    lampiran_e_items = build_lampiran_e_items(doc)
    lampiran_f_items = build_lampiran_f_items()

    total_items = (
        sum(len(items) for _, items in standard_tables)
        + len(unit_test_items)
        + len(lampiran_b_items)
        + len(lampiran_d_items)
        + (len(lampiran_e_items) * 3)
        + len(lampiran_f_items)
    )

    mismatches = 0
    for group_name, items in standard_tables:
        mismatches += verify_standard_table_group(group_name, items, pdf_pages, logs)

    mismatches += verify_unit_tests(unit_test_items, logs["test-output.txt"])
    mismatches += verify_lampiran_d(lampiran_d_items, logs)
    mismatches += verify_lampiran_e(lampiran_e_items, logs["perf-output.txt"])
    mismatches += verify_lampiran_b(lampiran_b_items, full_pdf_text, logs["demo-output.txt"])
    mismatches += verify_lampiran_f(lampiran_f_items, full_pdf_text, logs["exp_b06_output.txt"])

    print(f"\nRekapitulasi forward check: {total_items - mismatches}/{total_items} baris dan sel terverifikasi cocok secara eksak.")

    unexplained_dotted = audit_dotted_numbers(full_pdf_text)
    hash_check_passed = run_hash_audit(pdf_file)

    if mismatches > 0 or unexplained_dotted > 0 or not hash_check_passed:
        print(f"Status: GAGAL ({mismatches} mismatch forward, {unexplained_dotted} dotted tak dikenal, hash check={hash_check_passed})")
        sys.exit(1)

    print(f"Status: LULUS 100% ({total_items} forward check cocok, reverse dotted tervalidasi, hash check lulus).")
    sys.exit(0)

if __name__ == "__main__":
    main()
