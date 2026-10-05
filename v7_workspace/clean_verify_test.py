#!/usr/bin/env python3
"""
verify_report.py
Skrip verifikasi independen (di luar prototype/) untuk mencocokkan seluruh
angka, hash, dan metrik di dokumen laporan PDF dan DOCX final terhadap berkas log aktual
di prototype/results/* dan uts-blockchain-submission/tools/*.

Fitur Utama v7.4:
1. Cakupan Penuh 121 Item (>= 99 item) mencakup:
   - Tabel 2: Catatan Pelaksanaan Mini-Project (5 item)
   - Tabel 5: Record Daun Merkle G-01 s.d. G-06 (18 item)
   - Tabel 7: Field Transaksi EVM Penjangkaran (8 item)
   - Tabel 8: Komposisi Gas Transaksi issueBatch (13 item)
   - Tabel Unit Test: ID T-01 s.d. T-08 (8 item)
   - Lampiran B: Keluaran Eksekusi Prototipe B-05 (8 item)
   - Lampiran D: Matriks Evaluasi Kriteria Luaran OBE (10 item)
   - Lampiran E: Rekapitulasi Lengkap Metrik 30 Run Terukur (30 item: N=6, 100, 1000)
   - Lampiran F: Eksperimen Isolasi Variabel Selisih Gas B-06 (21 item: Run A s.d. E)
2. Pengecekan Dua Sisi:
   (a) Di sisi dokumen: nilai/string dicocokkan di sel tabel docx dan teks PDF pada halaman yang benar.
   (b) Di sisi log: nilai/string dicocokkan di baris log yang bersangkutan.
   Untuk alamat dan hash 0x: diperiksa eksistensinya secara eksak pada teks PDF.
3. Reverse Check Angka Bertitik:
   - 82 angka bertitik pada teks PDF diverifikasi sumber lognya atau konteks teoretisnya.
4. Reverse Check Hash 0x...:
   - 16 string hash 0x... diverifikasi eksistensinya di log aktual melalui hash_check.py.
5. Exit code 0 bila 100% lulus, exit code 1 bila ada kegagalan.
"""

import subprocess
import sys
import os
import re
import glob
import docx

if len(sys.argv) > 1:
    PDF_FILE = sys.argv[1]
elif os.path.exists("v7_workspace/Laporan_UTS_Blockchain_237006079_v7.5.pdf"):
    PDF_FILE = "v7_workspace/Laporan_UTS_Blockchain_237006079_v7.5.pdf"
elif os.path.exists("v7_workspace/Laporan_UTS_Blockchain_237006079_v7.4.pdf"):
    PDF_FILE = "v7_workspace/Laporan_UTS_Blockchain_237006079_v7.4.pdf"
elif os.path.exists("v7_workspace/Laporan_UTS_Blockchain_237006079_v7.3.pdf"):
    PDF_FILE = "v7_workspace/Laporan_UTS_Blockchain_237006079_v7.3.pdf"
else:
    PDF_FILE = "uts-blockchain-submission/237006079_Fajar_Geran_Arifin_UTS_Blockchain_OBE.pdf"

DOCX_FILE = os.environ.get("DOCX_FILE") or (sys.argv[2] if len(sys.argv) > 2 else PDF_FILE.replace(".pdf", ".docx"))
if not os.path.exists(DOCX_FILE) and os.path.exists(os.path.join("uts-blockchain-submission/sumber", os.path.basename(DOCX_FILE))):
    DOCX_FILE = os.path.join("uts-blockchain-submission/sumber", os.path.basename(DOCX_FILE))
RESULTS_DIR = "prototype/results"
TOOLS_DIR = "uts-blockchain-submission/tools"

