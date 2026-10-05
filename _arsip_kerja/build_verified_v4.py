import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# Load base v3 document
doc = docx.Document('uts-blockchain-submission/Laporan_UTS_Blockchain_237006079_v3.docx')

def update_cell_text(cell, new_text, font_name="Calibri", font_size_pt=7.5, bold=None, align=None):
    # Preserve cell formatting, clear paragraphs except first
    while len(cell.paragraphs) > 1:
        p_elem = cell.paragraphs[-1]._p
        p_elem.getparent().remove(p_elem)
    p = cell.paragraphs[0]
    p.text = ""
    if align is not None:
        p.alignment = align
    run = p.add_run(new_text)
    run.font.name = font_name
    run.font.size = Pt(font_size_pt)
    if bold is not None:
        run.font.bold = bold
    # Ensure tight spacing
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0

# 1. Update Paragraph 21
p21 = doc.paragraphs[21]
p21.text = (
    "Setiap artefak bukti pelaksanaan diberi kode referensi unik B-01 sampai B-08 dan merujuk langsung ke berkas log "
    "keluaran eksekusi nyata pada repositori prototipe (results/demo-output.txt, results/test-output.txt, dan "
    "results/perf-output.txt). Seluruh proses perancangan, implementasi prototipe, dan penyusunan laporan ini dibantu "
    "oleh agen kecerdasan artifisial (AI) sebagaimana diungkapkan secara jujur dan transparan pada Lampiran A."
)
for r in p21.runs:
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10)

# 2. Update Paragraphs 58, 59, 60, 61 (Model Regresi Linier)
p58 = doc.paragraphs[58]
p58.text = "Persamaan Regresi Linier: pureVerifyGas(k) = 7.800,04 + 251,26 * k (di mana k = jumlah sibling hash = ceil(log2 N))"
for r in p58.runs:
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10)
    r.font.bold = True

p59 = doc.paragraphs[59]
p59.text = (
    "• 1. Intercept Model: Biaya Tetap (Intercept) ≈ 7.800 gas: Berasal dari 2 kali pembacaan state storage via SLOAD "
    "(pemeriksaan batch dan status pembatalan ~4.200 gas), pemanggilan eksternal, dekoding calldata ke memori, dan "
    "pembungkusan return string. Batas kelayakan ditetapkan <= 10.000 gas (memberikan safety margin ~28% di atas hasil ukur)."
)
for r in p59.runs:
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10)

p60 = doc.paragraphs[60]
p60.text = (
    "• 2. Slope Model: Kemiringan (Slope) ≈ 251,3 gas/sibling: Merefleksikan perkiraan kasar opcode loop "
    "MerkleProof.verify [3], [4] per iterasi: KECCAK256 [6] (64 byte input: 42 gas) + MLOAD/MSTORE (6 gas) + "
    "percabangan & stack LT/JUMP/DUP/SWAP (~15 gas). Batas kelayakan ditetapkan <= 350 gas/sibling "
    "(memberikan safety margin ~39% di atas hasil ukur 251,3 gas/sibling)."
)
for r in p60.runs:
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10)

p61 = doc.paragraphs[61]
p61.text = (
    "• 3. Kriteria Evaluasi: Batas Kelayakan Performa: pureVerifyGas(k) <= 10.000 + (k * 350) gas. Untuk N=1.000 (k=10), "
    "batasnya adalah <= 13.500 gas; hasil nyata terukur adalah 10.313 gas (LULUS baseline kelayakan)."
)
for r in p61.runs:
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10)

