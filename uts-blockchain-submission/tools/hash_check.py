#!/usr/bin/env python3
"""Audit integritas seluruh string hash 0x... pada PDF laporan terhadap log aktual."""

import argparse
import glob
import os
import re
import subprocess
import sys

def parse_arguments():
    parser = argparse.ArgumentParser(description="Audit integritas string hash 0x... pada PDF laporan.")
    default_pdf = "uts-blockchain-submission/237006079_Fajar_Geran_Arifin_UTS_Blockchain_OBE.pdf"
    if not os.path.exists(default_pdf):
        default_pdf = "v7_workspace/Laporan_UTS_Blockchain_237006079_v7.5.pdf"
    parser.add_argument("--pdf", default=default_pdf, help="Jalur berkas PDF laporan")
    return parser.parse_args()

def extract_pdf_hashes(pdf_path):
    cmd = ["pdftotext", pdf_path, "-"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    pdf_text = res.stdout

    # Menyambung string hex terputus akibat word-wrap pdftotext.
    pdf_text = re.sub(r'(0x[a-fA-F0-9]{10,63})\n\s*([a-fA-F0-9]{1,54})', r'\1\2', pdf_text)
    return set(re.findall(r"0x[a-fA-F0-9\.]+", pdf_text))

def load_corpus_lines():
    log_files = sorted(glob.glob("prototype/results/*.txt"))
    gaslimit_file = "uts-blockchain-submission/tools/gaslimit_output.txt"
    if os.path.exists(gaslimit_file):
        log_files.append(gaslimit_file)

    corpus = []
    for log_path in log_files:
        with open(log_path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, 1):
                corpus.append((log_path, line_no, line.rstrip("\r\n")))
    return corpus

def find_target_in_corpus(target, corpus):
    target_clean = target.lower().rstrip(".,;:)")
    for log_path, line_no, line in corpus:
        if target_clean in line.lower():
            return f"{os.path.basename(log_path)}:{line_no}", True
    return "-", False

def classify_hash_string(hash_str):
    has_ellipsis = "..." in hash_str or hash_str.endswith("..") or hash_str.endswith(".")
    clean_hex = re.sub(r"[^0-9a-fA-F]", "", hash_str[2:])
    hex_len = len(clean_hex)

    if has_ellipsis:
        return f"Prefix ({hex_len}h)", hash_str[:hash_str.index(".")]
    if hex_len == 64:
        return "Full 64-hex", hash_str
    if hex_len == 40:
        return "Address 40-hex", hash_str
    return f"Short-hex ({hex_len}h)", hash_str

def main():
    args = parse_arguments()
    if not os.path.exists(args.pdf):
        print(f"Error: berkas PDF '{args.pdf}' tidak ditemukan.", file=sys.stderr)
        sys.exit(1)

    print(f"Audit integritas hash: {args.pdf}")
    raw_hashes = extract_pdf_hashes(args.pdf)
    corpus = load_corpus_lines()

    print(f"Total string 0x unik: {len(raw_hashes)}\n")
    print(f"{'No':<3} | {'String 0x di PDF':<70} | {'Jenis':<16} | {'Target Log:Baris':<25} | {'Status':<10}")

    missing_count = 0
    for idx, hash_item in enumerate(sorted(raw_hashes), 1):
        kind, search_target = classify_hash_string(hash_item)
        loc, found = find_target_in_corpus(search_target, corpus)
        status = "ADA" if found else "TIDAK ADA"
        if not found:
            missing_count += 1
        print(f"{idx:<3} | {hash_item:<70} | {kind:<16} | {loc:<25} | {status:<10}")

    if missing_count > 0:
        print(f"\nHasil: GAGAL ({missing_count} hash tidak ditemukan di log aktual).")
        sys.exit(1)

    print(f"\nHasil: LULUS (seluruh {len(raw_hashes)} string 0x terverifikasi di log aktual).")
    sys.exit(0)

if __name__ == "__main__":
    main()
