import subprocess
import re

# 1. Read PDF text
pdf_text = subprocess.check_output(['pdftotext', 'verified_v4.pdf', '-']).decode('utf-8', errors='ignore')

# 2. Read Logs
with open('prototype/results/demo-output.txt') as f:
    demo_raw = f.read()

with open('prototype/results/perf-output.txt') as f:
    perf_raw = f.read()

with open('prototype/results/test-output.txt') as f:
    test_raw = f.read()

# Define verification items
items = [
    # --- B-01 Deployment Kontrak ---
    ("Paragraf / Tabel 2", "B-01: Alamat Kontrak", "0x5FbDB2315678afecb367f032d93F642f64180aa3", "0x5FbDB2315678afecb367f032d93F642f64180aa3", demo_raw),
    ("Tabel 2 (Tahap 2)", "B-01: Tx Hash Deploy", "0x145b5523...", "0x145b5523b5eeb4fd842f56a495a3e9bf17267ea22d4c48a416d08a142f384498", demo_raw),
    ("Tabel 2 (Tahap 2)", "B-01: Gas Terpakai Deploy", "1.039.368 unit", "1039368 unit", demo_raw),
    
    # --- B-02 Pembangkitan Kredensial & Merkle Tree ---
    ("Tabel 2 (Tahap 3)", "B-02: Merkle Root Batch", "0x46ca2e8399d6be8a489c375dcd355319d7eaa4a92a132afdc3a00220c1faccd3", "0x46ca2e8399d6be8a489c375dcd355319d7eaa4a92a132afdc3a00220c1faccd3", demo_raw),
    ("Tabel 5 (Row 1)", "B-02: Leaf G-01", "0x7b5f7365dffd18a8...", "0x7b5f7365dffd18a87fb7b5471e7843da27e53b4ec53e8e1ef064b78ab3b0645c", demo_raw),
    ("Tabel 5 (Row 2)", "B-02: Leaf G-02", "0xf3695a1ce4a97902...", "0xf3695a1ce4a97902b58bf9bb868bac471c484bcedec9edfbb1a8290fa86a1575", demo_raw),
    ("Tabel 5 (Row 3)", "B-02: Leaf G-03", "0xca7c3acd32fa82a2...", "0xca7c3acd32fa82a21e64906ebae07cfca76df17336cb8709ca889b78e23fc486", demo_raw),
    ("Tabel 5 (Row 4)", "B-02: Leaf G-04", "0x5c97927280c16ef9...", "0x5c97927280c16ef933a39f6004b9015949d01f118ae032338b8160dafe2b947c", demo_raw),
    ("Tabel 5 (Row 5)", "B-02: Leaf G-05", "0xcc0d8357be021242...", "0xcc0d8357be021242337a76059c3621422797fb2e20ff36b77ca7067d264fec6c", demo_raw),
    ("Tabel 5 (Row 6)", "B-02: Leaf G-06", "0x108e53ac2b7a5439...", "0x108e53ac2b7a5439ce8a6e70eb35ba370bcf423c14a4c58cf35c9fc8f81ea3bc", demo_raw),
    
    # --- B-03 Penjangkaran Root On-Chain ---
    ("Tabel 2 & Tabel 8", "B-03: Tx Hash Issue", "0x1737c3595a7ffab660d99cb81bd14dc04b8c21f9fb399ad5b2aa454998a88321", "0x1737c3595a7ffab660d99cb81bd14dc04b8c21f9fb399ad5b2aa454998a88321", demo_raw),
    ("Tabel 8 (Row 3)", "B-03: Gas Terpakai Issue", "211.084 gas", "211084 unit", demo_raw),
    ("Tabel 8 (Row 4)", "B-03: Root di State Kontrak", "0x46ca2e83...", "0x46ca2e8399d6be8a489c375dcd355319d7eaa4a92a132afdc3a00220c1faccd3", demo_raw),
    
    # --- B-04 Verifikasi Dokumen Sah ---
    ("Tabel 2 & Tabel 12", "B-04: Biaya Gas Pemverifikasi", "0 gas (via eth_call)", "0 gas (Dipanggil via eth_call view query, bebas biaya)", demo_raw),
    
    # --- B-05 Anti-Tampering & RBAC ---
    ("Lampiran B & Tabel 12", "B-05A: Leaf Hasil Manipulasi", "0x0b097c59bcd2b3d0b5cba350b03cea87b34b4294eba79c5d5cf2f0a548d04f97", "0x0b097c59bcd2b3d0b5cba350b03cea87b34b4294eba79c5d5cf2f0a548d04f97", demo_raw),
    ("Lampiran B & Tabel 12", "B-05A: Pesan Status Ditolak", "INVALID_PROOF_OR_TAMPERED", "INVALID_PROOF_OR_TAMPERED", demo_raw),
    ("Lampiran B & Tabel 12", "B-05B: Pencegatan RBAC", "AccessControlUnauthorizedAccount", "AccessControlUnauthorizedAccount", demo_raw),
    
    # --- B-06 Pencabutan Kredensial ---
    ("Tabel 2 & Tabel 11", "B-06: Status Pasca-Cabut", "CREDENTIAL_REVOKED", "CREDENTIAL_REVOKED", demo_raw),
    
    # --- B-07 Jeda Darurat Pause ---
    ("Paragraf 66 & Tabel 2", "B-07: Gas Terpakai Pause", "48.214 unit", "Gas: 48214", demo_raw),
    
    # --- B-08 Benchmark Skalabilitas 30 Run ---
    ("Paragraf 6, 85, 91; Tabel 9, 13", "B-08: Gas Eksekusi Murni issueBatch", "164.911 gas", "164911.00", perf_raw),
    ("Paragraf 6, 56, 85, 91; Tabel 9", "B-08: Selisih Calldata N=1000 vs N=6", "84 gas", "+84 gas", perf_raw),
    ("Tabel 9 (Row 1)", "B-08: Total gasUsed N=6", "187.874 gas", "187873.80 (dibulatkan 187874)", perf_raw),
    ("Tabel 9 (Row 1)", "B-08: Total gasUsed N=100", "187.922 gas", "187922.20 (dibulatkan 187922)", perf_raw),
    ("Tabel 9 (Row 1)", "B-08: Total gasUsed N=1000", "187.958 gas", "187957.80 (dibulatkan 187958)", perf_raw),
    ("Tabel 9 (Row 3)", "B-08: Calldata tx.data N=6", "1.963 gas", "1962.80 (dibulatkan 1963)", perf_raw),
    ("Tabel 9 (Row 3)", "B-08: Calldata tx.data N=100", "2.011 gas", "2011.20 (dibulatkan 2011)", perf_raw),
    ("Tabel 9 (Row 3)", "B-08: Calldata tx.data N=1000", "2.047 gas", "2046.80 (dibulatkan 2047)", perf_raw),
    ("Tabel 13 (Row 1)", "B-08: Waktu Build N=6", "1.43 ms (SD: 0.43) [0.87 - 2.48]", "1.43 | 1.31 | 0.43 | [0.87 - 2.48]", perf_raw),
    ("Tabel 13 (Row 1)", "B-08: Waktu Build N=100", "14.01 ms (SD: 2.92) [11.29 - 26.39]", "14.01 | 13.01 | 2.92 | [11.29 - 26.39]", perf_raw),
    ("Tabel 13 (Row 1)", "B-08: Waktu Build N=1000", "129.44 ms (SD: 6.49) [121.10 - 146.35]", "129.44 | 128.35 | 6.49 | [121.10 - 146.35]", perf_raw),
    ("Tabel 13 (Row 5)", "B-08: Gas Revoke N=6", "55.303 gas (SD: 7) [55.285 - 55.309]", "55303 | 55309 | 7 | [55285 - 55309]", perf_raw),
    ("Tabel 13 (Row 5)", "B-08: Gas Revoke N=100", "55.328 gas (SD: 6) [55.321 - 55.333]", "55328 | 55333 | 6 | [55321 - 55333]", perf_raw),
    ("Tabel 13 (Row 5)", "B-08: Gas Revoke N=1000", "55.340 gas (SD: 7) [55.321 - 55.345]", "55340 | 55345 | 7 | [55321 - 55345]", perf_raw),
    ("Tabel 13 (Row 6)", "B-08: Raw estimateGas N=6", "32.242 gas (SD: 13) [32.211 - 32.267]", "32242 | 32245 | 13 | [32211 - 32267]", perf_raw),
    ("Tabel 13 (Row 6)", "B-08: Raw estimateGas N=100", "35.311 gas (SD: 20) [35.269 - 35.347]", "35311 | 35315 | 20 | [35269 - 35347]", perf_raw),
    ("Tabel 13 (Row 6)", "B-08: Raw estimateGas N=1000", "37.611 gas (SD: 25) [37.566 - 37.666]", "37611 | 37612 | 25 | [37566 - 37666]", perf_raw),
    ("Tabel 13 (Row 7)", "B-08: Calldata verify N=6", "2.687 gas (SD: 11) [2.664 - 2.700]", "2687 | 2688 | 11 | [2664 - 2700]", perf_raw),
    ("Tabel 13 (Row 7)", "B-08: Calldata verify N=100", "4.753 gas (SD: 14) [4.724 - 4.772]", "4753 | 4760 | 14 | [4724 - 4772]", perf_raw),
    ("Tabel 13 (Row 7)", "B-08: Calldata verify N=1000", "6.298 gas (SD: 16) [6.260 - 6.320]", "6298 | 6296 | 16 | [6260 - 6320]", perf_raw),
    ("Tabel 11 & 13 (Row 8)", "B-08: Pure Gas verify N=6", "8.554 gas", "8554", perf_raw),
    ("Tabel 13 (Row 8)", "B-08: Pure Gas verify N=100", "9.558 gas", "9558", perf_raw),
    ("Tabel 11 & 13 (Row 8)", "B-08: Pure Gas verify N=1000", "10.313 gas", "10313", perf_raw),
    ("Paragraf 58, 60; Tabel 13", "B-08: Model Regresi Linier", "pureVerifyGas = 7.800,04 + 251,26 * k", "pureVerifyGas(k) = 7800.04 + 251.26 * k", perf_raw),
    ("Tabel 13 (Row 10)", "B-08: Latensi View Call N=6", "0.89 ms (SD: 0.58) [0.48 - 3.24]", "0.89 | 0.71 | 0.58 | [0.48 - 3.24]", perf_raw),
    ("Tabel 13 (Row 10)", "B-08: Latensi View Call N=100", "0.87 ms (SD: 0.77) [0.38 - 3.72]", "0.87 | 0.62 | 0.77 | [0.38 - 3.72]", perf_raw),
    ("Tabel 13 (Row 10)", "B-08: Latensi View Call N=1000", "0.82 ms (SD: 0.26) [0.55 - 1.46]", "0.82 | 0.74 | 0.26 | [0.55 - 1.46]", perf_raw),
    
    # --- Unit Test Suite T-01 s.d. T-08 ---
    ("Tabel 12", "Test Runner: Status Kelulusan", "8 dari 8 test lulus (T-01 s.d. T-08)", "8 passing (673ms)", test_raw),
]

