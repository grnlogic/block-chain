#!/usr/bin/env python3
"""
Generate Gambar 3: Pengamanan Berlapis (Defense-in-Depth)
Type: Concentric Layered Boxes (Landscape SVG -> PNG)
Format: Pure Grayscale, No em-dash/en-dash, No tspan tags.
"""

import subprocess

svg_content = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1500 1000" width="1500" height="1000">
  <!-- Background -->
  <rect width="1500" height="1000" fill="#ffffff" />
  <rect x="20" y="20" width="1460" height="960" rx="8" fill="#ffffff" stroke="#222222" stroke-width="1.2" />

  <!-- Main Title -->
  <text x="50" y="60" font-family="Liberation Sans, Arial" font-size="20" font-weight="bold" fill="#111111">ARSITEKTUR PENGAMANAN BERLAPIS (DEFENSE-IN-DEPTH)</text>
  <text x="50" y="84" font-family="Liberation Sans, Arial" font-size="13" fill="#555555">Model Lapisan Konsentris: Melindungi Inti Aset Treasury Melalui Empat Pilar Pengamanan</text>

  <!-- ==================== LAYER 1: MANUSIA (OUTERMOST) ==================== -->
  <g transform="translate(60, 110)">
    <!-- Layer 1 Container -->
    <rect x="0" y="0" width="1380" height="830" rx="8" fill="#f8f8f8" stroke="#333333" stroke-width="2" />
    <rect x="25" y="15" width="340" height="32" rx="4" fill="#333333" />
    <text x="35" y="36" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="#ffffff">1. LAPISAN MANUSIA (PEOPLE)</text>

    <!-- Top Left Item -->
    <rect x="420" y="15" width="440" height="32" rx="4" fill="#ffffff" stroke="#777777" stroke-width="1" />
    <text x="430" y="35" font-family="Liberation Sans, Arial" font-size="12" fill="#222222">• Pelatihan Berkala Anti-Phishing dan Typosquatting</text>

    <!-- Top Right Item -->
    <rect x="880" y="15" width="460" height="32" rx="4" fill="#ffffff" stroke="#777777" stroke-width="1" />
    <text x="890" y="35" font-family="Liberation Sans, Arial" font-size="12" fill="#222222">• Akses Antarmuka dApp Wajib Melalui Bookmark Resmi</text>

    <!-- Bottom Left Item -->
    <rect x="25" y="780" width="460" height="32" rx="4" fill="#ffffff" stroke="#777777" stroke-width="1" />
    <text x="35" y="800" font-family="Liberation Sans, Arial" font-size="12" fill="#222222">• Verifikasi Mandiri Parameter Mentah Sebelum Tanda Tangan</text>

    <!-- Bottom Right Item -->
    <rect x="510" y="780" width="460" height="32" rx="4" fill="#ffffff" stroke="#777777" stroke-width="1" />
    <text x="520" y="800" font-family="Liberation Sans, Arial" font-size="12" fill="#222222">• Larangan Membuka Tautan Finansial dari Email dan Chat</text>

    <!-- ==================== LAYER 2: PROSES ==================== -->
    <g transform="translate(100, 65)">
      <!-- Layer 2 Container -->
      <rect x="0" y="0" width="1180" height="700" rx="8" fill="#eeeeee" stroke="#333333" stroke-width="2" />
      <rect x="25" y="15" width="340" height="32" rx="4" fill="#444444" />
      <text x="35" y="36" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="#ffffff">2. LAPISAN PROSES (PROCESS)</text>

      <!-- Top Mid Item -->
      <rect x="400" y="15" width="420" height="32" rx="4" fill="#ffffff" stroke="#777777" stroke-width="1" />
      <text x="410" y="35" font-family="Liberation Sans, Arial" font-size="12" fill="#222222">• Pemisahan Tugas (Inisiator Berbeda dari Penyelia)</text>

      <!-- Top Right Item -->
      <rect x="840" y="15" width="315" height="32" rx="4" fill="#ffffff" stroke="#777777" stroke-width="1" />
      <text x="850" y="35" font-family="Liberation Sans, Arial" font-size="12" fill="#222222">• Standar Operasional Respons Tanggap Darurat</text>

      <!-- Bottom Items -->
      <rect x="25" y="650" width="450" height="32" rx="4" fill="#ffffff" stroke="#777777" stroke-width="1" />
      <text x="35" y="670" font-family="Liberation Sans, Arial" font-size="12" fill="#222222">• Persetujuan Ganda (Four-Eyes Principle) Transaksi Besar</text>

      <rect x="500" y="650" width="450" height="32" rx="4" fill="#ffffff" stroke="#777777" stroke-width="1" />
      <text x="510" y="670" font-family="Liberation Sans, Arial" font-size="12" fill="#222222">• Rekonsiliasi Kas dan Audit Saldo Buku Besar Rutin</text>

      <!-- ==================== LAYER 3: WALLET ==================== -->
      <g transform="translate(100, 65)">
        <!-- Layer 3 Container -->
        <rect x="0" y="0" width="980" height="570" rx="8" fill="#dddddd" stroke="#222222" stroke-width="2" />
        <rect x="25" y="15" width="340" height="32" rx="4" fill="#333333" />
        <text x="35" y="36" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="#ffffff">3. LAPISAN WALLET (INFRASTRUKTUR)</text>

        <!-- Top Right Item -->
        <rect x="420" y="15" width="530" height="32" rx="4" fill="#ffffff" stroke="#666666" stroke-width="1" />
        <text x="430" y="35" font-family="Liberation Sans, Arial" font-size="12" fill="#222222">• Eliminasi Total Penyimpanan Kunci Privat pada Ekstensi Browser</text>

        <!-- Bottom Items -->
        <rect x="25" y="520" width="450" height="32" rx="4" fill="#ffffff" stroke="#666666" stroke-width="1" />
        <text x="35" y="540" font-family="Liberation Sans, Arial" font-size="12" fill="#222222">• Skema Multi-Signature atau MPC (Minimal Ambang 3-dari-5)</text>

        <rect x="500" y="520" width="450" height="32" rx="4" fill="#ffffff" stroke="#666666" stroke-width="1" />
        <text x="510" y="540" font-family="Liberation Sans, Arial" font-size="12" fill="#222222">• Isolasi Hardware Wallet Fisik dan Pemisahan Hot/Cold Wallet</text>

        <!-- ==================== LAYER 4: KONTROL TRANSAKSI ==================== -->
        <g transform="translate(100, 65)">
          <!-- Layer 4 Container -->
          <rect x="0" y="0" width="780" height="440" rx="8" fill="#cccccc" stroke="#111111" stroke-width="2" />
          <rect x="25" y="15" width="350" height="32" rx="4" fill="#222222" />
          <text x="35" y="36" font-family="Liberation Sans, Arial" font-size="13" font-weight="bold" fill="#ffffff">4. KONTROL TRANSAKSI (RULE-BASED)</text>

          <!-- Top Item -->
          <rect x="400" y="15" width="350" height="32" rx="4" fill="#ffffff" stroke="#444444" stroke-width="1" />
          <text x="410" y="35" font-family="Liberation Sans, Arial" font-size="12" fill="#222222">• Allowlist Alamat Kontrak dan Mitra Resmi</text>

          <!-- Bottom Items -->
          <rect x="25" y="390" width="350" height="32" rx="4" fill="#ffffff" stroke="#444444" stroke-width="1" />
          <text x="35" y="410" font-family="Liberation Sans, Arial" font-size="12" fill="#222222">• Batasan Nominal Plafon Harian (Spending Limits)</text>

          <rect x="400" y="390" width="350" height="32" rx="4" fill="#ffffff" stroke="#444444" stroke-width="1" />
          <text x="410" y="410" font-family="Liberation Sans, Arial" font-size="12" fill="#222222">• Jeda Waktu Time-Lock (24 sampai 48 Jam)</text>

          <!-- Left and Right Vertical Items in Layer 4 -->
          <rect x="25" y="70" width="220" height="55" rx="4" fill="#ffffff" stroke="#444444" stroke-width="1" />
          <text x="35" y="92" font-family="Liberation Sans, Arial" font-size="11.5" font-weight="bold" fill="#222222">Simulasi Pra-Eksekusi:</text>
          <text x="35" y="112" font-family="Liberation Sans, Arial" font-size="11" fill="#444444">Visualisasi Mutasi Saldo</text>

          <rect x="535" y="70" width="215" height="55" rx="4" fill="#ffffff" stroke="#444444" stroke-width="1" />
          <text x="545" y="92" font-family="Liberation Sans, Arial" font-size="11.5" font-weight="bold" fill="#222222">Monitoring On-Chain:</text>
          <text x="545" y="112" font-family="Liberation Sans, Arial" font-size="11" fill="#444444">Peringatan Anomali Real-Time</text>

          <!-- ==================== CORE: ASET TREASURY ==================== -->
          <g transform="translate(230, 155)">
            <rect x="0" y="0" width="320" height="170" rx="8" fill="#111111" stroke="#000000" stroke-width="2.5" />
            <rect x="8" y="8" width="304" height="154" rx="6" fill="#222222" stroke="#ffffff" stroke-width="1.5" stroke-dasharray="4,3" />
            
            <circle cx="160" cy="55" r="24" fill="#ffffff" />
            <!-- Lock / Shield Symbol -->
            <path d="M 152 50 L 152 44 C 152 39 168 39 168 44 L 168 50 Z M 147 50 L 173 50 L 173 66 L 147 66 Z" fill="#111111" />
            
            <text x="160" y="105" font-family="Liberation Sans, Arial" font-size="15" font-weight="bold" fill="#ffffff" text-anchor="middle">INTI PERLINDUNGAN</text>
            <text x="160" y="128" font-family="Liberation Sans, Arial" font-size="14" font-weight="bold" fill="#f2f2f2" text-anchor="middle">ASET TREASURY</text>
            <text x="160" y="148" font-family="Liberation Sans, Arial" font-size="11" fill="#aaaaaa" text-anchor="middle">(Saldo Dana Perbendaharaan)</text>
          </g>
        </g>
      </g>
    </g>
  </g>
</svg>
'''

out_svg = "/home/fajar-geran-arifin/Documents/kuliah/block chain/UTS bagian A/gambar/gambar3-pengamanan.svg"
out_png = "/home/fajar-geran-arifin/Documents/kuliah/block chain/UTS bagian A/gambar/gambar3-pengamanan.png"

with open(out_svg, "w") as f:
    f.write(svg_content)

print("Saved Gambar 3 SVG to", out_svg)

cmd = ["convert", "-density", "150", out_svg, out_png]
res = subprocess.run(cmd, capture_output=True, text=True)
print("Convert result:", res.returncode, res.stderr)
