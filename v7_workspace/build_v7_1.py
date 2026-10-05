#!/usr/bin/env python3
"""
build_v7_1.py
Script to build Laporan_UTS_Blockchain_237006079_v7.1.docx and .pdf from v7.
Preserves exact run-level font formatting (Arial/Calibri, sizes, line spacing).
Implements all requirements of KOREKSI v7 -> v7.1.
"""

import docx
from docx.shared import Pt, RGBColor
import subprocess
import os
import re

SRC_DOCX = "v7_workspace/Laporan_UTS_Blockchain_237006079_v7.docx"
OUT_DOCX = "v7_workspace/Laporan_UTS_Blockchain_237006079_v7.1.docx"
OUT_PDF = "v7_workspace/Laporan_UTS_Blockchain_237006079_v7.1.pdf"

doc = docx.Document(SRC_DOCX)

def replace_in_p(p, old, new):
    """Replace text in paragraph while preserving font name and size."""
    if not p.runs:
        if old in p.text:
            p.text = p.text.replace(old, new)
            return True
        return False
    # If old is inside a single run
    for r in p.runs:
        if old in r.text:
            r.text = r.text.replace(old, new)
            return True
    # If old spans across runs
    if old in p.text:
        fname = p.runs[0].font.name
        fsize = p.runs[0].font.size
        color = p.runs[0].font.color.rgb if p.runs[0].font.color else None
        bold = p.runs[0].font.bold
        p.text = p.text.replace(old, new)
        for r in p.runs:
            r.font.name = fname
            r.font.size = fsize
            if color:
                r.font.color.rgb = color
            r.font.bold = bold
        return True
    return False

# 1. HARDWARE SPECS UPDATE (Table 1)
t1 = doc.tables[1]
for r in t1.rows:
    for c in r.cells:
        if "Intel" in c.text and "RAM" in c.text:
            for p in c.paragraphs:
                for run in p.runs:
                    run.text = "Perangkat keras: 12th Gen Intel(R) Core(TM) i5-12450H (12 thread logis), RAM total 15 GiB. OS: Ubuntu 24.04.4 LTS x86_64, Node.js v24.14.0."

# 2. TABLE 2 UPDATES (Address & Merkle Root ellipsis to prevent wrapping violations)
t2 = doc.tables[2]
t2.rows[2].cells[2].paragraphs[0].runs[0].text = "Kontrak aktif di alamat 0x5FbDB23156..., Tx: 0x145b5523..., Gas: 1.039.368 unit [B-01]"
t2.rows[3].cells[2].text = "Pohon Merkle (129,44 ms off-chain, B-02); 6 daun bergaram, Root: 0x46ca2e83... (Tabel 5, Diagram 3, results/demo-output.txt)"
for p in t2.rows[3].cells[2].paragraphs:
    for r in p.runs:
        r.font.name = 'Arial'
        r.font.size = Pt(8.5)

t2.rows[4].cells[2].paragraphs[0].runs[0].text = (
    "Root terdaftar Block #2 tx 0x1737c359... [B-03]; verifikasi valid 0 gas [B-04]; "
    "manipulasi ditolak [B-05A/B]; cabut ijazah (Gas: 56.359 unit) [B-06]; "
    "jeda darurat pause (Gas: 48.214 unit) [B-07], Tabel 7, Tabel 9, Tabel 10"
)

# 3. TABLE 7 UPDATES (Gas Limit 60.000.000 & Tx Hash ellipsis)
for t in doc.tables:
    if "Field Transaksi EVM" in t.rows[0].cells[0].text:
        t.rows[3].cells[0].paragraphs[0].runs[0].text = "Gas Limit / Gas Used / Status"
        t.rows[3].cells[1].paragraphs[0].runs[0].text = "Gas Limit Blok: 60.000.000 (Parameter terukur node lokal Hardhat); Gas Used: 211.084 gas (penjangkaran batch); Status: 1 (Success)"
        t.rows[4].cells[0].paragraphs[0].runs[0].text = "Event Logs & Transaction Hash"
        t.rows[4].cells[1].paragraphs[0].runs[0].text = "0x1737c359... (Bukti B-03, Block #2)"

# 4. LAMPIRAN D (TABLE 12) UPDATES (Preserve exact 6.5 pt font size)
for t in doc.tables:
    if "Kelompok Uji" in t.rows[0].cells[0].text:
        for r in t.rows:
            for c in r.cells:
                for p in c.paragraphs:
                    for run in p.runs:
                        if "30M gas" in run.text:
                            run.text = run.text.replace("30M gas", "60M gas node lokal / 30M gas contoh hipotetis konsorsium")
                        if "0x06" in run.text:
                            run.text = run.text.replace("0x06", "heksadesimal 06")