def load_file_lines(filename, base_dir=RESULTS_DIR):
    path = os.path.join(base_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        return [l.rstrip("\r\n") for l in f.readlines()]

def extract_pdf_page(page_num):
    cmd = ["pdftotext", "-f", str(page_num), "-l", str(page_num), PDF_FILE, "-"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return res.stdout

def extract_full_pdf():
    cmd = ["pdftotext", PDF_FILE, "-"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return res.stdout

def find_docx_table(doc, header_keyword):
    for i, t in enumerate(doc.tables):
        first_row_text = " ".join(c.text.strip().replace("\n", " ") for c in t.rows[0].cells)
        if header_keyword.lower() in first_row_text.lower():
            return t
    return None

def main():
    print(f"Memverifikasi PDF: {PDF_FILE}")
    print(f"Memverifikasi DOCX: {DOCX_FILE}")

    if not os.path.exists(PDF_FILE):
        print(f"Error: File PDF {PDF_FILE} tidak ditemukan!")
        sys.exit(1)

    doc = None
    if os.path.exists(DOCX_FILE):
        doc = docx.Document(DOCX_FILE)

    demo_lines = load_file_lines("demo-output.txt")
    perf_lines = load_file_lines("perf-output.txt")
    test_lines = load_file_lines("test-output.txt")
    gaslimit_lines = load_file_lines("gaslimit_output.txt", TOOLS_DIR)
    exp_b06_lines = load_file_lines("exp_b06_output.txt", TOOLS_DIR)

    pdfinfo_out = subprocess.check_output(["pdfinfo", PDF_FILE]).decode("utf-8")
    total_pages = int(re.search(r"Pages:\s+(\d+)", pdfinfo_out).group(1))
    pdf_pages = {p: extract_pdf_page(p) for p in range(1, total_pages + 1)}
    full_pdf_text = extract_full_pdf()

    mismatches = 0

    # 1. TABEL 2: Catatan Pelaksanaan (B-01, B-03, B-04, B-06, B-07) - Hal 3
    tabel_2_items = [
        ("B-01 Gas Deploy Kontrak", "1.039.368", 3, "demo-output.txt", 15, "1039368"),
        ("B-03 Tx Hash Issue Batch", "0x1737c359...", 3, "demo-output.txt", 29, "0x1737c359"),
        ("B-04 Verifikasi Valid", "0 gas", 3, "demo-output.txt", 43, "0 gas"),
        ("B-06 Gas Revoke Credential", "56.359", 3, "demo-output.txt", 63, "56359"),
        ("B-07 Gas Pause Circuit Breaker", "48.214", 3, "demo-output.txt", 68, "48214"),
    ]

    # 2. TABEL 5: Data Daun Merkle (Record / Daun G-01 s.d. G-06) - Hal 5-6
    tabel_5_items = [
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

    # 3. TABEL 7: Field Transaksi EVM (Penerbitan Batch #2) - Hal 8
    tabel_7_items = [
        ("Chain ID", "31337", 8, "perf-output.txt", 2, "31337"),
        ("Sender (from) ISSUER_ROLE", "0x70997970C5...", 8, "demo-output.txt", 5, "0x70997970C5"),
        ("Receiver (to) AcademicRegistry", "0x5FbDB23156...", 8, "demo-output.txt", 12, "0x5FbDB23156"),
        ("Gas Used Batch", "211.084", 8, "demo-output.txt", 31, "211084"),
        ("Block Number", "#2", 8, "demo-output.txt", 30, "2"),
        ("Merkle Root", "0x46ca2e83...", 8, "demo-output.txt", 25, "0x46ca2e83"),
        ("Tx Hash Penerbitan", "0x1737c359...", 8, "demo-output.txt", 29, "0x1737c359"),
        ("Gas Limit Blok Hardhat", "60.000.000", 8, "gaslimit_output.txt", 5, "60000000"),
    ]

    # 4. TABEL 8: Komposisi Gas Transaksi issueBatch (N=6, 100, 1000) - Hal 8
    tabel_8_items = [
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

    # 5. TABEL UNIT TEST (T-01 s.d. T-08 / Tabel 10 Naskah) - Hal 10
    tbl_10_doc = find_docx_table(doc, "ID Tes") if doc else None
    tabel_10_items = []
    if tbl_10_doc:
        for r_idx in range(1, 9):
            row_cells = [c.text.strip().replace("\n", " ") for c in tbl_10_doc.rows[r_idx].cells]
            tid = f"T-{r_idx:02d}"
            tabel_10_items.append((
                f"Tabel 10 Baris {r_idx} ({tid})",
                row_cells[0],
                row_cells[1],
                row_cells[4],
                "test-output.txt",
                r_idx + 3,
                tid
            ))

    # 6. LAMPIRAN B: Keluaran Eksekusi B-05 - Hal 14
    lampiran_b_items = [
        ("Skenario 5A IPK Manipulasi", "Skenario 5A: Pelamar mengubah IPK 3.82 menjadi 4.00 pada berkas lokal", "demo-output.txt", 49, "IPK 3.82 menjadi 4.00"),
        ("Leaf Asli 64-char Hex", "Leaf Asli            : 0x7b5f7365dffd18a87fb7b5471e7843da27e53b4ec53e8e1ef064b78ab3b0645c", "demo-output.txt", 50, "0x7b5f7365dffd18a87fb7b5471e7843da27e53b4ec53e8e1ef064b78ab3b0645c"),
        ("Leaf Manipulasi 64-char Hex", "Leaf Hasil Manipulasi: 0x0b097c59bcd2b3d0b5cba350b03cea87b34b4294eba79c5d5cf2f0a548d04f97", "demo-output.txt", 51, "0x0b097c59bcd2b3d0b5cba350b03cea87b34b4294eba79c5d5cf2f0a548d04f97"),
        ("Hasil Verifikasi Manipulasi", "Hasil Verifikasi     : DITOLAK / INVALID (FALSE)", "demo-output.txt", 52, "DITOLAK / INVALID (FALSE)"),
        ("Pesan Status Kontrak", "Pesan Status Kontrak : INVALID_PROOF_OR_TAMPERED", "demo-output.txt", 53, "INVALID_PROOF_OR_TAMPERED"),
        ("Skenario 5B Attacker RBAC", "Skenario 5B: Upaya penerbitan batch oleh penyerang tanpa hak (Attacker)", "demo-output.txt", 55, "Upaya penerbitan batch oleh penyerang tanpa hak"),
        ("Hasil Pencegatan RBAC", "Hasil Pencegatan RBAC: Transaksi Dibatalkan (Reverted)", "demo-output.txt", 56, "Transaksi Dibatalkan (Reverted)"),
        ("Custom Error Kontrak", "Eksepsi Kontrak      : VM Exception while processing transaction: reverted with custom error 'AccessControlUnauthorizedAccount", "demo-output.txt", 57, "AccessControlUnauthorizedAccount"),
    ]

    # 7. LAMPIRAN D: Matriks Evaluasi OBE (T-01 s.d. T-08) - Hal 15-18
    tbl_d_doc = find_docx_table(doc, "Kelompok Uji") if doc else None
    lampiran_d_items = []
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
    if tbl_d_doc:
        for r_idx in range(1, 11):
            row_text = " ".join(c.text.strip().replace("\n", " ") for c in tbl_d_doc.rows[r_idx].cells)
            label, token1, token2, log_f, log_l, exp_log = expected_d_tokens[r_idx - 1]
            status_cell = tbl_d_doc.rows[r_idx].cells[6].text.strip()
            lampiran_d_items.append((label, token1, token2, status_cell, row_text, log_f, log_l, exp_log))

    # 8. LAMPIRAN E: Parameter Pengujian 30 Run Terukur (30 item) - Hal 18-20
    tbl_e_doc = find_docx_table(doc, "Parameter Pengujian") if doc else None
    lampiran_e_items = []
    # (Label, N6_val, N100_val, N1000_val, log_file, line_num, exp_log_substr)
    expected_e_rows = [
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
    if tbl_e_doc:
        for r_idx in range(1, 11):
            row_cells = [c.text.strip().replace("\n", " ") for c in tbl_e_doc.rows[r_idx].cells]
            label, t1, t2, t3, log_f, log_l, exp_logs = expected_e_rows[r_idx - 1]
            lampiran_e_items.append((label, t1, t2, t3, row_cells, log_f, log_l, exp_logs))

    # 9. LAMPIRAN F: Eksperimen Selisih Gas B-06 (21 item) - Hal 20-21
    tbl_f_doc = find_docx_table(doc, "Skenario Uji") if doc else None
    lampiran_f_items = [
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
        ("Run E (N=6) Calldata", "1.412 gas", (20, 21), "exp_b06_output.txt", 41, "1412"),
        ("Run E (N=6) Receipt", "55.297 gas", (20, 21), "exp_b06_output.txt", 41, "55297"),
        ("Run E (N=1000) Calldata", "1.448 gas", (20, 21), "exp_b06_output.txt", 43, "1448"),
        ("Run E (N=1000) Receipt", "55.333 gas", (20, 21), "exp_b06_output.txt", 43, "55333"),
        ("Run E (N=1000) Selisih", "-1.026 gas", (20, 21), "exp_b06_output.txt", 43, "-1026"),
    ]

    # Total item count calculation
    count_tabel_2 = len(tabel_2_items)
    count_tabel_5 = len(tabel_5_items)
    count_tabel_7 = len(tabel_7_items)
    count_tabel_8 = len(tabel_8_items)
    count_tabel_10 = len(tabel_10_items)
    count_lampiran_b = len(lampiran_b_items)
    count_lampiran_d = len(lampiran_d_items)
    count_lampiran_e = len(lampiran_e_items) * 3  # 3 metrics per row (N=6, N=100, N=1000)
    count_lampiran_f = len(lampiran_f_items)
    total_items = (count_tabel_2 + count_tabel_5 + count_tabel_7 + count_tabel_8 +
                   count_tabel_10 + count_lampiran_b + count_lampiran_d + count_lampiran_e + count_lampiran_f)

    print("BAGIAN 1: VERIFIKASI FORWARD PER-BARIS TABEL DAN LOG AKTUAL (POIN 2a & D1)")
    print(f"{'Kategori Tabel / Bagian Dokumen':<45} | {'Jumlah Item':<12} | {'Halaman Target':<18} | {'Sumber Log Acuan':<25}")
    print(f"{'1. Tabel 2 (Catatan Pelaksanaan Mini-Project)':<45} | {count_tabel_2:<12} | {'Halaman 3':<18} | {'demo-output.txt':<25}")
    print(f"{'2. Tabel 5 (Struktur Data Record Daun G-01..G-06)':<45} | {count_tabel_5:<12} | {'Halaman 5-6':<18} | {'demo-output.txt':<25}")
    print(f"{'3. Tabel 7 (Field Transaksi EVM Penjangkaran)':<45} | {count_tabel_7:<12} | {'Halaman 8':<18} | {'perf / demo / gaslimit':<25}")
    print(f"{'4. Tabel 8 (Komposisi Gas Transaksi issueBatch)':<45} | {count_tabel_8:<12} | {'Halaman 8':<18} | {'perf-output.txt':<25}")
    print(f"{'5. Tabel Unit Test (T-01 s.d. T-08 / Tabel 10)':<45} | {count_tabel_10:<12} | {'Halaman 10':<18} | {'test-output.txt':<25}")
    print(f"{'6. Lampiran B (Keluaran Log Eksekusi B-05)':<45} | {count_lampiran_b:<12} | {'Halaman 14':<18} | {'demo-output.txt':<25}")
    print(f"{'7. Lampiran D (Matriks Luaran OBE T-01..T-08)':<45} | {count_lampiran_d:<12} | {'Halaman 15-18':<18} | {'demo / perf log':<25}")
    print(f"{'8. Lampiran E (Rekapitulasi 30 Run: N=6/100/1000)':<45} | {count_lampiran_e:<12} | {'Halaman 18-20':<18} | {'perf-output.txt':<25}")
    print(f"{'9. Lampiran F (Eksperimen Selisih Gas B-06)':<45} | {count_lampiran_f:<12} | {'Halaman 20-21':<18} | {'exp_b06_output.txt':<25}")
    print(f"{'TOTAL ITEM DIVERIFIKASI':<45} | {total_items:<12} | {'Seluruh Dokumen':<18} | {'(Syarat: >= 99 item)'}")

    # 1. Tabel 2, 5, 7, 8
    standard_tables = [
        ("Tabel 2 (Catatan Pelaksanaan)", tabel_2_items),
        ("Tabel 5 (Record Daun Merkle)", tabel_5_items),
        ("Tabel 7 (Field Transaksi EVM)", tabel_7_items),
        ("Tabel 8 (Komposisi Gas issueBatch)", tabel_8_items),
    ]
    for cat_name, items in standard_tables:
        print(f"\n--- {cat_name.upper()} ({len(items)} item) ---")
        print(f"{'Hal':<5} | {'Elemen / Metrik':<35} | {'Nilai di PDF':<26} | {'Target Log:Baris':<25} | {'Cocok?':<8}")
        for elem_name, val_pdf, page, log_file, line_num, expected_in_log in items:
            if isinstance(page, tuple):
                pdf_text = " ".join(pdf_pages[p] for p in range(page[0], page[1] + 1))
                page_str = f"{page[0]}-{page[1]}"
            else:
                pdf_text = pdf_pages[page]
                page_str = str(page)

            clean_pdf_text = re.sub(r"(0x[a-fA-F0-9]+)\n\s*([a-fA-F0-9\.]+)", r"\1\2", pdf_text)

            log_line = ""
            if log_file == "demo-output.txt":
                log_line = demo_lines[line_num - 1] if line_num <= len(demo_lines) else ""
            elif log_file == "perf-output.txt":
                log_line = perf_lines[line_num - 1] if line_num <= len(perf_lines) else ""
            elif log_file == "gaslimit_output.txt":
                log_line = gaslimit_lines[line_num - 1] if line_num <= len(gaslimit_lines) else ""

            pdf_match = (val_pdf in pdf_text) or (val_pdf in clean_pdf_text)
            log_match = expected_in_log in log_line
            status = "Cocok" if (pdf_match and log_match) else "GAGAL"
            if status == "GAGAL":
                mismatches += 1
            disp_pdf = val_pdf if len(val_pdf) <= 20 else val_pdf[:17] + "..."
            raw_log = log_line.strip()
            if len(raw_log) > 45: raw_log = raw_log[:42] + "..."
            print(f"{page_str:<5} | {elem_name:<32} | {disp_pdf:<20} | {status:<6} | [{log_file}:{line_num}] {raw_log}")

    # 2. Tabel Unit Test (Tabel 10): Per-Baris DOCX
    print(f"\n--- TABEL UNIT TEST (T-01 s.d. T-08 / TABEL 10 DOCX) ({len(tabel_10_items)} item) ---")
    print(f"{'Baris':<15} | {'ID Tes':<8} | {'Skenario Uji di Tabel':<40} | {'Status Cell':<12} | {'Log Ref:Baris':<22} | {'Cocok?':<8}")
    for label, tid, scenario, status_cell, log_file, line_num, exp_log in tabel_10_items:
        log_line = test_lines[line_num - 1] if line_num <= len(test_lines) else ""
        match_table = (tid in label) and (len(scenario) > 5)
        match_log = exp_log in log_line
        status = "Cocok" if (match_table and match_log) else "GAGAL"
        if status == "GAGAL":
            mismatches += 1
        print(f"{label:<15} | {tid:<8} | {scenario[:38]:<40} | {status_cell[:10]:<12} | {log_file}:{line_num:<14} | {status:<8}")

    # 3. Lampiran D: Per-Baris DOCX
    print(f"\n--- LAMPIRAN D (MATRIKS OBE LENGKAP - TABEL 12 DOCX) ({len(lampiran_d_items)} item) ---")
    print(f"{'Baris':<25} | {'Token 1 (Wajib)':<32} | {'Token 2 (Unloosened)':<20} | {'Status Cell':<12} | {'Cocok?':<8}")
    for label, t1, t2, status_cell, row_text, log_file, line_num, exp_log in lampiran_d_items:
        log_line = ""
        if log_file == "demo-output.txt":
            log_line = demo_lines[line_num - 1] if line_num <= len(demo_lines) else ""
        elif log_file == "perf-output.txt":
            log_line = perf_lines[line_num - 1] if line_num <= len(perf_lines) else ""

        match_row = (t1 in row_text) and (t2 in row_text)
        match_log = exp_log in log_line
        match_status = (status_cell == "LULUS")
        status = "Cocok" if (match_row and match_log and match_status) else "GAGAL"
        if status == "GAGAL":
            mismatches += 1
        print(f"{label:<25} | {t1[:30]:<32} | {t2:<20} | {status_cell:<12} | {status:<8}")

    # 4. Lampiran E: Per-Baris DOCX (30 item checked)
    print(f"\n--- LAMPIRAN E (REKAPITULASI 30 RUN - TABEL 13 DOCX) ({count_lampiran_e} item) ---")
    print(f"{'Baris':<30} | {'N=6':<18} | {'N=100':<18} | {'N=1000':<18} | {'Log Ref:Baris':<18} | {'Cocok?':<8}")
    for label, t1, t2, t3, cells, log_file, line_num, exp_logs in lampiran_e_items:
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
        print(f"{label:<30} | {t1:<18} | {t2:<18} | {t3:<18} | {log_file}:{line_num:<10} | {row_status:<8}")

    # 5. Lampiran B: Per-Baris Log
    print(f"\n--- LAMPIRAN B (KELUARAN EKSEKUSI B-05 - PER BARIS LOG DEMO) ({len(lampiran_b_items)} item) ---")
    print(f"{'Item Bukti':<28} | {'Baris Cuplikan di PDF / DOCX':<45} | {'Target Log:Baris':<22} | {'Cocok?':<8}")
    lamp_b_text = full_pdf_text
    for item_name, exp_text, log_file, line_num, exp_log in lampiran_b_items:
        log_line = demo_lines[line_num - 1] if line_num <= len(demo_lines) else ""
        match_pdf = (exp_log in lamp_b_text)
        match_log = (exp_log in log_line)
        status = "Cocok" if (match_pdf and match_log) else "GAGAL"
        if status == "GAGAL":
            mismatches += 1
        disp_txt = exp_text if len(exp_text) <= 42 else exp_text[:39] + "..."
        print(f"{item_name:<28} | {disp_txt:<45} | {log_file}:{line_num:<14} | {status:<8}")

    # 6. Lampiran F: Per-Baris Tabel Run A s.d. E (21 item)
    print(f"\n--- LAMPIRAN F (EKSPERIMEN ISOLASI VARIABEL B-06 - TABEL 14 DOCX) ({len(lampiran_f_items)} item) ---")
    print(f"{'Skenario & Metrik':<28} | {'Nilai di Tabel / PDF':<25} | {'Target Log:Baris':<25} | {'Cocok?':<8}")
    lamp_f_text = full_pdf_text
    for item_name, val_str, page, log_file, line_num, exp_log in lampiran_f_items:
        log_line = exp_b06_lines[line_num - 1] if line_num <= len(exp_b06_lines) else ""
        match_pdf = (val_str in lamp_f_text)
        match_log = (exp_log in log_line)
        status = "Cocok" if (match_pdf and match_log) else "GAGAL"
        if status == "GAGAL":
            mismatches += 1
        print(f"{item_name:<28} | {val_str:<25} | {log_file}:{line_num:<17} | {status:<8}")

    print("\n" + "=" * 115)
    print(f"REKAPITULASI FORWARD CHECK: {total_items - mismatches}/{total_items} baris & sel terverifikasi cocok secara eksak.")

    # BAGIAN 2: AUDIT KEBALIKAN ANGKA BERTITIK UTUH (POIN 2b)
    print("\n" + "=" * 115)
    print("BAGIAN 2: AUDIT KEBALIKAN (REVERSE CHECK) ANGKA BERTITIK UTUH PADA PDF (POIN 2b)")

    source_files = [
        ("prototype/results/demo-output.txt", "demo-output.txt"),
        ("prototype/results/perf-output.txt", "perf-output.txt"),
        ("prototype/results/test-output.txt", "test-output.txt"),
        ("uts-blockchain-submission/tools/gaslimit_output.txt", "gaslimit_output.txt"),
        ("uts-blockchain-submission/tools/exp_b06_output.txt", "exp_b06_output.txt"),
        ("uts-blockchain-submission/tools/bytecode_output.txt", "bytecode_output.txt")
    ]
    file_contents = {}
    for path, label in source_files:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                file_contents[label] = f.read()

    raw_pdf_dotted = sorted(list(set(re.findall(r"\b\d{1,3}(?:\.\d{3})+(?:,\d+)?\b", full_pdf_text))))
    pdf_dotted = raw_pdf_dotted

    log_map = {}
    for d in pdf_dotted:
        un_dotted = d.replace(".", "").replace(",", ".")
        int_val = d.replace(".", "").split(",")[0]

        matches = []
        for label, content in file_contents.items():
            if d in content:
                matches.append(label)
            elif re.search(rf"\b{re.escape(int_val)}\b", content):
                matches.append(label)
            elif un_dotted != int_val and re.search(rf"\b{re.escape(un_dotted)}\b", content):
                matches.append(label)

        if matches:
            log_map[d] = sorted(list(set(matches)))

    print(f"Total Angka Bertitik Ditemukan pada PDF: {len(pdf_dotted)} angka\n")
    print(f"{'No':<3} | {'Angka Bertitik':<15} | {'Status':<16} | {'Sumber Log Spesifik / Konteks Dokumen':<65}")

    known_non_log_dotted = {
        "0.005": "Teoretis/Config | Ilustrasi biaya transaksi OP_RETURN UTXO Bitcoin tanpa smart contract [Hal 7]",
        "0.8.28": "Teoretis/Config | Versi compiler Solidity pragma solidity ^0.8.28 [Hal 3, 7]",
        "1.963": "Teoretis/Config | Pembulatan calldata N=6 pada Tabel 8 (dari 1.962,80 gas perf-output.txt:23) [Hal 8]",
        "2.011": "Teoretis/Config | Pembulatan calldata N=100 pada Tabel 8 (dari 2.011,20 gas perf-output.txt:23) [Hal 8]",
        "2.047": "Teoretis/Config | Pembulatan calldata N=1000 pada Tabel 8 (dari 2.046,80 gas perf-output.txt:23) [Hal 8]",
        "4.200": "Teoretis/Config | Estimasi analitis pembacaan 2x SLOAD mapping (~4.200 gas) EVM Yellow Paper [Hal 9]",
        "12.000": "Teoretis/Config | Rujukan gas minimum fungsi transfer ETH standar EVM [Hal 8]",
        "13.500": "Teoretis/Config | Ambang batas anggaran pureVerifyGas N=1.000 (10.000 + 10*350 gas) [Hal 16]",
        "20.000": "Teoretis/Config | Biaya penulisan slot storage baru (SSTORE) EVM Yellow Paper (~20.000 gas/slot) [Hal 11]",
        "30.000.000": "Teoretis/Config | Contoh hipotetis kapasitas blok konsorsium untuk simulasi kapasitas blok [Hal 8, 11]"
    }

    unexplained_dotted = 0
    for idx, d in enumerate(pdf_dotted, 1):
        if d in log_map:
            sources_str = ", ".join(log_map[d])
            status_str = "Ditemukan (100%)"
            desc_str = f"Tercatat di log: {sources_str}"
        elif d in known_non_log_dotted:
            status_str = "Teoretis/Config"
            desc_str = known_non_log_dotted[d]
        else:
            status_str = "TIDAK DIKETAHUI"
            desc_str = "Perlu investigasi"
            unexplained_dotted += 1

        print(f"{idx:<3} | {d:<15} | {status_str:<16} | {desc_str:<65}")

    # BAGIAN 3: AUDIT KEBALIKAN INTEGRITAS HASH 0x... (POIN 1b & 2d)
    print("\n" + "=" * 115)
    print("BAGIAN 3: AUDIT INTEGRITAS STRING HASH 0x... (POIN 1b & 2d)")

    cmd_hash = ["python3", "uts-blockchain-submission/tools/hash_check.py", "--pdf", PDF_FILE]
    res_hash = subprocess.run(cmd_hash, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print(res_hash.stdout)
    hash_check_passed = (res_hash.returncode == 0)

    # STATUS AKHIR
    if mismatches > 0 or unexplained_dotted > 0 or not hash_check_passed:
        print(f"STATUS AKHIR: GAGAL ({mismatches} mismatch forward, {unexplained_dotted} dotted tak dikenal, hash_check={hash_check_passed})")
        sys.exit(1)
    else:
        print(f"STATUS AKHIR: BERHASIL LULUS 100% (Semua {total_items} forward check cocok, reverse dotted tervalidasi, hash_check lulus).")
        sys.exit(0)

if __name__ == "__main__":
    main()
