#!/usr/bin/env python3
"""
Test layout tuning script to verify exact page fitting for all questions.
"""
import os
import subprocess
import re
import docx
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

BASE_DIR = "/home/fajar-geran-arifin/Documents/kuliah/block chain/UTS bagian A"
TEST_DOCX = os.path.join(BASE_DIR, "UTS_Blockchain_Bagian_A_237006079_Fajar_Geran_Arifin_JAWABAN.docx")
TEST_PDF = os.path.join(BASE_DIR, "UTS_Blockchain_Bagian_A_237006079_Fajar_Geran_Arifin_JAWABAN.pdf")
IMG_DIR = os.path.join(BASE_DIR, "gambar")

FOREIGN_TERMS = [
    "checks-effects-interactions", "nonreentrant guard", "reentrancy guard",
    "smart contract", "smart contracts", "private key", "private keys",
    "public key", "public keys", "browser wallet", "hardware wallet",
    "hot wallet", "cold storage", "blind signing", "clear signing",
    "single point of failure", "defense-in-depth", "crash fault tolerant",
    "byzantine fault tolerant", "ordering service", "peer node", "peer nodes",
    "chain of custody", "working copy", "master copy", "evidence log sheet",
    "common-input ownership", "deposit address clustering", "temporal analysis",
    "time-lock controller", "time-lock", "multisignature", "multi-signature",
    "decentralized exchange", "decentralized exchanges", "centralized exchange",
    "centralized exchanges", "permissioned blockchain", "consortium blockchain",
    "permissioned", "consortium", "circuit breaker", "pause switch",
    "property-based testing", "property-based test", "unit testing", "unit test",
    "unit tests", "mock exploit contract", "mock contract", "mock contracts", "mock recall",
    "canary launch", "deposit cap", "deposit caps", "gas fee", "gas fees",
    "event log", "event logs", "internal trace", "internal traces",
    "transaction hash", "transaction hashes", "block height",
    "write-once-read-many", "bit-stream image", "bit-stream disk image", "memory dump",
    "freeze request", "freeze requests", "mule account", "mule accounts",
    "staleness check", "price deviation guard", "reentrancy", "oracle", "oracles",
    "wallet", "wallets", "ledger", "ledgers", "chaincode", "chaincodes",
    "fuzzing", "invariant", "invariants", "exploit", "exploits", "layering",
    "bridge", "bridges", "swap", "swaps", "router", "routers", "nonce",
    "subpoena", "subpoenas", "sweeping", "clustering", "typosquatting",
    "phishing", "malware", "infostealer", "allowlist", "spending limit",
    "spending limits", "payload", "payloads", "receipt", "receipts",
    "token", "tokens", "vault", "vaults", "testnet", "mainnet",
    "on-chain", "off-chain", "cross-chain", "read-only", "underflow",
    "overflow", "fallback", "feed", "feeds", "hash", "hashes", "digest",
    "digests", "query", "queries", "node", "nodes", "log", "logs",
    "peer", "peers", "commit", "channel", "channels", "gossip",
    "safetransfer", "nonreentrant", "require", "balances", "updatedat",
    "pausable", "end-to-end", "spot", "fan-out", "origin", "proof-of-stake",
    "state", "states", "order-execute", "execute-order-validate",
    "private data collections", "private data collection",
    "membership service provider", "certificate authority"
]

TERMS_SORTED = sorted(FOREIGN_TERMS, key=len, reverse=True)
REGEX_FOREIGN = re.compile(r"\b(" + "|".join(re.escape(t) for t in TERMS_SORTED) + r")\b", re.IGNORECASE)

def sanitize_text(text):
    text = text.replace("\u2014", ", ")
    text = text.replace("\u2013", "-")
    return text

def parse_runs_with_styling(text, base_bold=False, base_italic=False):
    text = sanitize_text(text)
    parts = re.split(r"(\*\*[^*]+\*\*)", text)
    runs = []
    
    for part in parts:
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            inner = part[2:-2]
            last_idx = 0
            for m in REGEX_FOREIGN.finditer(inner):
                s, e = m.span()
                if s > last_idx:
                    runs.append((inner[last_idx:s], True, base_italic))
                runs.append((inner[s:e], True, True))
                last_idx = e
            if last_idx < len(inner):
                runs.append((inner[last_idx:], True, base_italic))
        else:
            subparts = re.split(r"(\*[^*]+\*)", part)
            for sub in subparts:
                if not sub:
                    continue
                if sub.startswith("*") and sub.endswith("*"):
                    runs.append((sub[1:-1], base_bold, True))
                else:
                    last_idx = 0
                    for m in REGEX_FOREIGN.finditer(sub):
                        s, e = m.span()
                        if s > last_idx:
                            runs.append((sub[last_idx:s], base_bold, base_italic))
                        runs.append((sub[s:e], base_bold, True))
                        last_idx = e
                    if last_idx < len(sub):
                        runs.append((sub[last_idx:], base_bold, base_italic))
                        
    return runs