print("| Lokasi Dokumen | Parameter Bukti | Nilai di PDF | Nilai di Log | Status Cocok? |")
print("| :--- | :--- | :--- | :--- | :---: |")

# Clean helper for comparison
def simplify(t):
    return re.sub(r'[^a-zA-Z0-9]', '', t.lower())

for loc, param, pdf_val, log_val, log_source in items:
    # check if pdf_val is present in pdf_text
    # for truncated hashes, check prefix
    clean_pdf_val = simplify(pdf_val)
    found_in_pdf = False
    
    # check directly or partially
    if pdf_val.lower() in pdf_text.lower():
        found_in_pdf = True
    elif "..." in pdf_val:
        prefix = pdf_val.split("...")[0].strip()
        found_in_pdf = prefix.lower() in pdf_text.lower()
    else:
        # try checking with whitespace removed
        s_pdf = simplify(pdf_text)
        found_in_pdf = clean_pdf_val in s_pdf or clean_pdf_val[:12] in s_pdf

    # check if log_val is in log_source
    clean_log_val = simplify(log_val)
    found_in_log = clean_log_val in simplify(log_source)
    
    match = found_in_pdf and found_in_log
    status_str = "COCOK" if match else "PERIKSA"
    print(f"| {loc} | {param} | `{pdf_val}` | `{log_val}` | **{status_str}** |")