# 3. Update Table 2 (Catatan Pelaksanaan) - v3 data font: Calibri 7.0pt
t2 = doc.tables[2]
update_cell_text(
    t2.rows[2].cells[2],
    "Kontrak aktif di alamat 0x5FbDB2315678afecb367f032d93F642f64180aa3, Tx: 0x145b5523..., Gas: 1.039.368 unit [B-01]. "
    "(Eksekusi: 4 Oktober 2026, 19:16:58 WIB, results/demo-output.txt).",
    font_name="Calibri", font_size_pt=7.0
)
update_cell_text(
    t2.rows[3].cells[2],
    "6 Daun bergaram terhitung, Merkle Root: 0x46ca2e8399d6be8a489c375dcd355319d7eaa4a92a132afdc3a00220c1faccd3 [B-02], "
    "Tabel 5, Diagram 3. (Eksekusi: 4 Oktober 2026, 19:16:58 WIB, results/demo-output.txt).",
    font_name="Calibri", font_size_pt=7.0
)
update_cell_text(
    t2.rows[4].cells[2],
    "Root terdaftar Block #2 tx 0x1737c359... [B-03]; verifikasi valid 0 gas [B-04]; manipulasi ditolak [B-05A]; "
    "peretas dicegat [B-05B] (kutipan log mentah lengkap dicantumkan pada Lampiran B); pencabutan [B-06]; pause [B-07]. "
    "8 dari 8 test lulus (T-01 s.d. T-08). Log: results/demo-output.txt dan results/test-output.txt (4 Oktober 2026).",
    font_name="Calibri", font_size_pt=7.0
)
update_cell_text(
    t2.rows[5].cells[2],
    "Gas eksekusi murni issueBatch konstan 164.911 gas (O(1)), bukti selisih calldata deterministik tepat 84 gas, "
    "model anggaran verifikasi linier [B-08], Tabel 9, Tabel 11, Tabel 13. Log: results/perf-output.txt (Eksekusi: 4 Oktober 2026, 19:17:06 WIB).",
    font_name="Calibri", font_size_pt=7.0
)

# 4. Update Table 5 (Record Daun) - v3 data font: Calibri 7.5pt
t5 = doc.tables[5]
update_cell_text(t5.rows[1].cells[3], "0x7b5f7365dffd18a8... (32 byte)", font_name="Calibri", font_size_pt=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)
update_cell_text(t5.rows[2].cells[3], "0xf3695a1ce4a97902... (32 byte)", font_name="Calibri", font_size_pt=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)
update_cell_text(t5.rows[3].cells[3], "0xca7c3acd32fa82a2... (32 byte)", font_name="Calibri", font_size_pt=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)
update_cell_text(t5.rows[4].cells[3], "0x5c97927280c16ef9... (32 byte)", font_name="Calibri", font_size_pt=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)
update_cell_text(t5.rows[5].cells[3], "0xcc0d8357be021242... (32 byte)", font_name="Calibri", font_size_pt=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)
update_cell_text(t5.rows[6].cells[3], "0x108e53ac2b7a5439... (32 byte)", font_name="Calibri", font_size_pt=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)

# 5. Update Table 8 (Detail Transaksi) - v3 data font: Calibri 7.5pt
t8 = doc.tables[8]
update_cell_text(
    t8.rows[3].cells[1],
    "Gas Limit: 30.000.000; Gas Used: 211.084 gas (penjangkaran batch); Status: 1 (Success)",
    font_name="Calibri", font_size_pt=7.5
)
update_cell_text(
    t8.rows[4].cells[1],
    "Event: BatchIssued(WISUDA-2026-PERIODE-1, 0x46ca2e83..., timestamp); "
    "Tx Hash: 0x1737c3595a7ffab660d99cb81bd14dc04b8c21f9fb399ad5b2aa454998a88321; Block: #2 [B-03]",
    font_name="Calibri", font_size_pt=7.5
)

# 6. Update Table 9 (Rincian Gas issueBatch) - v3 data font: Calibri 7.5pt
t9 = doc.tables[9]
update_cell_text(t9.rows[1].cells[1], "187.874 gas", font_name="Calibri", font_size_pt=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)
update_cell_text(t9.rows[1].cells[2], "187.922 gas", font_name="Calibri", font_size_pt=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)
update_cell_text(t9.rows[1].cells[3], "187.958 gas", font_name="Calibri", font_size_pt=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)