def set_cell_margins(cell, top=35, bottom=35, left=85, right=85):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_cell_shading(cell, color_hex="F2F2F2"):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_table_borders_black(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="000000"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="000000"/>
            <w:left w:val="single" w:sz="6" w:space="0" w:color="000000"/>
            <w:right w:val="single" w:sz="6" w:space="0" w:color="000000"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>
            <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def build_test():
    doc = Document()
    s = doc.sections[0]
    s.page_width = Cm(21.0)
    s.page_height = Cm(29.7)
    s.top_margin = Cm(2.54)
    s.bottom_margin = Cm(2.54)
    s.left_margin = Cm(2.54)
    s.right_margin = Cm(2.54)

    st_norm = doc.styles['Normal']
    st_norm.font.name = 'Times New Roman'
    st_norm.font.size = Pt(12)
    st_norm.font.color.rgb = RGBColor(0, 0, 0)

    def add_para(text, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=1.2, line_spacing=1.06, keep_with_next=False):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        p.paragraph_format.keep_with_next = keep_with_next
        runs = parse_runs_with_styling(text)
        for r_text, r_bold, r_italic in runs:
            r = p.add_run(r_text)
            r.bold = r_bold
            r.italic = r_italic
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
        return p

    def add_item(label, body, space_before=0.3, space_after=0.8, line_spacing=1.06, keep_with_next=False):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        p.paragraph_format.keep_with_next = keep_with_next
        lbl_runs = parse_runs_with_styling(label, base_bold=True)
        for r_text, r_bold, r_italic in lbl_runs:
            r = p.add_run(r_text)
            r.bold = True
            r.italic = r_italic
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
        body_runs = parse_runs_with_styling(body, base_bold=False)
        for r_text, r_bold, r_italic in body_runs:
            r = p.add_run(r_text)
            r.bold = r_bold
            r.italic = r_italic
            r.font.name = 'Times New Roman'
            r.font.size = Pt(12)
        return p

    def add_case_title(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.06
        p.paragraph_format.keep_with_next = True
        run = p.add_run(sanitize_text(text))
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        return p

    def add_question(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.line_spacing = 1.06
        p.paragraph_format.keep_with_next = True
        run = p.add_run(sanitize_text(text))
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        return p

    def add_answer_label(space_before=1.5, space_after=1.0):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.06
        p.paragraph_format.keep_with_next = True
        r = p.add_run("Jawaban:")
        r.bold = True
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)
        return p

    def add_table_custom(table_id, title, headers, data, col_widths, font_size=Pt(8.5), cell_padding_y=30):
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_cap.paragraph_format.space_before = Pt(3)
        p_cap.paragraph_format.space_after = Pt(1.5)
        p_cap.paragraph_format.keep_with_next = True
        cap_runs = parse_runs_with_styling(f"Tabel {table_id}. {title}", base_bold=True)
        for r_text, r_bold, r_italic in cap_runs:
            r = p_cap.add_run(r_text)
            r.bold = True
            r.italic = r_italic
            r.font.name = 'Times New Roman'
            r.font.size = Pt(10.5)

        t = doc.add_table(rows=len(data) + 1, cols=len(headers))
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders_black(t)
        trPr0 = t.rows[0]._tr.get_or_add_trPr()
        trPr0.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        for row in t.rows:
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

        hdr_cells = t.rows[0].cells
        for c_idx, h_text in enumerate(headers):
            hdr_cells[c_idx].width = col_widths[c_idx]
            set_cell_margins(hdr_cells[c_idx], top=cell_padding_y, bottom=cell_padding_y, left=80, right=80)
            set_cell_shading(hdr_cells[c_idx], "F2F2F2")
            p = hdr_cells[c_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            runs = parse_runs_with_styling(h_text, base_bold=True)
            for r_text, r_bold, r_italic in runs:
                r = p.add_run(r_text)
                r.bold = True
                r.italic = r_italic
                r.font.name = 'Times New Roman'
                r.font.size = Pt(9.0)

        for r_idx, row_data in enumerate(data):
            row_cells = t.rows[r_idx + 1].cells
            shd_col = "FFFFFF" if r_idx % 2 == 0 else "F9F9F9"
            for c_idx, cell_value in enumerate(row_data):
                row_cells[c_idx].width = col_widths[c_idx]
                set_cell_margins(row_cells[c_idx], top=cell_padding_y, bottom=cell_padding_y, left=75, right=75)
                set_cell_shading(row_cells[c_idx], shd_col)
                p = row_cells[c_idx].paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.05
                runs = parse_runs_with_styling(cell_value, base_bold=False)
                for r_text, r_bold, r_italic in runs:
                    r = p.add_run(r_text)
                    r.bold = r_bold
                    r.italic = r_italic
                    r.font.name = 'Times New Roman'
                    r.font.size = font_size

    def add_figure_custom(fig_id, title, filename, width_cm, explanation):
        img_path = os.path.join(IMG_DIR, filename)
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(2)
        p_img.paragraph_format.space_after = Pt(1.5)
        p_img.paragraph_format.keep_with_next = True
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=Cm(width_cm))

        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(1.5)
        p_cap.paragraph_format.space_after = Pt(2.5)
        p_cap.paragraph_format.keep_with_next = True
        cap_runs = parse_runs_with_styling(f"Gambar {fig_id}. {title}", base_bold=False, base_italic=True)
        for r_text, r_bold, r_italic in cap_runs:
            r = p_cap.add_run(r_text)
            r.bold = r_bold
            r.italic = True
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)

        add_item("Penjelasan Gambar: ", explanation, space_before=1.0, space_after=2.0)

    # 1. Page 1: Identitas + Kasus 1 + Soal 1.1
    for line in [
        "Nama\t: Fajar Geran Arifin",
        "NPM\t: 237006079",
        "Kelas\t: C",
        "Mata Kuliah\t: Blockchain",
        "Dosen Pengampu\t: Dr. Ir. Nur Widiyasono, M.Kom."
    ]:
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1.0)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run(line)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(12)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(1.0)
    p_title.paragraph_format.keep_with_next = True
    r_t = p_title.add_run("Bagian A Ujian Berbasis Kasus")
    r_t.bold = True
    r_t.font.name = 'Times New Roman'
    r_t.font.size = Pt(12)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(3)
    r_s = p_sub.add_run("Bobot 60 poin. Bacalah konteks setiap kasus, kemudian jawab seluruh pertanyaan secara argumentatif.")
    r_s.font.name = 'Times New Roman'
    r_s.font.size = Pt(12)

    add_case_title("Kasus 1 Sistem Ketertelusuran Produk Pangan")
    add_para("Sebuah konsorsium terdiri atas koperasi petani, pabrik pengolahan, perusahaan logistik, laboratorium mutu, dan jaringan ritel. Saat ini data lot produksi tersimpan pada basis data masing-masing organisasi. Ketika terjadi penarikan produk, pencocokan nomor lot memerlukan dua hingga tiga hari. Konsorsium ingin memperoleh jejak audit bersama, tetapi harga pemasok dan identitas petani tertentu tidak boleh terlihat oleh semua pihak. Volume transaksi diperkirakan 25 transaksi per detik dan peserta jaringan telah diketahui identitasnya.", space_after=2.5)

    add_question("1.1 Identifikasi tiga kebutuhan bisnis dan dua kendala teknis yang menentukan desain sistem. [4 poin | CPMK 1 dan CPMK 2 | C4]")
    add_answer_label()
    add_para("Berdasarkan konteks konsorsium rantai pasok pangan, berikut adalah identifikasi tiga kebutuhan bisnis dan dua kendala teknis penentu desain sistem:")
    add_para("A. Tiga Kebutuhan Bisnis:", space_before=0.8, space_after=0.8, keep_with_next=True)
    add_item("1. Jejak Audit Bersama yang Abadi (Immutable Audit Trail): ", 
             "Konsorsium membutuhkan satu sumber kebenaran data tunggal yang transparan dan tahan manipulasi untuk mendokumentasikan silsilah bahan baku dari perkebunan hingga gerai ritel, mengeliminasi sengketa data dan ketergantungan rekonsiliasi manual antar-organisasi.")
    add_item("2. Akselerasi Penarikan Produk (Rapid Product Recall): ", 
             "Memangkas durasi pencocokan nomor lot terdampak dari dua sampai tiga hari menjadi hitungan menit atau jam guna memitigasi risiko keamanan konsumen dan menekan kerugian finansial akibat penarikan massal yang salah sasaran.")
    add_item("3. Perlindungan Kerahasiaan Komersial Selektif (Selective Confidentiality): ", 
             "Melindungi data bisnis rahasia, seperti harga pembelian bahan baku antar-pemasok dan identitas privat petani tertentu, agar tidak terlihat oleh pihak non-rekanan, namun integritas dan keabsahan transaksinya tetap dapat diverifikasi.")
    add_para("B. Dua Kendala Teknis:", space_before=0.8, space_after=0.8, keep_with_next=True)
    add_item("1. Throughput Transaksi dan Finalitas Deterministik: ", 
             "Sistem harus mampu memproses throughput operasional sekitar 25 transaksi per detik dengan latensi rendah dan finalitas deterministik tanpa risiko percabangan ledger, guna menjamin kelancaran serah terima operasional logistik.")
    add_item("2. Penyimpanan Hibrida dan Integrasi Sistem Warisan: ", 
             "Berkas biner berukuran besar (foto komoditas, sertifikat inspeksi, berkas laporan laboratorium) tidak layak disimpan langsung di on-chain ledger karena beban komputasi node, sehingga memerlukan integrasi penyimpanan off-chain terenkripsi serta penyelarasan dengan basis data internal ERP eksisting.")

    # 2. Page 2: Soal 1.2 + Tabel 1
    doc.add_page_break()
    add_question("1.2 Pilih jenis blockchain dan mekanisme konsensus yang paling sesuai. Bandingkan pilihan Anda dengan sekurang-kurangnya satu alternatif. [5 poin | CPMK 2 | C5]")
    add_answer_label()
    add_para("A. Pemilihan Jenis Blockchain dan Mekanisme Konsensus:", space_before=0.8, space_after=0.8, keep_with_next=True)
    add_para("Jenis blockchain yang paling tepat adalah permissioned consortium blockchain berbasis Hyperledger Fabric, dengan mekanisme konsensus ordering service berbasis Byzantine Fault Tolerant, yaitu SmartBFT.")
    add_para("B. Argumentasi dan Analisis Trade-off:", space_before=0.8, space_after=0.8, keep_with_next=True)
    add_item("1. Kesesuaian Tata Kelola: ", 
             "Seluruh anggota konsorsium telah diketahui identitas hukumnya. Hyperledger Fabric mengautentikasi setiap node melalui Certificate Authority (CA) dan Membership Service Provider (MSP), meniadakan mekanisme penambangan anonim publik yang boros energi dan biaya transaksi gas fee fluktuatif.")
    add_item("2. Skalabilitas Performa: ", 
             "Beban 25 transaksi per detik tergolong sangat wajar dan berada jauh di bawah kapasitas puncak Hyperledger Fabric yang mampu melayani ratusan hingga ribuan transaksi per detik dengan finalitas deterministik sub-detik.")
    add_item("3. Analisis Trade-off Konsensus: ", 
             "Konsensus Raft (Crash Fault Tolerant) memang berkinerja tinggi, namun hanya tahan terhadap node yang padam, bukan node yang bertindak curang atau mengirimkan data bertentangan. Karena anggota konsorsium adalah entitas bisnis independen dengan potensi persaingan komersial, SmartBFT jauh lebih unggul karena mampu mentoleransi hingga f node jahat dari total 3f + 1 node pemesanan.")
    add_para("C. Evaluasi Komparatif terhadap Alternatif:", space_before=0.8, space_after=0.8, keep_with_next=True)
    add_para("Perbandingan komparatif antara Hyperledger Fabric yang diusulkan terhadap alternatif jaringan blockchain lainnya dirangkum secara sistematis pada Tabel 1.")

    t1_headers = ["Kriteria Evaluasi", "Hyperledger Fabric (SmartBFT)\n[Pilihan yang Diusulkan]", "Ethereum Publik (PoS)\n[Alternatif 1]", "Hyperledger Besu (IBFT 2.0)\n[Alternatif 2]"]
    t1_data = [
        ("Akses Jaringan", "Permissioned consortium; akses terbatas bagi anggota terdaftar.", "Permissionless publik; siapa pun dapat membaca dan menulis data.", "Permissioned private; akses node dibatasi oleh smart contract."),
        ("Mekanisme Konsensus", "SmartBFT (Byzantine Fault Tolerant) pada ordering service.", "Proof-of-Stake (PoS) berbasis validator publik global.", "IBFT 2.0 / QBFT berbasis voting antar-validator terpercaya."),
        ("Privasi Data Bisnis", "Tinggi; isolasi bilateral via Private Data Collections dan channel.", "Rendah; data transaksi dan payload terbuka transparan on-chain.", "Sedang; privasi grup via Tessera / Orion private transactions."),
        ("Finalitas Transaksi", "Instan dan deterministik (sub-detik tanpa risiko fork).", "Probabilistik; finalitas blok membutuhkan waktu 12 sampai 15 menit.", "Deterministik instan dalam hitungan detik per blok."),
        ("Biaya Transaksi", "Nol biaya gas fee per transaksi (biaya operasional infrastruktur).", "Fluktuatif dan tinggi mengikuti beban pasar gas fee.", "Nol gas fee internal (dapat disetel biaya gas nol)."),
        ("Tata Kelola Jaringan", "Ketat via Certificate Authority (CA) dan MSP berbasis PKI.", "Terdesentralisasi publik tanpa identitas hukum terikat.", "Konsorsium berbasis daftar izin alamat akun validator."),
        ("Kecocokan Beban 25 TPS", "Sangat optimal; throughput kapasitas Fabric mencapai >1000 TPS.", "Kurang cocok; rentan kemacetan antrean transaksi dan lonjakan biaya.", "Cukup optimal; mampu menangani ratusan TPS stabil.")
    ]
    t1_widths = [Cm(3.8), Cm(4.3), Cm(3.9), Cm(3.9)]
    add_table_custom("1", "Perbandingan platform blockchain dan mekanisme konsensus", t1_headers, t1_data, t1_widths, font_size=Pt(8.5))

    # 3. Page 3: Soal 1.3 + Gambar 1
    doc.add_page_break()
    add_question("1.3 Gambarkan arsitektur logis yang menunjukkan aktor, node, data on-chain, data off-chain, serta mekanisme kontrol akses. [4 poin | CPMK 2 | C6]")
    add_answer_label()
    add_para("Arsitektur logis sistem ketertelusuran produk pangan terintegrasi yang diusulkan ditampilkan pada Gambar 1.")
    add_figure_custom(
        fig_id="1",
        title="Arsitektur logis sistem ketertelusuran pangan",
        filename="gambar1-arsitektur.png",
        width_cm=15.0,
        explanation="Arsitektur pada Gambar 1 mengintegrasikan lima aktor konsorsium (Koperasi, Pabrik Pengolah, Perusahaan Logistik, Laboratorium, dan Jaringan Ritel) yang berinteraksi melalui Aplikasi Organisasi untuk submit transaksi dan monitoring lot, serta Aplikasi Keterlacakan untuk akses publik konsumen via pemindaian kode QR. Pada lapisan jaringan Hyperledger Fabric, setiap organisasi mengoperasikan peer node yang menyimpan world state (CouchDB) dan mengeksekusi logika bisnis smart contract (chaincode). Konsensus pengurutan transaksi dikelola secara terdesentralisasi oleh klaster ordering service berbasis SmartBFT (Node 1 sampai 4) yang mendistribusikan blok ke bar validasi dan pencatatan ledger guna verifikasi kebijakan endorsement dan validasi konflik versi MVCC. Sistem menerapkan penyimpanan hibrida: data transaksi bernilai tinggi (nomor lot universal, relasi silsilah antar-lot, jejak peristiwa serah terima, status mutu, status penarikan, serta hash dokumen pendukung) disimpan secara permanen pada on-chain ledger, sedangkan dokumen berukuran besar (berkas laporan uji laboratorium, faktur komersial, foto komoditas, dan rekaman telemetri sensor IoT) disimpan pada penyimpanan off-chain terenkripsi (IPFS atau penyimpanan cloud privat). Data komersial sensitif seperti harga pemasok dilindungi secara bilateral menggunakan Private Data Collections via protokol Fabric Gossip. Seluruh interaksi diamankan oleh Certificate Authority (CA) dan Membership Service Provider (MSP) berbasis PKI X.509 dan kontrol akses berbasis peran (RBAC), dengan penegakan aturan di mana penerbitan hasil uji mutu mutlak menjadi wewenang laboratorium dan serah terima logistik mewajibkan endorsement ganda dari pengirim dan penerima."
    )

    # 4. Page 4: Soal 1.4 + Kasus 2 + Soal 2.1 + Tabel 2
    doc.add_page_break()
    add_question("1.4 Tetapkan dua indikator keberhasilan pilot project yang dapat diukur. [2 poin | CPMK 1 | C4]")
    add_answer_label()
    add_para("Dua indikator keberhasilan target rancangan pilot project yang diusulkan ditetapkan sebagai berikut:")
    add_item("1. Durasi Pelacakan Silsilah Lot (Recall Traceability Time): ", 
             "Waktu penelusuran silsilah lot lengkap dari hulu ke hilir ditargetkan terpangkas dari dua sampai tiga hari menjadi di bawah 15 menit, diuji melalui simulasi pengujian penarikan produk (mock recall) berkala hingga seluruh rantai pasok terdampak teridentifikasi.")
    add_item("2. Tingkat Kelengkapan Pencatatan Data Lot (Data Completeness Rate): ", 
             "Ditargetkan minimal 95% dari total pergerakan lot komoditas selama fase uji coba tercatat secara valid dan end-to-end pada ledger on-chain, diverifikasi melalui audit rekonsiliasi data mingguan antara basis data ERP internal dengan transaksi blockchain.")

    add_case_title("Kasus 2 Insiden Wallet Organisasi")
    add_para("Wallet treasury sebuah organisasi blockchain kehilangan aset setelah seorang staf menyetujui transaksi yang tampil sebagai pembaruan kontrak. Log menunjukkan login dari perangkat staf yang sah, tetapi domain antarmuka berbeda satu karakter dari domain resmi. Private key disimpan pada browser wallet; tidak ada multisignature, allowlist alamat, maupun prosedur respons insiden. Organisasi meminta analisis akar masalah dan rencana pemulihan.", space_after=2.5)

    add_question("2.1 Susun urutan kejadian yang paling mungkin dan bedakan fakta, hipotesis, serta bukti yang masih perlu dikumpulkan. [4 poin | CPMK 4 | C4]")
    add_answer_label()
    add_para("Analisis pemilahan antara fakta kasus, hipotesis investigatif, dan bukti forensik digital yang perlu dihimpun disajikan pada Tabel 2.")

    t2_headers = ["Fakta (Berdasarkan Teks Kasus)", "Hipotesis Investigatif", "Bukti Forensik yang Perlu Dikumpulkan"]
    t2_data = [
        ("Login berasal dari perangkat staf sah; domain berbeda satu karakter.", 
         "Staf menjadi korban rekayasa sosial phishing typosquatting akibat kekeliruan navigasi atau tautan berbahaya.", 
         "Riwayat penjelajahan browser, DNS cache lokal, log proxy jaringan, dan data registrasi domain WHOIS."),
        ("Transaksi tampil sebagai 'pembaruan kontrak' pada antarmuka dApp.", 
         "Antarmuka palsu memanipulasi tampilan narasi transaksi untuk memicu persetujuan buta (blind signing).", 
         "Source code antarmuka web palsu, skrip injeksi web3, payload transaksi mentah, dan ABI smart contract."),
        ("Private key disimpan langsung pada browser wallet tanpa multisignature.", 
         "Kunci privat terekspos tanpa perlindungan otorisasi ganda atau segregasi wewenang operasional.", 
         "Berkas vault browser wallet terenkripsi, log ekstensi peramban, dan riwayat otorisasi izin dApp."),
        ("Staf menyetujui dan menandatangani transaksi menggunakan private key.", 
         "Muatan transaksi berisi instruksi transfer saldo langsung atau persetujuan token tak terbatas.", 
         "Transaction hash on-chain, data heksadesimal input transaksi, dan status pemindahan aset."),
        ("Aset treasury hilang; ketiadaan allowlist dan SOP respons insiden.", 
         "Ketiadaan batas transaksi memungkinkan penyerang menguras saldo treasury dalam sekali eksekusi.", 
         "Alamat penampung aset milik penyerang di blockchain dan salinan mutasi buku besar internal.")
    ]
    t2_widths = [Cm(5.1), Cm(5.2), Cm(5.6)]
    add_table_custom("2", "Pemilahan fakta, hipotesis, dan bukti forensik insiden", t2_headers, t2_data, t2_widths, font_size=Pt(9.0))

    # 5. Page 5: Gambar 2 + Soal 2.2
    doc.add_page_break()
    add_para("Rekonstruksi kronologis kejadian berdasarkan tahapan waktu divisualisasikan dalam bentuk linimasa kejadian pada Gambar 2.", space_after=1.5)
    add_figure_custom(
        fig_id="2",
        title="Linimasa kejadian insiden wallet organisasi",
        filename="gambar2-linimasa.png",
        width_cm=12.2,
        explanation="Linimasa pada Gambar 2 memetakan tujuh titik kejadian secara kronologis dari kiri ke kanan. Garis solid merepresentasikan fakta empiris yang terkonfirmasi (login perangkat sah, narasi antarmuka palsu, persetujuan staf via browser wallet, dan hilangnya saldo treasury), sedangkan garis putus-putus merepresentasikan hipotesis investigatif (distribusi tautan jebakan, bentuk muatan transaksi transfer/approval, perpindahan lanjut oleh penyerang, dan waktu organisasi pertama kali menyadari insiden). Pada baris bawah, setiap tahapan dipadukan dengan inventarisasi bukti digital yang wajib diakuisisi oleh tim investigasi guna pembuktian komprehensif."
    )
    add_question("2.2 Jelaskan bagaimana tanda tangan digital tetap valid meskipun transaksi terjadi akibat rekayasa sosial. [3 poin | CPMK 3 | C4]")
    add_answer_label()
    add_para("Tanda tangan digital berbasis kriptografi kurva eliptik (ECDSA secp256k1) tetap valid secara teknis karena protokol blockchain hanya menguji keabsahan matematis dari pasangan kunci dan integritas pesan data, bukan menguji intensi atau konteks kebenaran manusiawi pembuat tanda tangan (kebutaan semantik atau semantic blindness).")
    add_para("Secara operasional, verifikasi kriptografis membuktikan dua kondisi mutlak: pertama, transaksi ditandatangani oleh pemegang private key sah yang berpasangan secara matematis dengan public key pengirim; kedua, muatan biner payload transaksi tidak mengalami perubahan sedikit pun sejak penandatanganan dilakukan. Ketika staf terpedaya rekayasa sosial, staf secara sadar mengeksekusi instruksi penandatanganan menggunakan private key resmi yang tersimpan di dalam browser wallet.")
    add_para("Pada kasus ini berlangsung fenomena blind signing: antarmuka dApp palsu menampilkan teks manipulatif 'Pembaruan Kontrak', padahal payload heksadesimal mentah yang disodorkan adalah instruksi pemindahan saldo atau approval tak terbatas. Karena penandatanganan dilakukan menggunakan private key yang sah, validator jaringan memproses transaksi tersebut sebagai instruksi yang sepenuhnya legal, terlepas dari fakta bahwa persetujuan staf didasari oleh manipulasi informasi visual.")

    # 6. Page 6: Soal 2.3 + Gambar 3
    doc.add_page_break()
    add_question("2.3 Rancang pengamanan berlapis yang mencakup manusia, proses, wallet, dan kontrol transaksi. [5 poin | CPMK 3 dan CPMK 4 | C6]")
    add_answer_label()
    add_para("Kerangka arsitektur pertahanan berlapis dirancang secara terpusat mengelilingi aset treasury sebagaimana diilustrasikan pada Gambar 3.", space_after=1.5)
    add_figure_custom(
        fig_id="3",
        title="Pengamanan berlapis aset treasury",
        filename="gambar3-pengamanan.png",
        width_cm=13.5,
        explanation="Gambar 3 mengilustrasikan strategi pertahanan berlapis konsentris yang membentengi aset treasury pada inti terdalam. Dari luar ke dalam, lapisan pertama adalah Manusia (pelatihan anti-phishing berkala, verifikasi domain secara mandiri, dan kewajiban bookmark dApp resmi). Lapisan kedua adalah Proses (pemisahan wewenang inisiator dan penyelia, persetujuan ganda dua orang untuk transaksi besar, SOP respons insiden darurat, dan rekonsiliasi kas harian). Lapisan ketiga adalah Wallet (migrasi ke multisignature minimal 3-dari-5 atau MPC, isolasi kunci fisik via hardware wallet berfitur clear signing, eliminasi browser wallet, serta pemisahan hot wallet dan cold storage). Lapisan keempat adalah Kontrol Transaksi (allowlist alamat mitra resmi, pembatasan plafon pengeluaran harian, time-lock 24 sampai 48 jam, simulasi pra-tanda tangan, serta sistem monitoring dan peringatan anomali real-time)."
    )

    # 7. Page 7: Soal 2.4 + Kasus 3 + Soal 3.1 + Tabel 3
    doc.add_page_break()
    add_question("2.4 Tentukan tindakan pada 24 jam pertama dengan tetap menjaga integritas bukti digital. [3 poin | CPMK 4 | C5]")
    add_answer_label(space_before=1.0, space_after=0.5)
    add_para("Tindakan sistematis pada 24 jam pertama dengan memprioritaskan penjagaan integritas bukti digital dirancang dalam empat fase waktu:", space_before=0.2, space_after=0.5, line_spacing=1.04)
    add_item("1. Jam 0 sampai 2 (Isolasi Non-Destruktif dan Preservasi Bukti Volatil): ", 
             "Putuskan perangkat kerja staf dari jaringan fisik dan nirkabel seketika tanpa mematikan daya guna menjaga memori RAM. Lakukan akuisisi memory dump untuk mengamankan session token dan proses injeksi skrip, dilanjutkan pembuatan citra bit-stream disk image terverifikasi hash SHA-256.", space_before=0.1, space_after=0.3, line_spacing=1.03)
    add_item("2. Jam 2 sampai 6 (Containment dan Penyelamatan Cadangan Aset): ", 
             "Lakukan audit status on-chain dari perangkat bersih yang terisolasi. Segera cabut (revoke) seluruh izin allowance token yang terkompromi melalui smart contract darurat, lalu amankan sisa saldo kas ke cold storage atau vault multisignature baru yang aman.", space_before=0.1, space_after=0.3, line_spacing=1.03)
    add_item("3. Jam 6 sampai 12 (Tracing On-Chain dan Koordinasi Eksternal): ", 
             "Petakan pergerakan dana peretas di blockchain dan identifikasi alamat perantara. Kirimkan permohonan pembekuan aset darurat (emergency freeze request) yang memuat bukti transaction hash kepada entitas exchange terpusat (CEX) yang terdeteksi menerima aliran dana.", space_before=0.1, space_after=0.3, line_spacing=1.03)
    add_item("4. Jam 12 sampai 24 (Konsolidasi Forensik dan Pelaporan Hukum): ", 
             "Amankan log proxy, log gateway, dan catatan DNS server internal. Susun laporan kronologis insiden awal bagi manajemen dan unit kepolisian siber, serta terbitkan pernyataan publik yang terukur tanpa membocorkan rincian teknis yang dapat dieksploitasi pihak lain.", space_before=0.1, space_after=0.3, line_spacing=1.03)

    add_case_title("Kasus 3 Audit Smart Contract Vault")
    add_para("Sebuah vault menerima setoran token dan memungkinkan pengguna menarik saldo. Pengembang menuliskan alur penarikan secara sederhana: kontrak memeriksa saldo, mengirim token atau aset kepada pemanggil melalui external call, lalu mengurangi saldo pengguna. Kontrak juga menggunakan oracle harga tunggal dan fungsi admin untuk mengganti alamat oracle tanpa time-lock. Deployment direncanakan langsung ke mainnet tanpa pengujian invariant.", space_before=0.2, space_after=1.0, line_spacing=1.04)

    add_question("3.1 Identifikasi sekurang-kurangnya tiga kerentanan atau kelemahan desain beserta dampaknya. [4 poin | CPMK 3 dan CPMK 4 | C4]")
    add_answer_label(space_before=1.0, space_after=0.5)
    add_para("Berdasarkan evaluasi terhadap kode smart contract vault, diidentifikasi empat kerentanan desain kritis beserta dampaknya yang dirangkum pada Tabel 3.", space_before=0.2, space_after=0.6, line_spacing=1.04)

    t3_headers = ["Kerentanan Desain", "Akar Penyebab Teknis", "Potensi Dampak Kerugian"]
    t3_data = [
        ("Kerentanan Reentrancy pada Alur Penarikan", 
         "Panggilan eksternal (external call) mendahului pembaruan saldo internal pengguna (balances[msg.sender]).", 
         "Kritis; penyerang dapat mengeksekusi penarikan rekursif via fallback function hingga cadangan kas terkuras."),
        ("Ketergantungan Oracle Harga Tunggal", 
         "Kontrak hanya mengandalkan satu sumber oracle harga spot tanpa redundansi atau filter perata harga.", 
         "Tinggi; rentan manipulasi kilat melalui flash loan dalam satu blok transaksi, merusak kalkulasi nilai penarikan."),
        ("Ketiadaan Time-Lock pada Kontrol Admin", 
         "Fungsi pergantian alamat oracle dapat dieksekusi secara instan oleh akun pengendali tanpa jeda tunda.", 
         "Tinggi; jika private key admin bocor, penyerang dapat mengganti oracle ke kontrak jahat dan merampas aset pengguna."),
        ("Ketiadaan Circuit Breaker dan Uji Invariant", 
         "Rencana deployment langsung ke mainnet tanpa fungsi pause darurat dan tanpa pengujian matematis invariant.", 
         "Sedang-Tinggi; pengelola tidak memiliki mekanisme intervensi saat insiden berlangsung, menjamin kerugian permanen.")
    ]
    t3_widths = [Cm(4.5), Cm(5.6), Cm(5.8)]
    add_table_custom("3", "Matriks identifikasi kerentanan smart contract vault", t3_headers, t3_data, t3_widths, font_size=Pt(8.2), cell_padding_y=16)

    # 8. Page 8: Soal 3.2 + Gambar 4 + Kontrol 1-5
    doc.add_page_break()
    add_question("3.2 Usulkan perbaikan urutan logika penarikan dan kontrol akses admin. Jelaskan alasan setiap kontrol. [5 poin | CPMK 3 | C6]")
    add_answer_label()
    add_para("Perbandingan komparatif alur penarikan rentan lawan aman beserta arsitektur kontrol akses admin ditampilkan pada Gambar 4.", space_after=1.0)
    add_figure_custom(
        fig_id="4",
        title="Perbandingan alur penarikan rentan lawan aman dan kontrol administratif",
        filename="gambar4-alur-penarikan.png",
        width_cm=9.6,
        explanation="Gambar 4 memperbandingkan alur penarikan rentan lawan aman disertai kontrol administratif. Pada alur rentan, panggilan eksternal mendahului pengurangan saldo internal sehingga memicu celah reentrancy. Alur aman menerapkan pola Checks-Effects-Interactions (validasi saldo, mutasi saldo internal, lalu transfer aset) berbalut modifier nonReentrant guard. Panel bawah mengamankan kontrol admin melalui multisignature, time-lock 24 sampai 48 jam, dan pencatatan event on-chain sebelum pergantian oracle diberlakukan."
    )
    add_para("Rincian argumentasi dan alasan teknis perbaikan kontrol dirumuskan sebagai berikut:", space_before=0.4, space_after=0.4, keep_with_next=True)
    add_item("1. Pola Checks-Effects-Interactions (CEI): ", 
             "Urutan instruksi dibalik: validasi input (require saldo mencukupi), kurangi variabel saldo internal pemanggil pada penyimpanan kontrak, kemudian eksekusi transfer token ke alamat eksternal. Alasan: Mencegah eksploitasi reentrancy karena saldo pengguna telah terpotong sebelum transfer terjadi.", space_before=0.1, space_after=0.4)
    add_item("2. Proteksi Mutex Guard (nonReentrant): ", 
             "Menambahkan modifier pengunci nonReentrant dari pustaka OpenZeppelin sebagai pertahanan lapis kedua. Alasan: Mengunci status fungsi penarikan agar tidak dapat dipanggil kembali selama instruksi eksternal sebelumnya belum rampung sepenuhnya.", space_before=0.1, space_after=0.4)
    add_item("3. Pembungkus Transfer Aman (SafeERC20): ", 
             "Menggunakan fungsi safeTransfer untuk membungkus pengiriman token ERC-20. Alasan: Mengantisipasi token non-standar yang tidak mengembalikan nilai boolean true agar transaksi tidak gagal secara tersembunyi.", space_before=0.1, space_after=0.4)
    add_item("4. Pengendali Antrean Waktu (Time-Lock Controller 24-48 Jam): ", 
             "Setiap instruksi penggantian alamat oracle wajib dimasukkan ke antrean publik dengan jeda tunda 24 sampai 48 jam disertai emisi event on-chain. Alasan: Memberikan jeda waktu bagi para penyetor modal untuk memeriksa perubahan parameter dan menarik aset secara aman.", space_before=0.1, space_after=0.4)
    add_item("5. Redundansi Multi-Oracle Terdesentralisasi: ", 
             "Menggabungkan data oracle harga Chainlink terdesentralisasi dengan oracle TWAP DEX, dilengkapi batas keusangan data (staleness check) dan deviasi harga maksimum. Alasan: Meniadakan titik kegagalan tunggal dan menolak manipulasi harga instan berbasis flash loan.", space_before=0.1, space_after=0.4)

    # 9. Page 9: Soal 3.3 + Tabel 4 + Soal 3.4
    doc.add_page_break()
    add_question("3.3 Rancang strategi pengujian yang memuat unit test, fuzzing atau property-based test, serta invariant utama. [4 poin | CPMK 3 dan CPMK 4 | C6]")
    add_answer_label()
    add_para("Strategi pengujian komprehensif smart contract dan invariant kritis yang diverifikasi dirangkum pada Tabel 4.")

    t4_headers = ["Tingkat / Jenis Pengujian", "Sasaran dan Metode Pengujian", "Invariant / Sifat Kritis yang Diverifikasi"]
    t4_data = [
        ("Unit Testing (Deterministik)", 
         "Pengujian alur normal dan kasus batas (setoran, penarikan saldo nol, penarikan melampaui saldo, otorisasi fungsi admin).", 
         "Pengecekan kondisi saldo tepat, pembalikan transaksi (revert) saat saldo kurang, dan penolakan pemanggil non-admin."),
        ("Simulasi Serangan Reentrancy", 
         "Menyusun kontrak uji tiruan (mock exploit contract) yang mencoba memanggil fungsi withdraw() secara rekursif via fallback.", 
         "Pola CEI dan nonReentrant guard sukses menolak eksekusi rekursif kedua, mempertahankan integritas saldo vault."),
        ("Fuzzing & Property-Based Testing", 
         "Mengeksekusi ratusan ribu kombinasi urutan transaksi dan nominal acak ekstrem menggunakan Foundry atau Echidna.", 
         "Mendeteksi potensi kesalahan pembulatan aritmatika (rounding errors) serta celah underflow dan overflow numerik."),
        ("Formal Invariants Verification", 
         "Membuktikan kebenaran sifat matematis absolut kontrak di seluruh perubahan status transaksi.", 
         "Solvabilitas cadangan: TotalAsetFisik >= TotalKewajiban; Non-negativitas: saldo akun tidak pernah bernilai minus."),
        ("Audit Statis & Uji Coba Testnet", 
         "Pemindaian kerentanan kode otomatis via analisis statis (Slither) dan uji coba operasional terintegrasi di testnet publik.", 
         "Bebas peringatan kelemahan logika; stabilitas interaksi kontrak dengan token standar dan non-standar selama simulasi.")
    ]
    t4_widths = [Cm(4.3), Cm(5.8), Cm(5.8)]
    add_table_custom("4", "Matriks strategi pengujian dan verifikasi invariant", t4_headers, t4_data, t4_widths, font_size=Pt(8.5))

    add_question("3.4 Putuskan apakah deployment harus dilanjutkan atau ditunda dan nyatakan kriteria go atau no-go. [2 poin | CPMK 4 | C5]")
    add_answer_label()
    add_item("Keputusan Evaluasi: ", "TUNDA (NO-GO) secara mutlak terhadap rencana deployment ke mainnet sampai seluruh kerentanan kritis diperbaiki dan diuji tuntas.")
    add_para("Empat Kriteria Go / No-Go Terukur yang Wajib Dipenuhi Sebelum Rilis:", space_before=0.8, space_after=0.8, keep_with_next=True)
    add_item("1. Remediasi Tuntas Kerentanan Kritis: ", 
             "Celah reentrancy, ketergantungan oracle tunggal, dan fungsi admin instan telah diperbaiki sepenuhnya serta memperoleh surat verifikasi bersih dari auditor keamanan eksternal independen.")
    add_item("2. Kelulusan Uji Invariant Fuzzing: ", 
             "Kontrak berhasil melewati pengujian fuzzing minimal 100.000 iterasi transaksi acak tanpa satupun pelanggaran terhadap invariant solvabilitas aset vault.")
    add_item("3. Implementasi Kontrol Multi-Signature dan Time-Lock: ", 
             "Hak akses administratif telah dialihkan ke smart contract multisignature minimal 3-dari-5 dan time-lock controller 24 sampai 48 jam telah aktif terpasang pada jaringan.")
    add_item("4. Validasi Stabilitas Testnet Publik: ", 
             "Kontrak beroperasi tanpa kendala di testnet publik selama minimal dua minggu, dilanjutkan peluncuran bertahap (canary launch) dengan pembatasan plafon setoran (deposit cap) ketat pada fase awal.")

    # 10. Page 10: Kasus 4 + Soal 4.1 + Gambar 5 + Metode
    doc.add_page_break()
    add_case_title("Kasus 4 Investigasi Aliran Dana Lintas Jaringan")
    add_para("Sebuah alamat A menerima aset hasil eksploitasi protokol DeFi. Dana kemudian dipecah ke enam alamat, sebagian ditukar melalui decentralized exchange, lalu dipindahkan melalui bridge ke jaringan lain. Salah satu alamat tujuan mengirim dana ke alamat deposit yang diduga milik exchange terpusat. Tim investigasi memiliki transaction hash, timestamp, alamat kontrak, dan log event, tetapi belum memiliki informasi identitas pemilik alamat.", space_after=2.5)

    add_question("4.1 Jelaskan metode rekonstruksi aliran dana dan artefak on-chain yang harus dikumpulkan. [4 poin | CPMK 4 | C4]")
    add_answer_label()
    add_para("Pemetaan aliran dana dari alamat awal hasil eksploitasi menuju entitas bursa direkonstruksi dalam graf transaksi pada Gambar 5.", space_after=1.5)
    add_figure_custom(
        fig_id="5",
        title="Graf rekonstruksi aliran dana lintas jaringan",
        filename="gambar5-graf-aliran-dana.png",
        width_cm=15.0,
        explanation="Graf pada Gambar 5 merekonstruksi aliran dana peretasan secara terstruktur dari kiri ke kanan. Dimulai dari Alamat A sebagai penampung awal hasil eksploitasi protokol DeFi, dana disebarkan ke enam alamat perantara (Alamat B1 sampai B6) untuk memecah jejak transaksi. Sebagian dana (diilustrasikan melalui Alamat B1 dan B2) dialirkan ke kontrak router decentralized exchange (DEX) guna menukar token hasil curian menjadi aset kripto lain, sementara alamat lainnya mengirimkan dana langsung ke gerbang kontrak bridge jaringan asal. Pada bridge asal, aset dikunci atau dibakar, memicu emisi event log lintas rantai yang menginstruksikan bridge jaringan tujuan menerbitkan aset pengganti kepada Alamat Tujuan. Dari Alamat Tujuan, dana dikirimkan ke Alamat Deposit. Hubungan garis solid menunjukkan transaksi yang terbukti mutlak via transaction hash on-chain, sedangkan garis putus-putus menunjukkan atribusi kepemilikan alamat deposit bursa terpusat yang didasarkan pada analisis heuristik sweeping saldo."
    )
    add_para("Metode Rekonstruksi dan Pengumpulan Artefak On-Chain:", space_before=0.8, space_after=0.8, keep_with_next=True)
    add_item("1. Rekonstruksi Aliran Dana Berbasis Graf: ", 
             "Penyelidikan memanfaatkan pemodelan graf terarah (Directed Acyclic Graph) untuk memetakan alamat sebagai node dan transfer aset sebagai edge. Proses mencakup dekonvolusi pemecahan dana (fan-out layering), penguraian log event pertukaran token (Transfer, Swap, Sync) pada router DEX, serta pencocokan relasi stempel waktu dan nonce peristiwa bridge lintas jaringan.")
    add_item("2. Inventarisasi Artefak On-Chain Kritis: ", 
             "Artefak yang wajib dihimpun mencakup parameter transaksi (transaction hash, nomor blok, stempel waktu presisi UTC, origin), entitas alamat pengirim dan penerima, alamat smart contract token dan gateway bridge, data log event mentah beserta topik terindeks, rekaman internal trace eksekusi panggilan kontrak, resi status transaksi (receipt), serta pemakaian bahan bakar transaksi (gas fee).")

    # 11. Page 11: Soal 4.2 + Tabel 5 + Uraian
    doc.add_page_break()
    add_question("4.2 Nilai kekuatan dan keterbatasan heuristik common-input, clustering waktu, dan hubungan alamat deposit. [4 poin | CPMK 4 | C5]")
    add_answer_label()
    add_para("Evaluasi perbandingan analitis mengenai kekuatan dan keterbatasan ketiga metode heuristik blockchain disajikan pada Tabel 5.")

    t5_headers = ["Metode Heuristik", "Kekuatan Analisis Forensik", "Keterbatasan Teknis"]
    t5_data = [
        ("Common-Input Ownership\n(Catatan: Berasal dari Model UTXO)", 
         "Sangat andal pada arsitektur UTXO (Bitcoin); penggabungan beberapa input dalam satu transaksi membuktikan kepemilikan oleh satu entitas yang sama.", 
         "Tidak berlaku langsung pada model berbasis akun (Ethereum/EVM) karena setiap transaksi hanya memiliki satu pengirim (msg.sender). Analisis EVM beralih ke sumber gas fee awal bersama atau penandatangan multisignature."),
        ("Clustering Waktu\n(Temporal Analysis)", 
         "Efektif mendeteksi otomatisasi bot, seperti distribusi saldo ke enam alamat dalam blok yang sama atau selisih detik yang sangat teratur.", 
         "Rentan kesalahan positif akibat kongesti jaringan global; mudah dikaburkan penyerang dengan menyetel jeda waktu acak (randomized delay)."),
        ("Hubungan Alamat Deposit\n(Deposit Address Clustering)", 
         "Sangat kuat mengaitkan alamat on-chain dengan entitas bursa resmi via pola penyapuan saldo (sweeping) ke hot wallet utama exchange.", 
         "Hanya mengidentifikasi platform penyedia layanan bursa, bukan identitas manusia pemilik akun, karena pelaku kerap memakai akun sewaan (mule account).")
    ]
    t5_widths = [Cm(4.5), Cm(5.6), Cm(5.8)]
    add_table_custom("5", "Evaluasi kekuatan dan keterbatasan heuristik analisis blockchain", t5_headers, t5_data, t5_widths, font_size=Pt(9.0))

    add_para("Uraian Analisis Heuristik:", space_before=0.8, space_after=0.8, keep_with_next=True)
    add_para("Penerapan ketiga heuristik tersebut memerlukan pendekatan kontekstual sesuai model arsitektur buku besar. Heuristik common-input ownership memberikan dasar pembuktian kepemilikan dompet tunggal yang sangat kuat pada ekosistem UTXO seperti Bitcoin melalui analisis masukan bersama, namun pada ekosistem EVM analis harus mengalihkan fokus pada transaksi pembiayaan gas fee awal atau kesamaan alamat penandatangan kontrak multi-pemilik. Sementara itu, analisis temporal clustering mampu mengungkap keterlibatan skrip otomatisasi bot penyerang dalam mengeksekusi pemecahan dana secara serentak, meskipun analis harus mewaspadai upaya penyamaran berupa penyisipan jeda waktu acak. Pada tahap akhir, deposit address clustering menjadi kunci krusial untuk menghubungkan transaksi pseudonim blockchain dengan entitas penyedia layanan aset virtual resmi di dunia nyata melalui pelacakan sweeping saldo.")

    # 12. Page 12: Soal 4.3 + Gambar 6
    doc.add_page_break()
    add_question("4.3 Susun chain of custody untuk menjaga bukti hasil ekstraksi blockchain dan data pendukung off-chain. [4 poin | CPMK 4 | C6]")
    add_answer_label()
    add_para("Bagan alir prosedur preservasi bukti digital forensik dirumuskan dalam rantai penjagaan (chain of custody) pada Gambar 6.", space_after=1.5)
    add_figure_custom(
        fig_id="6",
        title="Alur chain of custody preservasi bukti digital blockchain",
        filename="gambar6-chain-of-custody.png",
        width_cm=10.0,
        explanation="Gambar 6 menggambarkan bagan alir terstruktur chain of custody dalam delapan tahapan berurutan untuk menjamin integritas bukti forensik digital di mata hukum. Dimulai dari identifikasi sumber bukti digital (node RPC, basis data log, memori sistem), dilanjutkan pengumpulan bukti dengan dokumentasi perkakas, versi klien, stempel waktu, dan parameter kueri. Tahap ketiga adalah perhitungan nilai hash kriptografis SHA-256 seketika untuk setiap berkas mentah. Tahap keempat memisahkan salinan master berstatus read-only dari salinan kerja (working copy). Tahap kelima mengamankan penyimpanan bukti pada media terenkripsi di dalam brankas fisik dengan pembatasan hak akses ketat. Tahap keenam mencatat setiap riwayat peminjaman pada log serah terima bertanda tangan (siapa, kapan, dan tujuan peminjaman). Tahap ketujuh memastikan seluruh analisis forensik hanya dijalankan pada salinan kerja. Tahap kedelapan melakukan verifikasi ulang nilai hash SHA-256 sebelum bukti diajukan ke laporan investigasi atau persidangan; apabila hash tidak cocok, sistem memberi peringatan untuk menandai dan menelusuri anomali perubahan data."
    )

    # 13. Page 13: Soal 4.4 + Tabel 6 + Kesimpulan
    doc.add_page_break()
    add_question("4.4 Tuliskan kesimpulan investigatif yang membedakan atribusi alamat, atribusi layanan, dan atribusi individu. [3 poin | CPMK 4 | C5]")
    add_answer_label()
    add_para("Klasifikasi tingkatan atribusi investigasi beserta dasar pembuktian dan status kesimpulannya dirangkum pada Tabel 6.")

    t6_headers = ["Tingkat Atribusi", "Dasar Bukti Pendukung", "Tingkat Keyakinan", "Status Kesimpulan"]
    t6_data = [
        ("Atribusi Alamat\n(Address Attribution)", 
         "Catatan transaction hash on-chain, rekaman blok, log event token transfer, dan mutasi saldo.", 
         "Pasti (Deterministik)", 
         "Terbukti secara matematis dan permanen pada ledger publik bahwa alamat penampung menerima dana eksploitasi."),
        ("Atribusi Layanan\n(Service Attribution)", 
         "Interaksi dengan smart contract DEX, gateway bridge, serta transaksi sweeping saldo menuju klaster hot wallet bursa.", 
         "Tinggi (Analisis Perilaku)", 
         "Terbukti kuat bahwa alamat tujuan akhir berfungsi sebagai alamat deposit khusus milik entitas exchange terpusat."),
        ("Atribusi Individu\n(Individual Attribution)", 
         "Data pendaftaran akun bursa off-chain, rekaman identitas KYC, log alamat IP login, dan rekening penarikan fiat.", 
         "Belum Terbukti (Perlu Bukti Hukum)", 
         "Masih berupa hipotesis investigatif; identitas pelaku fisik mutlak memerlukan perintah pengadilan (subpoena) kepada exchange.")
    ]
    t6_widths = [Cm(3.8), Cm(4.6), Cm(3.5), Cm(4.0)]
    add_table_custom("6", "Tingkatan atribusi investigasi on-chain dan off-chain", t6_headers, t6_data, t6_widths, font_size=Pt(9.0))

    add_para("Uraian Kesimpulan Investigatif:", space_before=0.8, space_after=0.8, keep_with_next=True)
    add_para("Investigasi membuktikan secara pasti pada tingkat atribusi alamat bahwa dana hasil eksploitasi mengalir dari Alamat A melalui enam alamat perantara, sebagian dikonversi di DEX, dan diseberangkan melalui bridge menuju alamat tujuan. Pada tingkat atribusi layanan, jejak transaksi membuktikan dengan tingkat keyakinan tinggi bahwa alamat penerima akhir terafiliasi dengan entitas exchange terpusat tertentu berdasarkan karakteristik penyapuan saldo ke klaster hot wallet bursa. Namun, pada tingkat atribusi individu, identitas manusia di balik pengendali alamat belum dapat disimpulkan karena transaksi blockchain bersifat pseudonim. Penetapan tersangka secara hukum memerlukan langkah investigasi off-chain melalui penerbitan surat perintah pengadilan (subpoena) kepada bursa terkait guna membuka catatan identitas KYC, log alamat IP akses, dan rekening penarikan fiat yang terhubung.")

    doc.save(TEST_DOCX)
    print(f"Test docx saved to {TEST_DOCX}")

if __name__ == '__main__':
    build_test()
