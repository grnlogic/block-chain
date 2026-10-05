#!/usr/bin/env python3
"""
hash_check.py
Audit integritas seluruh string hash 0x... pada PDF laporan UTS Blockchain.
Aturan:
- Mengekstrak semua string 0x... dari PDF (menggabungkan baris yang terpotong word-wrap).
- Memeriksa string 64 digit hex bahwa string itu ADA persis di prototype/results/*.txt.
- Memeriksa string berelipsis bahwa prefiksnya ada di log.
- Memeriksa string short-hex EVM bahwa nilainya tercatat di log terukur (results/*.txt / gaslimit_output.txt).
- Mencetak tabel: String, Jenis, Berkas:Baris di Log, Status (ADA / TIDAK ADA).
- Keluar dengan exit code 1 bila ada string yang TIDAK ADA di log.
"""

import sys
import os
import re
import glob
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description="Audit Integritas Hash 0x... pada Laporan PDF")
    parser.add_argument("--pdf", default="v7_workspace/Laporan_UTS_Blockchain_237006079_v7.3.pdf", help="Jalur berkas PDF laporan")
    args = parser.parse_args()

    pdf_file = args.pdf
    if not os.path.exists(pdf_file):
        # Fallback to v7.2 if v7.3 not yet built
        if os.path.exists("v7_workspace/Laporan_UTS_Blockchain_237006079_v7.2.pdf") and "v7.3" in pdf_file:
            pdf_file = "v7_workspace/Laporan_UTS_Blockchain_237006079_v7.2.pdf"
        else:
            print(f"Error: Berkas PDF '{pdf_file}' tidak ditemukan.")
            sys.exit(1)

    print(f"=== HASH CHECKER AUDIT INTEGRITAS HASH 0x... ===")
    print(f"Memeriksa Dokumen: {pdf_file}")

    # Ekstraksi teks PDF
    cmd = ["pdftotext", pdf_file, "-"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    pdf_text = res.stdout

    # Gabungkan baris yang terpotong word-wrap: e.g. '0x1737...\n  321'
    pdf_text = re.sub(r'(0x[a-fA-F0-9]{10,63})\n\s*([a-fA-F0-9]{1,54})', r'\1\2', pdf_text)

    # Ekstraksi semua string 0x...
    raw_hashes = set(re.findall(r"0x[a-fA-F0-9\.]+", pdf_text))

    # Muat seluruh baris dari berkas log aktual
    log_files = sorted(glob.glob("prototype/results/*.txt"))
    # Tambahkan gaslimit_output.txt untuk blockGasLimit 0x3938700
    gaslimit_file = "uts-blockchain-submission/tools/gaslimit_output.txt"
    if os.path.exists(gaslimit_file):
        log_files.append(gaslimit_file)

    corpus_lines = []
    for p in log_files:
        with open(p, "r", encoding="utf-8") as f:
            for i, line in enumerate(f, 1):
                corpus_lines.append((p, i, line.rstrip("\r\n")))

    def find_in_log(target, is_prefix=False):
        t_clean = target.lower().rstrip(".,;:)")
        for path, line_no, line in corpus_lines:
            l_lower = line.lower()
            if t_clean in l_lower:
                return f"{os.path.basename(path)}:{line_no}", True
        return "-", False

    print(f"Total String 0x... Unik Ditemukan pada PDF: {len(raw_hashes)} string\n")
    print(f"{'No':<3} | {'String 0x... di PDF':<70} | {'Jenis':<16} | {'Target Log:Baris':<25} | {'Status':<10}")
    print("-" * 132)

    missing_count = 0
    results_table = []

    for idx, h in enumerate(sorted(raw_hashes), 1):
        has_dots = "..." in h or h.endswith("..") or h.endswith(".")
        clean_hex = re.sub(r"[^0-9a-fA-F]", "", h[2:])
        hex_len = len(clean_hex)

        if has_dots:
            kind = f"Prefix ({hex_len}h)"
            prefix_target = h[:h.index(".")]
            loc, found = find_in_log(prefix_target, is_prefix=True)
        elif hex_len == 64:
            kind = "Full 64-hex"
            loc, found = find_in_log(h)
        elif hex_len == 40:
            kind = "Address 40-hex"
            loc, found = find_in_log(h)
        else:
            kind = f"Short-hex ({hex_len}h)"
            loc, found = find_in_log(h)

        status = "ADA" if found else "TIDAK ADA"
        if not found:
            missing_count += 1

        results_table.append((idx, h, kind, loc, status))
        print(f"{idx:<3} | {h:<70} | {kind:<16} | {loc:<25} | {status:<10}")

    print("-" * 132)
    if missing_count > 0:
        print(f"HASIL AKHIR: GAGAL ({missing_count} hash tidak ditemukan di log aktual).")
        sys.exit(1)
    else:
        print(f"HASIL AKHIR: BERHASIL LULUS 100% (Semua {len(raw_hashes)} string 0x... terverifikasi ADA di log aktual).")
        sys.exit(0)

if __name__ == "__main__":
    main()