update_cell_text(t9.rows[3].cells[1], "1.963 gas", font_name="Calibri", font_size_pt=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)
update_cell_text(t9.rows[3].cells[2], "2.011 gas", font_name="Calibri", font_size_pt=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)
update_cell_text(t9.rows[3].cells[3], "2.047 gas", font_name="Calibri", font_size_pt=7.5, align=WD_ALIGN_PARAGRAPH.CENTER)

# 7. Update Table 11 (Kriteria Penerimaan & Justifikasi) - v3 data font: Calibri 6.5pt
t11 = doc.tables[11]
update_cell_text(t11.rows[1].cells[1], "T-01: menerbitkan batch ijazah oleh akun berwenang ISSUER_ROLE / B-03", font_name="Calibri", font_size_pt=6.5)
update_cell_text(t11.rows[2].cells[1], "T-02: memverifikasi kredensial sah menggunakan valid Merkle proof / B-04", font_name="Calibri", font_size_pt=6.5)
update_cell_text(t11.rows[3].cells[1], "T-05: mencabut status keabsahan ijazah oleh REVOKER_ROLE secara spesifik / B-06", font_name="Calibri", font_size_pt=6.5)
update_cell_text(t11.rows[4].cells[1], "T-03: menolak manipulasi klaim data IPK dan salt palsu / B-05A", font_name="Calibri", font_size_pt=6.5)
update_cell_text(t11.rows[5].cells[1], "T-04 & T-06: membatalkan upaya tanpa peran berwenang / B-05B", font_name="Calibri", font_size_pt=6.5)
update_cell_text(t11.rows[6].cells[1], "T-07: menghentikan mutasi state saat jeda darurat pause aktif / B-07", font_name="Calibri", font_size_pt=6.5)
update_cell_text(t11.rows[7].cells[1], "T-08: mengevaluasi efisiensi gas konstan O(1) / B-08", font_name="Calibri", font_size_pt=6.5)
update_cell_text(t11.rows[8].cells[1], "T-08: mengevaluasi panjang proof logaritmik O(log N) / B-08", font_name="Calibri", font_size_pt=6.5)
update_cell_text(t11.rows[9].cells[1], "T-08: evaluasi estimasi komputasi murni verifikasi / B-08", font_name="Calibri", font_size_pt=6.5)
update_cell_text(t11.rows[10].cells[1], "T-08: evaluasi waktu pembuatan Merkle tree off-chain / B-08", font_name="Calibri", font_size_pt=6.5)

update_cell_text(t11.rows[9].cells[5], "8.554 gas (N=6) hingga 10.313 gas (N=1000).", font_name="Calibri", font_size_pt=6.5)
update_cell_text(t11.rows[10].cells[5], "Rata-rata 129,44 ms (rentang 121,10 sampai 146,35 ms).", font_name="Calibri", font_size_pt=6.5)

# 8. Update Table 12 (Skenario Pengujian Unit Test) - v3 data font: Calibri 7.5pt
t12 = doc.tables[12]
test_titles = [
    "T-01: menerbitkan batch ijazah oleh akun berwenang ISSUER_ROLE",
    "T-02: memverifikasi kredensial sah menggunakan valid Merkle proof",
    "T-03: menolak manipulasi klaim data IPK dan salt palsu",
    "T-04: membatalkan upaya penerbitan batch oleh pihak tanpa peran ISSUER_ROLE",
    "T-05: mencabut status keabsahan ijazah oleh REVOKER_ROLE secara spesifik",
    "T-06: membatalkan upaya pencabutan ijazah oleh pihak tanpa peran REVOKER_ROLE",
    "T-07: menghentikan mutasi state saat jeda darurat pause aktif dan pulih pasca-unpause",
    "T-08: mengevaluasi efisiensi gas konstan O(1) dan panjang proof logaritmik O(log N)",
]
test_proofs = [
    "[B-03] / Block #2 (results/demo-output.txt)",
    "[B-04] / Gas: 0 (results/demo-output.txt)",
    "[B-05A] (results/demo-output.txt & Lampiran B)",
    "[B-05B] (results/demo-output.txt & Lampiran B)",
    "[B-06] (results/demo-output.txt)",
    "[results/test-output.txt]",
    "[B-07] (results/demo-output.txt)",
    "[B-08] (results/perf-output.txt)",
]
for idx, (title, proof) in enumerate(zip(test_titles, test_proofs)):
    update_cell_text(t12.rows[idx + 1].cells[1], title, font_name="Calibri", font_size_pt=7.5)
    update_cell_text(t12.rows[idx + 1].cells[4], proof, font_name="Calibri", font_size_pt=7.5)

