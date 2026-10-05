#!/usr/bin/env python3
"""
Generator for UTS Blockchain Bagian A answers document.
Student: Fajar Geran Arifin (NPM: 237006079, Kelas: C)
Destination: UTS_Blockchain_Bagian_A_237006079_Fajar_Geran_Arifin_JAWABAN.docx
"""

import os
import re
import docx
from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

SRC_PATH = "/home/fajar-geran-arifin/Documents/kuliah/block chain/UTS bagian A/UTS_Blockchain_Bagian_A_237006079_Fajar_Geran_Arifin.docx"
DST_PATH = "/home/fajar-geran-arifin/Documents/kuliah/block chain/UTS bagian A/UTS_Blockchain_Bagian_A_237006079_Fajar_Geran_Arifin_JAWABAN.docx"
IMG_PATH = "/home/fajar-geran-arifin/Documents/kuliah/block chain/UTS bagian A/arsitektur-blockchain.png"

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
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

def set_cell_shading(cell, color_hex="F1F5F9"):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    tcPr.append(shd)

def set_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="334155"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="334155"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>
            <w:insideV w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def build_document():
    doc_new = Document()
    s = doc_new.sections[0]
    s.page_width = Cm(21.0)
    s.page_height = Cm(29.7)
    s.top_margin = Cm(2.54)
    s.bottom_margin = Cm(2.54)
    s.left_margin = Cm(2.54)
    s.right_margin = Cm(2.54)

    st_norm = doc_new.styles['Normal']
    st_norm.font.name = 'Times New Roman'
    st_norm.font.size = Pt(12)
    st_norm.font.color.rgb = RGBColor(0, 0, 0)

    def add_para(text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, line_spacing=1.12, keep_with_next=False):
        p = doc_new.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        p.paragraph_format.keep_with_next = keep_with_next
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        return p

    def add_item(title, body, bold_title=True, space_before=2, space_after=3, line_spacing=1.12, keep_with_next=False):
        p = doc_new.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        p.paragraph_format.keep_with_next = keep_with_next
        if title:
            run_t = p.add_run(title)
            run_t.bold = bold_title
            run_t.font.name = 'Times New Roman'
            run_t.font.size = Pt(12)
        if body:
            run_b = p.add_run(body)
            run_b.font.name = 'Times New Roman'
            run_b.font.size = Pt(12)
        return p

    def add_bullet(title, body, bold_title=True, indent_cm=0.5, space_before=1, space_after=2, line_spacing=1.12):
        p = doc_new.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.left_indent = Cm(indent_cm)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        run_bullet = p.add_run("• ")
        run_bullet.bold = True
        run_bullet.font.name = 'Times New Roman'
        run_bullet.font.size = Pt(12)
        if title:
            run_t = p.add_run(title)
            run_t.bold = bold_title
            run_t.font.name = 'Times New Roman'
            run_t.font.size = Pt(12)
        if body:
            run_b = p.add_run(body)
            run_b.font.name = 'Times New Roman'
            run_b.font.size = Pt(12)
        return p

    def add_case_title(text):
        p = doc_new.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        return p

    def add_question(text):
        p = doc_new.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        return p

    # --- 1. HEADER SECTION ---
    header_lines = [
        "Nama\t: Fajar Geran Arifin",
        "NPM\t: 237006079",
        "Kelas\t: C",
        "Mata Kuliah\t: Blockchain",
        "Dosen Pengampu\t: Dr. Ir. Nur Widiyasono, M.Kom."
    ]
    for line in header_lines:
        p = doc_new.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run(line)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)

    p_title = doc_new.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(2)
    p_title.paragraph_format.keep_with_next = True
    r_t = p_title.add_run("Bagian A Ujian Berbasis Kasus")
    r_t.bold = True
    r_t.font.name = 'Times New Roman'
    r_t.font.size = Pt(12)

    p_sub = doc_new.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(8)
    r_s = p_sub.add_run("Bobot 60 poin. Bacalah konteks setiap kasus, kemudian jawab seluruh pertanyaan secara argumentatif.")
    r_s.font.name = 'Times New Roman'
    r_s.font.size = Pt(12)

    # --- 2. KASUS 1 ---
    add_case_title("Kasus 1 Sistem Ketertelusuran Produk Pangan")
    add_para("Sebuah konsorsium terdiri atas koperasi petani, pabrik pengolahan, perusahaan logistik, laboratorium mutu, dan jaringan ritel. Saat ini data lot produksi tersimpan pada basis data masing-masing organisasi. Ketika terjadi penarikan produk, pencocokan nomor lot memerlukan dua hingga tiga hari. Konsorsium ingin memperoleh jejak audit bersama, tetapi harga pemasok dan identitas petani tertentu tidak boleh terlihat oleh semua pihak. Volume transaksi diperkirakan 25 transaksi per detik dan peserta jaringan telah diketahui identitasnya.", space_after=6)

    # 1.1 (Target: 150 - 220 kata | 4 poin)
    add_question("1.1 Identifikasi tiga kebutuhan bisnis dan dua kendala teknis yang menentukan desain sistem. [4 poin | CPMK 1 dan CPMK 2 | C4]")
    add_para("Berdasarkan konteks konsorsium rantai pasok pangan, berikut adalah identifikasi tiga kebutuhan bisnis dan dua kendala teknis penentu desain sistem:")
    add_para("A. Tiga Kebutuhan Bisnis:", bold=True, space_before=2, space_after=2, keep_with_next=True)
    add_item("1. Jejak Audit Bersama yang Abadi (Shared Immutable Audit Trail): ", 
             "Konsorsium membutuhkan satu sumber kebenaran data tunggal yang transparan dan tahan manipulasi untuk mendokumentasikan silsilah bahan baku dari perkebunan hingga gerai ritel, mengeliminasi sengketa data dan ketergantungan rekonsiliasi manual antar-organisasi.")
    add_item("2. Akselerasi Penarikan Produk (Rapid Product Recall): ", 
             "Memangkas durasi pencocokan nomor lot terdampak dari 2–3 hari menjadi hitungan menit atau jam guna memitigasi risiko keamanan konsumen dan menekan kerugian finansial akibat penarikan massal yang salah sasaran.")
    add_item("3. Perlindungan Kerahasiaan Komersial Selektif (Selective Confidentiality): ", 
             "Melindungi data bisnis rahasia, seperti harga pembelian bahan baku antar-pemasok dan identitas privat (PII) petani tertentu, agar tidak terlihat oleh pihak non-rekanan, namun integritas dan keabsahan transaksinya tetap dapat diverifikasi.")
    add_para("B. Dua Kendala Teknis:", bold=True, space_before=2, space_after=2, keep_with_next=True)
    add_item("1. Throughput Transaksi dan Finalitas Cepat: ", 
             "Sistem harus mampu memproses throughput operasional sekitar 25 transaksi per detik (TPS) dengan latensi rendah dan finalitas deterministik tanpa risiko percabangan (zero fork), guna menjamin kelancaran serah terima operasional logistik.")
    add_item("2. Penyimpanan Hibrida dan Integrasi Sistem Warisan: ", 
             "Berkas biner berukuran besar (foto komoditas, sertifikat inspeksi, PDF laporan laboratorium) tidak layak disimpan langsung di on-chain ledger karena beban komputasi node, sehingga memerlukan integrasi penyimpanan off-chain terenkripsi serta penyelarasan dengan basis data internal (ERP) eksisting.")

    # 1.2 (Target: 200 - 280 kata | 5 poin)
    add_question("1.2 Pilih jenis blockchain dan mekanisme konsensus yang paling sesuai. Bandingkan pilihan Anda dengan sekurang-kurangnya satu alternatif. [5 poin | CPMK 2 | C5]")
    add_para("A. Pemilihan Jenis Blockchain dan Mekanisme Konsensus:", bold=True, space_before=2, space_after=2, keep_with_next=True)
    add_para("Jenis blockchain yang paling tepat adalah Permissioned / Consortium Blockchain berbasis Hyperledger Fabric, dengan mekanisme konsensus Ordering Service berbasis Byzantine Fault Tolerant, yaitu SmartBFT (tersedia pada Fabric v3).")
    add_para("B. Argumentasi dan Analisis Trade-off:", bold=True, space_before=2, space_after=2, keep_with_next=True)
    add_item("1. Kesesuaian Tata Kelola: ", 
             "Seluruh anggota konsorsium (koperasi, pabrik, logistik, lab, ritel) telah diketahui identitas hukumnya. Fabric mengautentikasi setiap node melalui Certificate Authority (CA) dan Membership Service Provider (MSP), meniadakan mekanisme penambangan anonim publik yang boros energi dan biaya transaksi (gas fee) fluktuatif.")
    add_item("2. Skalabilitas Performa: ", 
             "Beban 25 TPS tergolong sangat wajar dan berada jauh di bawah kapasitas puncak Fabric yang mampu melayani ratusan hingga ribuan TPS dengan finalitas deterministik sub-detik.")
    add_item("3. Trade-off Konsensus (SmartBFT vs. Raft): ", 
             "Konsensus Raft (Crash Fault Tolerant/CFT) memang lebih sederhana dan berkinerja tinggi, namun hanya tahan terhadap node yang padam (crash), bukan node yang bertindak curang atau mengirimkan data bertentangan (Byzantine). Karena anggota konsorsium adalah entitas bisnis independen dengan potensi persaingan komersial, SmartBFT jauh lebih unggul karena mampu mentoleransi hingga f node jahat dari total 3f + 1 node pemesanan, meskipun memerlukan sedikit overhead komunikasi pesan.")
    add_para("C. Perbandingan dengan Alternatif:", bold=True, space_before=2, space_after=2, keep_with_next=True)
    add_item("1. Ethereum PoS (Publik): ", 
             "Kurang cocok karena data transaksi terbuka untuk umum secara inheren (melanggar kerahasiaan harga dan identitas petani), biaya gas fluktuatif, serta finalitas blok membutuhkan waktu 12–15 menit.")
    add_item("2. Quorum / Hyperledger Besu (IBFT/QBFT): ", 
             "Menerapkan model eksekusi order-execute di mana seluruh node memvalidasi transaksi secara seragam di saluran bersama, berbeda dengan arsitektur execute-order-validate milik Fabric yang mendukung isolasi privasi data bilateral via Private Data Collections (PDC).")

    # 1.3 (Target: 150 - 220 kata | 4 poin) - Explicit Page Break to keep Question 1.3, Diagram, Caption, and Explanation unified on Page 3
    doc_new.add_page_break()
    add_question("1.3 Gambarkan arsitektur logis yang menunjukkan aktor, node, data on-chain, data off-chain, serta mekanisme kontrol akses. [4 poin | CPMK 2 | C6]")
    
    # Diagram image
    p_img = doc_new.add_paragraph()
    p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img.paragraph_format.space_before = Pt(4)
    p_img.paragraph_format.space_after = Pt(2)
    p_img.paragraph_format.keep_with_next = True
    run_img = p_img.add_run()
    run_img.add_picture(IMG_PATH, width=Cm(16.0))

    # Caption
    p_cap = doc_new.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(6)
    p_cap.paragraph_format.keep_with_next = True
    run_cap = p_cap.add_run("Gambar 1. Arsitektur logis sistem ketertelusuran pangan")
    run_cap.italic = True
    run_cap.font.name = 'Times New Roman'
    run_cap.font.size = Pt(11)

    add_item("Penjelasan Arsitektur Logis Sistem: ",
             "Arsitektur pada Gambar 1 mengintegrasikan lima aktor konsorsium (Koperasi, Pabrik Pengolah, Perusahaan Logistik, Laboratorium, dan Jaringan Ritel) yang berinteraksi melalui Aplikasi Organisasi untuk submit transaksi dan monitoring lot, serta Aplikasi Keterlacakan untuk akses publik konsumen via pemindaian kode QR. Pada lapisan jaringan Hyperledger Fabric, setiap organisasi mengoperasikan Peer Node yang menyimpan World State (CouchDB) dan mengeksekusi logika bisnis smart contract (Chaincode). Konsensus pengurutan transaksi dikelola secara terdesentralisasi oleh klaster Ordering Service berbasis SmartBFT (Node 1–4) yang mendistribusikan blok ke bar Validasi & Pencatatan Ledger guna verifikasi kebijakan endorsement (VSCC) dan validasi konflik versi (MVCC). Sistem menerapkan penyimpanan hibrida: data transaksi bernilai tinggi (nomor lot universal, relasi silsilah antar-lot, jejak peristiwa serah terima, status mutu, status penarikan/recall, serta hash dokumen pendukung) disimpan secara permanen pada on-chain ledger, sedangkan dokumen berukuran besar (PDF laporan uji lab, faktur, foto komoditas, dan rekaman sensor IoT) disimpan pada penyimpanan off-chain terenkripsi (IPFS/Cloud). Data komersial sensitif seperti harga pemasok dilindungi secara bilateral menggunakan Private Data Collections (PDC) via protokol Fabric Gossip. Seluruh interaksi diamankan oleh Certificate Authority (CA) dan Membership Service Provider (MSP) berbasis PKI/X.509 dan RBAC, dengan penegakan aturan di mana penerbitan hasil uji mutu mutlak menjadi hak MSP Laboratorium dan serah terima logistik mewajibkan endorsement ganda dari pihak pengirim dan penerima.",
             space_before=4, space_after=4)

    # 1.4 (Target: 60 - 100 kata | 2 poin)
    add_question("1.4 Tetapkan dua indikator keberhasilan pilot project yang dapat diukur. [2 poin | CPMK 1 | C4]")
    add_para("Dua indikator keberhasilan pilot project yang terukur ditetapkan sebagai berikut:")
    add_item("1. Durasi Pelacakan Lot Terdampak (Recall Traceability Time): ", 
             "Waktu penelusuran silsilah lot lengkap dari hulu ke hilir terpangkas dari 2–3 hari menjadi di bawah 15 menit, diuji melalui simulasi penarikan produk (mock recall) berkala hingga seluruh rantai pasok terdampak teridentifikasi.")
    add_item("2. Tingkat Kelengkapan Pencatatan Data Lot (Data Completeness Rate): ", 
             "Minimal 95% dari total lot komoditas selama fase pilot tercatat valid secara end-to-end pada ledger on-chain, diverifikasi melalui audit rekonsiliasi data mingguan antara basis data ERP internal dengan transaksi blockchain.")

    # --- 3. KASUS 2 ---
    add_case_title("Kasus 2 Insiden Wallet Organisasi")
    add_para("Wallet treasury sebuah organisasi blockchain kehilangan aset setelah seorang staf menyetujui transaksi yang tampil sebagai pembaruan kontrak. Log menunjukkan login dari perangkat staf yang sah, tetapi domain antarmuka berbeda satu karakter dari domain resmi. Private key disimpan pada browser wallet; tidak ada multisignature, allowlist alamat, maupun prosedur respons insiden. Organisasi meminta analisis akar masalah dan rencana pemulihan.", space_after=6)

    # 2.1 (Target: 150 - 220 kata | 4 poin)
    add_question("2.1 Susun urutan kejadian yang paling mungkin dan bedakan fakta, hipotesis, serta bukti yang masih perlu dikumpulkan. [4 poin | CPMK 4 | C4]")
    add_para("Analisis insiden memisahkan fakta empiris, hipotesis investigatif, dan bukti forensik yang perlu dikumpulkan:")
    
    # Table 2.1 (5 focused rows)
    t = doc_new.add_table(rows=6, cols=3)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t)
    
    trPr0 = t.rows[0]._tr.get_or_add_trPr()
    trPr0.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    for row in t.rows:
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))

    headers = ["Fakta (Berdasarkan Teks Kasus)", "Hipotesis Investigatif", "Bukti yang Perlu Dikumpulkan"]
    col_widths = [Cm(5.1), Cm(5.1), Cm(5.6)]

    hdr_cells = t.rows[0].cells
    for c_idx, title in enumerate(headers):
        hdr_cells[c_idx].width = col_widths[c_idx]
        set_cell_margins(hdr_cells[c_idx], top=120, bottom=120, left=140, right=140)
        set_cell_shading(hdr_cells[c_idx], "F1F5F9")
        p = hdr_cells[c_idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(title)
        run.bold = True
        run.font.name = 'Times New Roman'
        run.font.size = Pt(10.5)

    table_data = [
        ("Login berasal dari perangkat staf sah; domain berbeda 1 karakter.", 
         "Staf terkena rekayasa sosial phishing typosquatting akibat kelalaian pengetikan URL.", 
         "Riwayat penjelajahan browser, DNS cache lokal, dan log proxy perangkat."),
        ("Transaksi tampil sebagai 'pembaruan kontrak' pada dApp.", 
         "Antarmuka palsu memanipulasi tampilan guna melakukan blind signing.", 
         "Source code web palsu, script injeksi web3, dan ABI transaksi."),
        ("Private key disimpan pada browser wallet tanpa multisig.", 
         "Kunci terekspos langsung tanpa kontrol otorisasi ganda atau segregasi wewenang.", 
         "Log aktivitas wallet extension, file vault terenkripsi, dan konfigurasi dApp."),
        ("Staf menyetujui transaksi menggunakan private key treasury.", 
         "Muatan transaksi berisi transfer dana langsung atau izin token tak terbatas (infinite approval).", 
         "Transaction hash on-chain, data payload heksadesimal, dan status mutasi saldo."),
        ("Wallet treasury kehilangan aset; ketiadaan allowlist dan SOP.", 
         "Ketiadaan batas transaksi memungkinkan pengurasan saldo dalam sekali eksekusi.", 
         "Alamat penampung peretas di blockchain dan log transaksi kas internal.")
    ]

    for row_idx, data in enumerate(table_data):
        row_cells = t.rows[row_idx + 1].cells
        for col_idx, text in enumerate(data):
            row_cells[col_idx].width = col_widths[col_idx]
            set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=120, right=120)
            if row_idx % 2 == 1:
                set_cell_shading(row_cells[col_idx], "F8FAFC")
            p = row_cells[col_idx].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            run = p.add_run(text)
            run.font.name = 'Times New Roman'
            run.font.size = Pt(10)

    p_space = doc_new.add_paragraph()
    p_space.paragraph_format.space_before = Pt(4)
    p_space.paragraph_format.space_after = Pt(2)

    add_item("Urutan Kejadian yang Paling Mungkin: ", 
             "(1) Penyerang membuat web typosquatting; (2) staf mengakses situs dari perangkat kerja sah; (3) antarmuka palsu menyamarkan manipulasi izin aset sebagai 'Pembaruan Kontrak'; (4) staf menandatangani transaksi via browser wallet; dan (5) transaksi dieksekusi di blockchain hingga aset terkuras tanpa hambatan multisig.",
             space_before=2, space_after=4)

    # 2.2 (Target: 100 - 150 kata | 3 poin)
    add_question("2.2 Jelaskan bagaimana tanda tangan digital tetap valid meskipun transaksi terjadi akibat rekayasa sosial. [3 poin | CPMK 3 | C4]")
    add_para("Tanda tangan digital (berbasis ECDSA secp256k1) tetap valid secara teknis karena kriptografi blockchain hanya memverifikasi autentisitas matematis dan integritas data, bukan menguji intensi atau konteks kebenaran manusia (semantic blindness).")
    add_para("Secara protokol, tanda tangan membuktikan dua hal pasti: (1) transaksi didekripsi menggunakan public key yang berpasangan sah dengan private key penandatangan (autentikasi pengirim), dan (2) muatan byte data transaksi tidak berubah sejak ditandatangani (integritas pesan). Ketika staf terkena rekayasa sosial, staf secara sadar mengeksekusi penandatanganan menggunakan private key sah di browser wallet.")
    add_para("Pada insiden ini terjadi fenomena blind signing: antarmuka dApp menampilkan narasi palsu 'Pembaruan Kontrak', padahal payload data mentah adalah instruksi pemindahan aset atau approval tak terbatas. Karena penandatanganan dilakukan dengan private key yang sah, node validator blockchain wajib memproses transaksi tersebut sebagai instruksi legal, terlepas dari fakta bahwa persetujuan diperoleh melalui penipuan.")

    # 2.3 (Target: 200 - 280 kata | 5 poin)
    add_question("2.3 Rancang pengamanan berlapis yang mencakup manusia, proses, wallet, dan kontrol transaksi. [5 poin | CPMK 3 dan CPMK 4 | C6]")
    add_para("Rancangan pengamanan berlapis (Defense-in-Depth) mencakup empat pilar pertahanan:")
    
    add_para("1. Lapisan Manusia (People):", bold=True, space_before=3, space_after=1, keep_with_next=True)
    add_bullet("Pelatihan Anti-Phishing: ", "Edukasi periodik mengenai ancaman typosquatting dan teknik manipulasi antarmuka web3.")
    add_bullet("Akses Berbasis Bookmark: ", "Mewajibkan operator mengakses antarmuka dApp hanya melalui bookmarked URL resmi terverifikasi dan melarang membuka tautan treasury dari email atau pesan instan.")
    add_bullet("Verifikasi Parameter Mentah: ", "Mewajibkan verifikasi mandiri terhadap alamat tujuan dan data transaksi sebelum penandatanganan.")

    add_para("2. Lapisan Proses (Process):", bold=True, space_before=3, space_after=1, keep_with_next=True)
    add_bullet("Pemisahan Wewenang (Segregation of Duties): ", "Menerapkan prinsip four-eyes/dual-control di mana inisiasi transaksi dan persetujuan akhir harus dieksekusi oleh individu berbeda.")
    add_bullet("SOP Respons Insiden: ", "Prosedur tanggap darurat yang merinci rantai komando, matriks eskalasi, dan isolasi aset saat anomali terdeteksi.")
    add_bullet("Rekonsiliasi Kas Berkala: ", "Pencocokan harian antara pembukuan kas internal dan saldo on-chain.")

    add_para("3. Lapisan Wallet (Infrastructure):", bold=True, space_before=3, space_after=1, keep_with_next=True)
    add_bullet("Eliminasi Browser Hot Wallet: ", "Menghapus penyimpanan private key dari browser extension yang rentan terhadap malware pencuri kredensial (infostealer).")
    add_bullet("Implementasi Multi-Signature / MPC: ", "Memigrasikan treasury ke smart contract multisig (misal Safe / Gnosis Safe) atau MPC dengan ambang batas minimal 3-of-5 dari perangkat terpisah.")
    add_bullet("Isolasi Hardware Wallet: ", "Mewajibkan penggunaan hardware wallet (Ledger/Trezor) dengan layar verifikasi fisik (clear signing), serta memisahkan hot wallet operasional dan cold storage cadangan.")

    add_para("4. Lapisan Kontrol Transaksi (Transaction Controls):", bold=True, space_before=3, space_after=1, keep_with_next=True)
    add_bullet("Allowlist Alamat: ", "Membatasi transfer dana hanya ke alamat kontrak atau mitra yang telah terdaftar dan terverifikasi.")
    add_bullet("Spending Limits & Time-Lock: ", "Menerapkan batas plafon nominal harian serta jeda tunda (time-lock 24–48 jam) untuk transaksi bernilai besar guna memberikan jendela intervensi.")
    add_bullet("Simulasi Pra-Eksekusi: ", "Mengintegrasikan alat simulasi transaksi (seperti Tenderly) guna memvisualisasikan dampak mutasi saldo sebelum transaksi disetujui.")

    # 2.4 (Target: 100 - 150 kata | 3 poin)
    add_question("2.4 Tentukan tindakan pada 24 jam pertama dengan tetap menjaga integritas bukti digital. [3 poin | CPMK 4 | C5]")
    add_para("Tindakan terukur pada 24 jam pertama dengan menjaga integritas bukti digital:")
    add_item("1. Jam 0–2 (Isolasi Non-Destruktif & Preservasi Bukti): ", 
             "Putuskan perangkat staf dari internet tanpa mematikan daya (power off). Lakukan akuisisi RAM (memory dump) untuk mengamankan data volatil dan session token, disusul pembuatan bit-stream image disk terverifikasi hash SHA-256.")
    add_item("2. Jam 2–6 (Containment & Penyelamatan Aset): ", 
             "Periksa status on-chain dari perangkat bersih yang terisolasi. Segera cabut (revoke) seluruh token allowance yang terkompromi dan selamatkan sisa dana ke cold storage atau multisig baru.")
    add_item("3. Jam 6–12 (Tracing & Koordinasi Eksternal): ", 
             "Lacak transaksi dan alamat penampung dana peretas. Kirimkan permohonan pembekuan darurat (freeze request) beserta bukti hash ke bursa terpusat (CEX) terkait.")
    add_item("4. Jam 12–24 (Konsolidasi Forensik): ", 
             "Amankan log gateway/proxy, susun laporan kronologi awal untuk manajemen dan kepolisian (cyber crime unit), serta rilis pernyataan publik terukur tanpa membocorkan detail teknis.")

    # --- 4. KASUS 3 ---
    add_case_title("Kasus 3 Audit Smart Contract Vault")
    add_para("Sebuah vault menerima setoran token dan memungkinkan pengguna menarik saldo. Pengembang menuliskan alur penarikan secara sederhana: kontrak memeriksa saldo, mengirim token atau aset kepada pemanggil melalui external call, lalu mengurangi saldo pengguna. Kontrak juga menggunakan oracle harga tunggal dan fungsi admin untuk mengganti alamat oracle tanpa time-lock. Deployment direncanakan langsung ke mainnet tanpa pengujian invariant.", space_after=6)

    # 3.1 (Target: 150 - 220 kata | 4 poin)
    add_question("3.1 Identifikasi sekurang-kurangnya tiga kerentanan atau kelemahan desain beserta dampaknya. [4 poin | CPMK 3 dan CPMK 4 | C4]")
    add_para("Berdasarkan analisis smart contract vault, diidentifikasi empat kerentanan kritis beserta dampaknya:")
    add_item("1. Kerentanan Reentrancy (Kritis): ", 
             "Fungsi penarikan melakukan external call sebelum saldo internal pengguna dikurangi (balances[msg.sender]). Penyerang dapat menyebarkan kontrak eksploitasi dengan fallback() yang memanggil ulang withdraw() secara rekursif sebelum mutasi state dicatat. Dampaknya, seluruh cadangan dana vault dapat dikuras habis dalam satu transaksi.")
    add_item("2. Ketergantungan Oracle Harga Tunggal (Tinggi): ", 
             "Mengandalkan satu oracle menciptakan Single Point of Failure. Oracle tunggal (spot DEX) rentan dimanipulasi melalui serangan flash loan dalam satu blok. Dampaknya, penyerang dapat mendistorsi kalkulasi harga aset untuk menarik dana melebihi hak proporsionalnya, memicu kebangkrutan likuiditas.")
    add_item("3. Ketiadaan Time-Lock pada Fungsi Admin (Tinggi): ", 
             "Admin dapat mengganti alamat oracle seketika tanpa jeda tunda (time-lock). Jika private key admin bocor, peretas dapat mengarahkan oracle ke kontrak palsu buatannya yang mengembalikan harga manipulatif dan melucuti seluruh aset pengguna seketika.")
    add_item("4. Ketiadaan Circuit Breaker dan Uji Invariant (Sedang-Tinggi): ", 
             "Deployment langsung ke mainnet tanpa pengujian invariant matematis dan tanpa fungsi pause switch menghilangkan pertahanan krisis. Dampaknya, pengelola tidak dapat membekukan kontrak saat eksploitasi terjadi, menjamin kerugian total bagi deposan.")

    # 3.2 (Target: 200 - 280 kata | 5 poin)
    add_question("3.2 Usulkan perbaikan urutan logika penarikan dan kontrol akses admin. Jelaskan alasan setiap kontrol. [5 poin | CPMK 3 | C6]")
    add_para("A. Usulan Perbaikan Logika Penarikan (Withdrawal Logic):", bold=True, space_before=2, space_after=2, keep_with_next=True)
    add_item("1. Pola Checks-Effects-Interactions (CEI): ", 
             "Urutan eksekusi fungsi withdraw wajib dibalik secara ketat: (a) Checks: Validasi input dan saldo pemanggil: require(balances[msg.sender] >= amount, 'Saldo tidak cukup');; (b) Effects: Kurangi saldo internal pengguna pada state kontrak terlebih dahulu: balances[msg.sender] -= amount;; (c) Interactions: Lakukan transfer aset ke alamat eksternal pemanggil. Alasan: Jika terjadi reentrancy, pengecekan saldo pada panggilan rekursif akan gagal karena saldo pengguna sudah berkurang.")
    add_item("2. Mutex Guard (nonReentrant): ", 
             "Menambahkan modifier nonReentrant dari OpenZeppelin ReentrancyGuard sebagai proteksi ganda (defense-in-depth). Alasan: Mencegah eksekusi konkuren fungsi penarikan selama panggilan eksternal masih berlangsung.")
    add_item("3. SafeERC20: ", 
             "Membungkus transfer token dengan library SafeERC20 (safeTransfer). Alasan: Menangani token non-standar yang tidak mengembalikan nilai boolean agar transaksi tidak gagal secara tersembunyi.")
    add_para("B. Usulan Perbaikan Kontrol Akses Admin dan Tata Kelola Oracle:", bold=True, space_before=2, space_after=2, keep_with_next=True)
    add_item("1. Tata Kelola Multi-Signature: ", 
             "Menghapus hak admin EOA tunggal dan mengalihkannya ke kontrak multi-sig (minimal 3-of-5). Alasan: Menghilangkan risiko kegagalan tunggal apabila satu private key hilang atau disusupi.")
    add_item("2. Time-Lock Controller (24–48 Jam): ", 
             "Mewajibkan seluruh perubahan parameter kritis, terutama penggantian alamat oracle, melewati antrean tunda minimal 24–48 jam disertai emisi event on-chain transparan. Alasan: Memberikan jeda waktu bagi pengguna untuk memeriksa perubahan dan menarik dana mereka secara aman jika terjadi anomali.")
    add_item("3. Redundansi Multi-Oracle: ", 
             "Menggunakan agregator terdesentralisasi (Chainlink) yang dipadukan dengan TWAP DEX, dilengkapi pemeriksaan keusangan data (staleness check via updatedAt), validasi deviasi harga, dan circuit breaker harga wajar.")
    add_item("4. Emergency Pause: ", 
             "Menerapkan fungsi pause() berbasis peran (Pausable) untuk membekukan setoran dan penarikan saat terdeteksi kondisi darurat.")

    # 3.3 (Target: 150 - 220 kata | 4 poin)
    add_question("3.3 Rancang strategi pengujian yang memuat unit test, fuzzing atau property-based test, serta invariant utama. [4 poin | CPMK 3 dan CPMK 4 | C6]")
    add_para("Strategi pengujian komprehensif dirancang melalui pendekatan multi-layer sebelum rilis produksi:")
    add_item("1. Unit Testing: ", 
             "Menguji seluruh alur logika deterministik dan kasus batas (edge cases): setoran, penarikan normal, penolakan penarikan nir-saldo atau melebihi saldo, transfer token non-standar, pembatasan akses admin, serta simulasi serangan reentrancy aktif via mock contract guna memastikan proteksi pola CEI dan modifier nonReentrant.")
    add_item("2. Fuzzing & Property-Based Testing: ", 
             "Memanfaatkan framework Foundry (Forge) atau Echidna untuk mengeksekusi ratusan ribu kombinasi urutan transaksi acak dengan nilai parameter ekstrem guna mendeteksi celah pembulatan aritmatika serta underflow/overflow.")
    add_para("3. Invariant Utama (Formal Invariants):", bold=True, space_before=2, space_after=1, keep_with_next=True)
    add_bullet("Invariant Solvabilitas: ", "Saldo aset cadangan fisik vault harus selalu lebih besar atau sama dengan total kewajiban pengguna (TotalAsetFisik >= TotalKewajiban).")
    add_bullet("Invariant Non-Negativitas Saldo: ", "Saldo akun pengguna tidak boleh pernah bernilai negatif dalam kondisi transaksi apa pun.")
    add_bullet("Invariant Integritas Penarikan: ", "Total aset yang ditarik seorang pengguna tidak boleh melebihi setoran sah ditambah imbal hasil proporsionalnya.")
    add_bullet("Invariant Otorisasi: ", "Parameter kritis (oracle, jeda waktu) hanya dapat diubah melalui antrean time-lock dan persetujuan multisig.")
    add_item("4. Analisis Statis & Testnet: ", 
             "Menjalankan audit statis (Slither) dan uji coba operasional pada testnet publik.", space_before=3)

    # 3.4 (Target: 60 - 100 kata | 2 poin)
    add_question("3.4 Putuskan apakah deployment harus dilanjutkan atau ditunda dan nyatakan kriteria go atau no-go. [2 poin | CPMK 4 | C5]")
    add_item("Keputusan: ", "TUNDA (NO-GO) deployment ke mainnet secara mutlak hingga seluruh kerentanan kritis diperbaiki dan diverifikasi.")
    add_para("Kriteria Go / No-Go Terukur:", bold=True, space_before=2, space_after=2, keep_with_next=True)
    add_item("1. Remediasi Kerentanan Kritis: ", 
             "Seluruh temuan kerentanan Kritis dan Tinggi (Reentrancy, oracle spot, hak admin instan) tuntas diperbaiki dan lolos verifikasi auditor eksternal.")
    add_item("2. Verifikasi Invariant: ", 
             "Invariant solvabilitas vault lolos uji fuzzing minimal 100.000 run tanpa satupun pelanggaran properti.")
    add_item("3. Pengamanan Kontrak: ", 
             "Kontrak multisig (minimal 3-of-5) dan time-lock controller (24–48 jam) aktif terpasang.")
    add_item("4. Uji Testnet: ", 
             "Vault beroperasi tanpa anomali di testnet selama minimal dua minggu sebelum rilis canary bertahap.")

    # --- 5. KASUS 4 - Page Break to ensure Case 4 starts cleanly ---
    doc_new.add_page_break()
    add_case_title("Kasus 4 Investigasi Aliran Dana Lintas Jaringan")
    add_para("Sebuah alamat A menerima aset hasil eksploitasi protokol DeFi. Dana kemudian dipecah ke enam alamat, sebagian ditukar melalui decentralized exchange, lalu dipindahkan melalui bridge ke jaringan lain. Salah satu alamat tujuan mengirim dana ke alamat deposit yang diduga milik exchange terpusat. Tim investigasi memiliki transaction hash, timestamp, alamat kontrak, dan log event, tetapi belum memiliki informasi identitas pemilik alamat.", space_after=6)

    # 4.1 (Target: 150 - 220 kata | 4 poin)
    add_question("4.1 Jelaskan metode rekonstruksi aliran dana dan artefak on-chain yang harus dikumpulkan. [4 poin | CPMK 4 | C4]")
    add_para("A. Metode Rekonstruksi Aliran Dana:", bold=True, space_before=2, space_after=2, keep_with_next=True)
    add_para("Rekonstruksi dilakukan melalui analisis graf transaksi terarah (DAG) dengan memetakan alamat sebagai node dan transfer aset sebagai edge:")
    add_item("1. Pelacakan Percabangan (Fan-Out): ", 
             "Menelusuri aliran dana keluar dari alamat A ke enam alamat perantara untuk memetakan skema pemecahan (layering).")
    add_item("2. Dekonvolusi DEX: ", 
             "Membedah log event swap (Transfer, Swap, Sync) pada router DEX guna melacak token masukan, token keluaran, nilai konversi, dan alamat penerima.")
    add_item("3. Pelacakan Lintas Rantai: ", 
             "Menghubungkan peristiwa penguncian dana (event Lock/Deposit) di rantai asal dengan peristiwa pelepasan dana (event Mint/Unlock) di rantai tujuan berdasarkan relasi nonce, timestamp, dan nominal transaksi.")
    add_item("4. Penelusuran Titik Akhir: ", 
             "Melacak pergerakan dana hingga mencapai alamat deposit bursa terpusat (CEX).")
    add_para("B. Artefak On-Chain yang Harus Dikumpulkan:", bold=True, space_before=2, space_after=2, keep_with_next=True)
    add_bullet("Identifikasi Transaksi: ", "Hash transaksi, block height, dan timestamp UTC.")
    add_bullet("Entitas Alamat: ", "Alamat pengirim (from), penerima (to), dan penandatangan transaksi (origin).")
    add_bullet("Alamat Kontrak: ", "Smart contract token ERC-20, router DEX, dan gateway bridge.")
    add_bullet("Log Event & Topik: ", "Log event mentah, topic terindeks, serta data payload heksadesimal.")
    add_bullet("Trace Internal & Status: ", "Jejak panggilan internal kontrak, resi status transaksi, dan konsumsi gas fee.")

    # 4.2 (Target: 150 - 220 kata | 4 poin)
    add_question("4.2 Nilai kekuatan dan keterbatasan heuristik common-input, clustering waktu, dan hubungan alamat deposit. [4 poin | CPMK 4 | C5]")
    add_para("Evaluasi kekuatan dan keterbatasan ketiga heuristik analisis blockchain:")
    add_para("1. Heuristik Common-Input Ownership:", bold=True, space_before=3, space_after=1, keep_with_next=True)
    add_bullet("Kekuatan: ", "Sangat andal pada model UTXO (Bitcoin), di mana penggabungan beberapa input dalam satu transaksi membuktikan kepemilikan oleh satu entitas yang sama.")
    add_bullet("Keterbatasan: ", "Tidak berlaku langsung pada model berbasis akun (Ethereum/EVM) karena setiap transaksi hanya memiliki satu pengirim (msg.sender). Analisis harus bertumpu pada sumber gas fee awal yang sama atau penandatangan multisig bersama.")
    
    add_para("2. Clustering Waktu (Temporal Analysis):", bold=True, space_before=3, space_after=1, keep_with_next=True)
    add_bullet("Kekuatan: ", "Efektif mendeteksi otomatisasi bot, seperti pemecahan dana dari alamat A ke enam alamat perantara dalam blok yang sama atau selang detik berdekatan.")
    add_bullet("Keterbatasan: ", "Rentan kesalahan positif akibat jam sibuk jaringan global, serta mudah dikaburkan penyerang dengan menyetel jeda waktu acak (randomized delay).")
    
    add_para("3. Hubungan Alamat Deposit (Deposit Address Clustering):", bold=True, space_before=3, space_after=1, keep_with_next=True)
    add_bullet("Kekuatan: ", "Sangat kuat mengaitkan alamat on-chain dengan entitas bursa resmi (CEX) melalui identifikasi penyapuan saldo (sweeping) ke hot wallet utama CEX.")
    add_bullet("Keterbatasan: ", "Hanya mengidentifikasi platform bursa, bukan identitas pemilik rekening, karena pelaku kerap menggunakan akun sewaan atau identitas curian (mule account).")

    # 4.3 (Target: 150 - 220 kata | 4 poin)
    add_question("4.3 Susun chain of custody untuk menjaga bukti hasil ekstraksi blockchain dan data pendukung off-chain. [4 poin | CPMK 4 | C6]")
    add_para("Prosedur Chain of Custody disusun untuk menjaga integritas dan keabsahan bukti digital di ranah hukum:")
    add_item("1. Dokumentasi Sumber Akuisisi: ", 
             "Mencatat metadata penarikan bukti secara rinci: URL RPC node, versi client, block height, rentang blok, serta cap waktu presisi UTC.")
    add_item("2. Hashing Kriptografis Seketika: ", 
             "Menghitung nilai hash SHA-256 pada seluruh data mentah on-chain (JSON-RPC response, trace, receipt) dan data off-chain (log transaksi CEX, screenshot explorer) segera setelah diunduh, lalu mendokumentasikannya ke Berita Acara.")
    add_item("3. Pemisahan Master Copy dan Working Copy: ", 
             "Menyimpan salinan master pada media terenkripsi berstatus write-once-read-many (WORM). Analisis graf, decoding ABI, dan penyelidikan hanya dilakukan pada working copy.")
    add_item("4. Log Rantai Penjagaan (Evidence Log Sheet): ", 
             "Mencatat setiap interaksi terhadap bukti: nama personel, tanggal/waktu, tujuan tindakan, serta verifikasi ulang hash SHA-256 sebelum dan sesudah analisis untuk menjamin nir-perubahan data.")
    add_item("5. Reprodusibilitas Metodologi: ", 
             "Mengarsipkan skrip otomatisasi ekstraksi beserta dependensi pustaka agar hasil rekonstruksi dapat diverifikasi ulang secara identik oleh pihak independen.")

    # 4.4 (Target: 100 - 150 kata | 3 poin)
    add_question("4.4 Tuliskan kesimpulan investigatif yang membedakan atribusi alamat, atribusi layanan, dan atribusi individu. [3 poin | CPMK 4 | C5]")
    add_para("Kesimpulan investigatif ditarik dengan membedakan secara tegas tiga tingkatan atribusi:")
    add_item("1. Atribusi Alamat (Tingkat Keyakinan: Pasti / Bukti On-Chain): ", 
             "Tercatat secara deterministik bahwa alamat A mengirimkan aset ke enam alamat perantara, melakukan swap di DEX, memindahkan dana via bridge, dan meneruskannya ke alamat penerima 0xDeposit... Fakta perpindahan aset antarnode ini terbukti matematis dan permanen pada buku besar blockchain.")
    add_item("2. Atribusi Layanan (Tingkat Keyakinan: Tinggi / Analisis Perilaku On-Chain): ", 
             "Berdasarkan transaksi penyapuan saldo (sweeping) dari 0xDeposit... menuju hot wallet utama yang terverifikasi publik, alamat tersebut dipastikan sebagai alamat deposit milik bursa terpusat (CEX) tertentu.")
    add_item("3. Atribusi Individu (Tingkat Keyakinan: Belum Terbukti / Memerlukan Data Hukum Off-Chain): ", 
             "Identitas fisik pengendali alamat belum dapat dipastikan. Pengungkapan identitas pelaku memerlukan proses hukum formal (subpoena) kepada pihak bursa untuk membuka data KYC, log IP login, dan rekening bank penarikan fiat yang terhubung.")

    # Save new document
    doc_new.save(DST_PATH)
    print(f"Document successfully created at: {DST_PATH}")

if __name__ == '__main__':
    build_document()