# 5. PARAGRAPH UPDATES WITH PRESERVED FORMATTING
for p in doc.paragraphs:
    # Abstrak UU PDP
    replace_in_p(p, "Pasal 8 dan Pasal 43 UU PDP", "Pasal 8 dan Pasal 43 ayat (1) UU PDP")

    # Section 4.4 (P61) - Byte literal 0x03e8 and 0x06
    replace_in_p(p, "(0x03e8)", "(heksadesimal 03e8)")
    replace_in_p(p, "(0x06)", "(heksadesimal 06)")

    # Section 4.7 Keputusan Desain (~20 juta gas comparison)
    replace_in_p(
        p,
        "akan menghabiskan lebih dari 20 juta gas untuk 1.000 lulusan. Pendekatan Merkle batching mengompresi ribuan lulusan ke dalam 1 Merkle Root 32-byte [4] dengan gas konstan 164.911 gas (hemat > 98%)",
        "akan menghabiskan lebih dari 20 juta gas untuk 1.000 lulusan (menyerap 33,3% dari batas blok 60 juta gas node lokal Hardhat atau 66,7% dari contoh hipotetis 30 juta gas konsorsium). Pendekatan Merkle batching mengompresi ribuan lulusan ke dalam 1 Merkle Root 32-byte [4] dengan gas konstan 164.911 gas (hemat > 98%, hanya < 0,36% dari batas blok 60 juta gas)"
    )

    # Section 4.7 Hardware specs
    if "workstation pengembang (12th Gen Intel" in p.text:
        for r in p.runs:
            if "workstation pengembang" in r.text:
                r.text = re.sub(
                    r"workstation pengembang \([^)]+\)",
                    "workstation pengembang (12th Gen Intel(R) Core(TM) i5-12450H 12 thread logis, RAM total 15 GiB, Ubuntu 24.04.4 LTS, Node.js v24.14.0)",
                    r.text
                )

    # Section 4.7 Bullet 6 Gas Limit
    if "• 6. Batas Gas Blok:" in p.text:
        fname = p.runs[0].font.name or 'Arial'
        fsize = p.runs[0].font.size or Pt(8.5)
        p.text = (
            "• 6. Batas Gas Blok: Parameter Node Lokal Hardhat vs Hipotesis Konsorsium: Pengukuran aktual "
            "pada node lokal Hardhat melalui RPC eth_getBlockByNumber menghasilkan blockGasLimit sebesar 60.000.000 "
            "gas (0x3938700). Angka 30.000.000 gas dijadikan contoh hipotetis jaringan konsorsium untuk simulasi "
            "kapasitas blok. Penjangkaran individual 1.000 ijazah (~20 juta gas) akan menyerap sepertiga (33,3%) "
            "dari batas blok 60 juta gas atau dua pertiga (66,7%) dari contoh hipotetis 30 juta gas, sedangkan skema "
            "Merkle batching pada prototipe ini hanya memerlukan 211.084 gas (< 0,36% dari batas blok 60 juta gas)."
        )
        for r in p.runs:
            r.font.name = fname
            r.font.size = fsize

    # Section 5.1 Kesimpulan 2 (UU PDP separate articles)
    if "• 2. Perlindungan Privasi:" in p.text:
        fname = p.runs[0].font.name or 'Arial'
        fsize = p.runs[0].font.size or Pt(8.5)
        p.text = (
            "• 2. Perlindungan Privasi: Arsitektur Zero-PII On-Chain yang memisahkan dokumen lengkap off-chain "
            "bergaram (256-bit salt) dari Merkle root on-chain [4] dirancang selaras dengan prinsip pelindungan data "
            "pribadi UU No. 27 Tahun 2022 (UU PDP) [10], meliputi perlindungan klasifikasi data pribadi umum "
            "(Pasal 4 ayat (3)), pemenuhan hak penghapusan data pribadi (Pasal 8 dan Pasal 43 ayat (1)), serta hak "
            "penarikan persetujuan (Pasal 9), sekaligus mengeliminasi ancaman serangan kamus terhadap atribut bernilai rendah."
        )
        for r in p.runs:
            r.font.name = fname
            r.font.size = fsize

    # Kesimpulan 3 - Remove 100% claim
    replace_in_p(
        p,
        "terbukti 100% bersumber dari penambahan panjang parameter calldata ABI transaksi sesuai aturan EIP-2028 [11].",
        "dapat dijelaskan secara terukur bersumber dari penambahan panjang parameter calldata ABI transaksi sesuai aturan EIP-2028 [11]."
    )

    # Reference [10] Access date
    if p.text.strip().startswith("[10]"):
        replace_in_p(p, "[Diakses: 4 Oktober 2026]", "[Diakses: 5 Oktober 2026]")