# 9. Update Table 13 (Benchmark Skalabilitas 30 Run) - v3 data font: Calibri 7.5pt
t13 = doc.tables[13]
update_cell_text(t13.rows[1].cells[1], "1.43 ms (SD: 0.43) [0.87 - 2.48]", font_name="Calibri", font_size_pt=7.5)
update_cell_text(t13.rows[1].cells[2], "14.01 ms (SD: 2.92) [11.29 - 26.39]", font_name="Calibri", font_size_pt=7.5)
update_cell_text(t13.rows[1].cells[3], "129.44 ms (SD: 6.49) [121.10 - 146.35]", font_name="Calibri", font_size_pt=7.5)

update_cell_text(t13.rows[3].cells[1], "187.874 gas (SD: 8) [187.855 - 187.879]", font_name="Calibri", font_size_pt=7.5)
update_cell_text(t13.rows[3].cells[2], "187.922 gas (SD: 6) [187.915 - 187.927]", font_name="Calibri", font_size_pt=7.5)
update_cell_text(t13.rows[3].cells[3], "187.958 gas (SD: 6) [187.951 - 187.963]", font_name="Calibri", font_size_pt=7.5)

update_cell_text(t13.rows[5].cells[1], "55.303 gas (SD: 7) [55.285 - 55.309]", font_name="Calibri", font_size_pt=7.5)
update_cell_text(t13.rows[5].cells[2], "55.328 gas (SD: 6) [55.321 - 55.333]", font_name="Calibri", font_size_pt=7.5)
update_cell_text(t13.rows[5].cells[3], "55.340 gas (SD: 7) [55.321 - 55.345]", font_name="Calibri", font_size_pt=7.5)

update_cell_text(t13.rows[6].cells[1], "32.242 gas (SD: 13) [32.211 - 32.267]", font_name="Calibri", font_size_pt=7.5)
update_cell_text(t13.rows[6].cells[2], "35.311 gas (SD: 20) [35.269 - 35.347]", font_name="Calibri", font_size_pt=7.5)
update_cell_text(t13.rows[6].cells[3], "37.611 gas (SD: 25) [37.566 - 37.666]", font_name="Calibri", font_size_pt=7.5)

update_cell_text(t13.rows[7].cells[1], "2.687 gas (SD: 11) [2.664 - 2.700]", font_name="Calibri", font_size_pt=7.5)
update_cell_text(t13.rows[7].cells[2], "4.753 gas (SD: 14) [4.724 - 4.772]", font_name="Calibri", font_size_pt=7.5)
update_cell_text(t13.rows[7].cells[3], "6.298 gas (SD: 16) [6.260 - 6.320]", font_name="Calibri", font_size_pt=7.5)

update_cell_text(t13.rows[8].cells[1], "8.554 gas (SD: 8) [8.537 - 8.567]", font_name="Calibri", font_size_pt=7.5)
update_cell_text(t13.rows[8].cells[2], "9.558 gas (SD: 13) [9.535 - 9.585]", font_name="Calibri", font_size_pt=7.5)
update_cell_text(t13.rows[8].cells[3], "10.313 gas (SD: 17) [10.266 - 10.346]", font_name="Calibri", font_size_pt=7.5)
update_cell_text(t13.rows[8].cells[4], "Model Linier: 7.800 + 251,3 * k.", font_name="Calibri", font_size_pt=7.5)

