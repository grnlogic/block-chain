import docx
import re

doc = docx.Document('uts-blockchain-submission/Laporan_UTS_Blockchain_237006079.docx')

with open('prototype/results/demo-output.txt') as f:
    demo = f.read()

with open('prototype/results/perf-output.txt') as f:
    perf = f.read()

with open('prototype/results/test-output.txt') as f:
    test = f.read()

all_logs = demo + "\n" + perf + "\n" + test

# Helper to normalize numbers and hashes
def clean_num(s):
    return s.replace('.', '').replace(',', '.')

print("=== CHECKING PARAGRAPHS ===")
# Check key paragraphs
for p_idx in [6, 21, 55, 60, 66, 85, 91]:
    p = doc.paragraphs[p_idx]
    # find hashes
    hashes = re.findall(r'0x[a-fA-F0-9]{8,}', p.text)
    for h in hashes:
        match = h.lower() in all_logs.lower()
        print(f"P{p_idx} Hash {h[:12]}... in logs: {match}")
    # find gas numbers like 164.911, 48.214, 84
    nums = re.findall(r'\b(?:164\.911|48\.214|21\.000|84|251[,.]3|252[,.]6)\b', p.text)
    for n in nums:
        norm = n.replace('.', '')
        match = norm in all_logs or n in all_logs
        print(f"P{p_idx} Num {n} in logs: {match}")

print("\n=== CHECKING TABLES ===")
# Tables: 2, 5, 8, 9, 11, 12, 13
tables_to_check = [2, 5, 8, 9, 11, 12, 13]
for t_idx in tables_to_check:
    tbl = doc.tables[t_idx]
    print(f"\n--- TABLE {t_idx} ---")
    for r_idx, row in enumerate(tbl.rows):
        for c_idx, cell in enumerate(row.cells):
            txt = cell.text.strip()
            # find hashes
            hashes = re.findall(r'0x[a-fA-F0-9]{8,}', txt)
            for h in set(hashes):
                match = h.lower() in all_logs.lower()
                print(f"T{t_idx}[R{r_idx},C{c_idx}] Hash {h[:14]}... in logs: {match}")
            # find metrics like 1.039.368, 211.084, 187.874, 55.303, 32.242, 8.554, etc.
            metric_candidates = re.findall(r'\b\d{1,3}(?:\.\d{3})+(?:,\d+)?\b|\b\d{5,6}\b', txt)
            for m in set(metric_candidates):
                raw_m = m.replace('.', '')
                match = (raw_m in all_logs) or (m in all_logs)
                print(f"T{t_idx}[R{r_idx},C{c_idx}] Metric {m} (raw: {raw_m}) in logs: {match}")