# 6. ADD B-06 BULLET TO SECTION 4.7
for i, p in enumerate(doc.paragraphs):
    if "• 7. Pembulatan Calldata:" in p.text:
        p_b06 = doc.add_paragraph()
        p_b06.text = (
            "• 8. Analisis Selisih Gas Pencabutan B-06: Pada skrip demo, revokeCredential mengonsumsi 56.359 gas "
            "[B-06], sedangkan pada benchmark berkisar 55.297 s.d. 55.333 gas. Pengujian isolasi variabel tunggal "
            "(exp_b06_v2) mengonfirmasi selisih ini terbagi menjadi dua faktor terukur: (1) Perbedaan calldata EIP-2028 "
            "akibat panjang string reason (60 byte pada demo vs 11 byte 'Sidang Etik' pada benchmark) serta perbedaan "
            "byte non-nol batchId; (2) Selisih 262 gas yang terkonfirmasi melompat di batas 32 byte parameter reason "
            "pada data event CredentialRevoked (1 word data log = 256 gas ditambah 6 gas ekspansi memori). "
            "Komponen di luar kedua faktor teruji tersebut dinyatakan belum dijelaskan."
        )
        p_b06.paragraph_format.space_before = Pt(1)
        p_b06.paragraph_format.space_after = Pt(1)
        p_b06.paragraph_format.line_spacing = 1.05
        for r in p_b06.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
        p._element.addnext(p_b06._element)
        break

# 7. ADD CONCISE ACCEPTANCE CRITERIA LIST (MAX 6 LINES) IN SUBCHAPTER 4.6
for i, p in enumerate(doc.paragraphs):
    if "Kriteria penerimaan (acceptance criteria) disusun dengan merujuk" in p.text:
        p_crit = doc.add_paragraph()
        p_crit.text = (
            "Ringkasan ambang batas penerimaan luaran OBE (rincian lengkap disajikan pada Lampiran D):\n"
            "• Penjangkaran & Verifikasi (T-01, T-02): status=1, exists==true; isValid==true, status 'VALID', gas pemverifikasi = 0 (via eth_call).\n"
            "• Resistensi Manipulasi (T-03): isValid==false, status 'INVALID_PROOF_OR_TAMPERED' untuk klaim atau salt palsu.\n"
            "• Kontrol Akses Berperan (T-04, T-06): Revert seketika dengan AccessControlUnauthorizedAccount untuk akun tanpa hak.\n"
            "• Jeda Darurat & Pencabutan (T-05, T-07): Status 'CREDENTIAL_REVOKED' (O(1)); penulisan revert EnforcedPause saat jeda aktif.\n"
            "• Skalabilitas Gas & Bukti (T-08): Deviasi relatif gas eksekusi murni <= 1,0% (O(1)); panjang bukti <= ceil(log2 N) (3, 7, 10).\n"
            "• Anggaran Komputasi & Latensi (T-08): pureGas(k) <= 10.000 + 350*k gas; durasi bangun pohon Merkle off-chain < 1.000 ms."
        )
        p_crit.paragraph_format.space_before = Pt(2)
        p_crit.paragraph_format.space_after = Pt(2)
        p_crit.paragraph_format.line_spacing = 1.05
        for r in p_crit.runs:
            r.font.name = 'Arial'
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(0x1F, 0x29, 0x37)
        p._element.addnext(p_crit._element)
        break

# Tighten heading space_before / space_after slightly (preserve font, margins, and line spacing)
for p in doc.paragraphs:
    if p.paragraph_format.space_before and p.paragraph_format.space_before.pt > 4:
        p.paragraph_format.space_before = Pt(3)
    if p.paragraph_format.space_after and p.paragraph_format.space_after.pt > 3:
        p.paragraph_format.space_after = Pt(2)

doc.save(OUT_DOCX)
print(f"v7.1 DOCX saved to {OUT_DOCX}")

cmd = ["soffice", "--headless", "--convert-to", "pdf", OUT_DOCX, "--outdir", "v7_workspace"]
subprocess.run(cmd, check=True)
print(f"v7.1 PDF compiled to {OUT_PDF}")