update_cell_text(t13.rows[10].cells[1], "0.89 ms (SD: 0.58) [0.48 - 3.24]", font_name="Calibri", font_size_pt=7.5)
update_cell_text(t13.rows[10].cells[2], "0.87 ms (SD: 0.77) [0.38 - 3.72]", font_name="Calibri", font_size_pt=7.5)
update_cell_text(t13.rows[10].cells[3], "0.82 ms (SD: 0.26) [0.55 - 1.46]", font_name="Calibri", font_size_pt=7.5)

# 10. REORGANIZE APPENDICES WITH PROPER OOXML STRUCTURE
# In v3:
# Child 124: p (Daftar Pustaka [12])
# Child 125: p (Lampiran A Heading)
# Child 126: p (Pernyataan)
# Child 127: tbl (Table 14 - Signature Table)
# Child 128: p (Lampiran B Heading)
# Child 129: p (Pengantar AI)
# Child 130: p (Claude)
# Child 131: p (Antigravity)
# Child 132: p (Tanggung Jawab)
# Child 133: sectPr

body = doc._body._element
t14 = doc.tables[14]
t14_elem = t14._element

# Detach t14 from its current position
t14_elem.getparent().remove(t14_elem)

# Remove old appendix paragraphs (111 to end)
for p in list(doc.paragraphs[111:]):
    p_elem = p._p
    p_elem.getparent().remove(p_elem)

# sectPr is currently at end of body. We will insert elements before sectPr!
sectPr = body.xpath('w:sectPr')[-1]

def add_elem_before_sectPr(new_p):
    sectPr.addprevious(new_p._p)

# Create helper for paragraphs
def make_paragraph(text, style='Normal', space_before=0, space_after=4, line_spacing=1.15, bold=False, italic=False, font_size=10, font_name='Times New Roman', is_heading=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    run = p.add_run(text)
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    if is_heading:
        run.font.color.rgb = RGBColor(0, 0, 0)
    # Detach from doc and return
    p._p.getparent().remove(p._p)
    return p

# --- Lampiran A: Pengungkapan AI ---
p_h_a = make_paragraph("Lampiran A: Pengungkapan Penggunaan Alat Bantu AI Transparan", space_before=14, space_after=4, bold=True, font_size=12, is_heading=True)
p_a1 = make_paragraph("Sesuai panduan etika akademik perguruan tinggi dan ketentuan naskah ujian OBE, penggunaan asisten kecerdasan artifisial (AI) dalam penyusunan tugas ini diungkapkan secara transparan sebagai berikut:", space_after=3)
p_a2 = make_paragraph("• 1. Claude (Anthropic): Digunakan pada Fase Eksplorasi & Desain Arsitektur (Fase 1) untuk melakukan brainstorming perbandingan arsitektur konsorsium versus public blockchain, serta perumusan awal model ancaman STRIDE.", space_after=3)
p_a3 = make_paragraph("• 2. Google Antigravity Agent: Digunakan pada Fase Rekayasa Prototipe & Verifikasi Eksperimental (Fase 2, 2b, dan 3) untuk otomatisasi eksekusi unit test Hardhat, komputasi biaya calldata EIP-2028, eksekusi benchmark performa 30 run, penyusunan model regresi linier, pembangkitan diagram Graphviz, serta formatting berkas laporan akhir.", space_after=3)
p_a4 = make_paragraph("• 3. Tanggung Jawab Penulis: Seluruh logika smart contract, angka konsumsi gas, hasil verifikasi tamper-evident, serta analisis kritis pada dokumen ini telah divalidasi, dieksekusi secara nyata di lingkungan komputasi lokal, dan diverifikasi kebenarannya oleh penulis.", space_after=6)

for p in [p_h_a, p_a1, p_a2, p_a3, p_a4]:
    add_elem_before_sectPr(p)

# --- Page Break before Lampiran B ---
p_pb_b = doc.add_paragraph()
p_pb_b.paragraph_format.space_before = Pt(0)
p_pb_b.paragraph_format.space_after = Pt(0)
p_pb_b.add_run().add_break(docx.enum.text.WD_BREAK.PAGE)
p_pb_b._p.getparent().remove(p_pb_b._p)
add_elem_before_sectPr(p_pb_b)

# --- Lampiran B: Keluaran Eksekusi B-05 ---
p_h_b = make_paragraph("Lampiran B: Keluaran Eksekusi Prototipe (Bukti B-05: Pengujian Anti-Tampering dan Kontrol Akses RBAC)", space_before=12, space_after=4, bold=True, font_size=12, is_heading=True)
p_b_intro = make_paragraph(
    "Kutipan teks log mentah keluaran eksekusi terminal Hardhat secara langsung dari berkas results/demo-output.txt (skenario B-05 baris 47–57) yang memvalidasi penolakan manipulasi klaim data IPK dan pencegatan eksekusi oleh pihak tanpa peran ISSUER_ROLE (dengan penandaan pemotongan string [dipotong] pada argumen eksepsi kontrol akses konsol):",
    space_after=4
)

b05_lines = [
    "[B-05 Uji Ketahanan Manipulasi Data dan Kontrol Akses RBAC]",
    "Skenario 5A: Pelamar mengubah IPK 3.82 menjadi 4.00 pada berkas lokal",
    "Leaf Asli            : 0x7b5f7365dffd18a87fb7b5471e7843da27e53b4ec53e8e1ef064b78ab3b0645c",
    "Leaf Hasil Manipulasi: 0x0b097c59bcd2b3d0b5cba350b03cea87b34b4294eba79c5d5cf2f0a548d04f97",
    "Hasil Verifikasi     : DITOLAK / INVALID (FALSE)",
    "Pesan Status Kontrak : INVALID_PROOF_OR_TAMPERED",
    "",
    "Skenario 5B: Upaya penerbitan batch oleh penyerang tanpa hak (Attacker)",
    "Hasil Pencegatan RBAC: Transaksi Dibatalkan (Reverted)",
    "Eksepsi Kontrak      : VM Exception while processing transaction: reverted with custom error 'AccessControlUnauthorizedAccount(\"0x9965507D1a55bcC2695C58ba16FB37d819B0A4dc\", \"0x5824905f...\")' [dipotong]"
]

p_b_box = make_paragraph("\n".join(b05_lines), space_before=2, space_after=6, line_spacing=1.05, font_size=8.5, font_name='Consolas')

for p in [p_h_b, p_b_intro, p_b_box]:
    add_elem_before_sectPr(p)

# --- Page Break before Lampiran C to guarantee Lampiran C is isolated on Page 17 ---
p_page_break = doc.add_paragraph()
p_page_break.paragraph_format.space_before = Pt(0)
p_page_break.paragraph_format.space_after = Pt(0)
run_pb = p_page_break.add_run()
run_pb.add_break(docx.enum.text.WD_BREAK.PAGE)
p_page_break._p.getparent().remove(p_page_break._p)
add_elem_before_sectPr(p_page_break)

# --- Lampiran C: Pernyataan Orisinalitas ---
p_h_c = make_paragraph("Lampiran C: Pernyataan Orisinalitas", space_before=14, space_after=6, bold=True, font_size=12, is_heading=True)
p_c_stmt = make_paragraph("Saya menyatakan bahwa jawaban ujian dan mini-project ini merupakan hasil kerja saya sendiri. Seluruh sumber dan penggunaan alat bantu telah saya ungkapkan secara jujur sesuai ketentuan mata kuliah.", space_after=10)

add_elem_before_sectPr(p_h_c)
add_elem_before_sectPr(p_c_stmt)

# Now add t14 right after p_c_stmt!
p_c_stmt._p.addnext(t14_elem)

# Check that sectPr is still the last child of body
children = list(body)
print(f"Final total children in body: {len(children)}")
print(f"Last child tag: {children[-1].tag.split('}')[-1]}")
print(f"Second to last child tag: {children[-2].tag.split('}')[-1]}")

doc.save('verified_v4.docx')
print("verified_v4.docx saved successfully!")
