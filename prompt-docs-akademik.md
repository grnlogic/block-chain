# Prompt Docs Akademik (Reusable, Versi 2)

Fajar Geran Arifin | Teknik Informatika UNSIL

Cara pakai: isi bagian KEBUTUHAN DOKUMEN, paste seluruh blok di bawah ke Claude, lalu dokumen .docx dikerjakan, diagram dipasang, dan hasilnya diperiksa sebelum diserahkan.

---

````
=== ATURAN PRIORITAS (BERLAKU UNTUK SEMUA BAGIAN) ===
1. Monochrome berlaku untuk teks, heading, hyperlink, tabel, serta diagram dan grafik yang dibuat Claude: hanya hitam, putih, abu-abu.
   PENGECUALIAN: foto, screenshot, atau gambar asli yang saya berikan atau minta dimasukkan. Gambar itu disisipkan apa adanya dengan warna aslinya. Dilarang mengubahnya ke grayscale, memberi filter, atau mengubah warnanya dengan cara apa pun. Yang boleh hanya mengubah ukuran secara proporsional (dan crop kalau saya minta).
2. Dilarang mengarang: referensi, kutipan, angka, data eksperimen, hasil pengujian, langkah kerja, nama tool, versi software, dan isi screenshot. Kalau bahan tidak ada dan pencarian referensi (langkah 2) tidak menemukan sumber terverifikasi, pakai placeholder resmi (lihat bagian PLACEHOLDER).
3. Dilarang memakai tanda pisah panjang (em dash, karakter —) dan en dash (karakter –) di seluruh dokumen, termasuk judul, keterangan gambar, isi tabel, header, dan footer. Gunakan koma, titik dua, tanda kurung, atau pecah menjadi dua kalimat. Untuk rentang angka, tulis "10 sampai 15" atau "10-15" dengan tanda hubung biasa (karakter -).
4. Font di file .docx adalah Times New Roman. Liberation Serif hanya boleh dipakai untuk render gambar dan pratinjau PDF di sandbox.
5. Kalau pedoman kampus atau dosen saya tempel di bagian KEBUTUHAN DOKUMEN, pedoman itu menimpa semua default format di prompt ini.

=== KEBUTUHAN DOKUMEN ===
Jenis dokumen        : lainnya - Laporan UTS Blockchain (mini-project Bagian B) dalam format Template Laporan Kegiatan Blockchain
Judul                : Rancangan Sistem Verifikasi Kredensial Akademik Berbasis Blockchain
Mata kuliah          : Blockchain (KP70067008), semester 7
Dosen pengampu       : Dr. Ir. Nur Widiyasono, M.Kom.
Program studi        : Informatika (S1)
Universitas          : Universitas Siliwangi
Tahun                : 2026 (TA 2026/2027 Semester Ganjil)
Target panjang       : 10-12 halaman A4 badan laporan, tidak termasuk halaman awal, daftar pustaka, dan lampiran
Spasi isi            : ikuti yang sudah ada di template (jangan diubah)
Perlu referensi paper: ya, minimal 5, utamakan dokumentasi resmi/standar/buku/artikel ilmiah. Hanya sumber yang benar-benar kamu buka dan verifikasi; jangan mengarang sitasi, halaman, atau nomor bab
Gaya sitasi          : IEEE
Struktur bab         : ikuti outline Fase 0/1 yang sudah disetujui (Ringkasan; 1 Pendahuluan P1; 2 Data, Alat, Reproduksibilitas; 3 Catatan Pelaksanaan B-xx; 4 Rancangan P2-P6 dengan subbagian 4.1-4.6; 5 Kesimpulan; Daftar Pustaka; Lampiran A Pernyataan Orisinalitas, Lampiran B Pengungkapan AI)
Pedoman kampus/dosen : dari Naskah Bagian B - 1 diagram arsitektur, 1 diagram alur transaksi, 1 matriks ancaman-mitigasi; prototipe + daftar pengujian + bukti hasil uji (jujur soal batasan); pustaka >= 5; lampiran orisinalitas dan penggunaan AI transparan; nama file NIM_Nama_UTS_Blockchain_OBE.pdf
Bahan                : design-decisions.md; folder prototype/ (README.md, test-output.txt, demo-output.txt, perf-output.txt); bukti B-01..B-08; test T-01..T-08; tabel kriteria penerimaan hasil Fase 2c/2d/2e

Kalau jenis dokumen, target panjang, atau bahan untuk suatu section belum jelas, tanyakan sekali di awal (Qmaksimal beberapa pertanyaan sekaligus, jangan bertahap) sebelum mengerjakan. Kalau sudah cukup jelas, langsung kerjakan tanpa meminta izin.

=== LANGKAH KERJA (WAJIB URUT) ===

0. PERSIAPAN
- Baca /mnt/skills/public/docx/SKILL.md sebelum menulis kode atau membuat file apa pun.
- Cek tool di sandbox: node, python, soffice (LibreOffice), pdftoppm, dot (Graphviz), chromium atau playwright, font Times New Roman atau Liberation Serif.
- Deteksi lingkungan kerja. Kalau berjalan di Antigravity atau IDE agentik lain, tentukan folder workspace yang sedang dibuka (jalankan pwd, lalu ls) dan simpan semua output di sana. Kalau berjalan di claude.ai, gunakan /mnt/user-data/outputs. Kalau /mnt/skills/public/docx/SKILL.md tidak ada, pakai library docx (npm) atau python-docx dan tetap patuhi semua aturan di prompt ini.
- Kalau dokumen butuh referensi (lihat langkah 2), cek apakah tool pencarian web dan unduhan tersedia, dan apakah domain sumber paper (arxiv.org, doi.org, dan sejenisnya) bisa diakses dari terminal.
- Untuk diagram, cek dulu apakah Chromium atau Playwright sudah terpasang (which chromium chromium-browser; ls ~/.cache/ms-playwright). Kalau sudah ada, pasang mmdc dan render Mermaid. Kalau belum ada, jangan buang waktu memasang mmdc karena unduhan Chromium biasanya diblokir jaringan sandbox. Langsung gunakan Graphviz atau matplotlib (langkah 3).

1. TULIS ISI DOKUMEN
- Baca seluruh bahan lebih dulu. Tentukan kerangka bab, lalu tentukan di section mana tiap diagram, tabel, dan gambar dibutuhkan.
- Tiap section harus langsung berisi konten. Kalau bahan untuk suatu section tipis, tulis seperlunya sesuai bahan dan laporkan di pesan akhir. Jangan mengisi dengan teks umum yang tidak berasal dari bahan.
- Susun kerangka dan daftar pernyataan yang butuh kutipan lebih dulu. Kalau referensi dibutuhkan, isi final ditulis setelah langkah 2 selesai, supaya sitasi mengacu ke paper yang benar-benar ada dan sudah dibaca.
- Tulis kode diagram per diagram sesuai jenisnya: alur proses = flowchart, komunikasi antar komponen = sequenceDiagram, arsitektur = graph TD atau LR, jadwal = timeline.

2. CARI DAN UNDUH REFERENSI (SUMBER KUTIPAN), HANYA JIKA DIBUTUHKAN
- Tentukan dulu apakah dokumen ini butuh referensi paper, sesuai isian "Perlu referensi paper":
  - ya: kerjakan langkah ini.
  - tidak: lewati seluruh langkah 2. Jangan mencari atau mengunduh paper, jangan membuat folder referensi/, dan jangan menambahkan sitasi [n], Daftar Pustaka, atau placeholder [REF] dan [KUTIPAN]. Kalau bahan saya sudah memuat referensi, tetap pakai yang ada.
  - otomatis (default): ya untuk makalah, proposal, tugas akhir, artikel, laporan KP yang punya landasan teori, dan dokumen lain yang punya bagian kajian pustaka atau latar belakang ilmiah. Tidak untuk laporan praktikum atau tugas yang seluruh isinya berasal dari hasil kerja dan bahan saya. Kalau ragu, pilih tidak mencari dan tulis satu kalimat alasannya di pesan akhir.
- Cari referensi hanya untuk bagian yang memang butuh dukungan literatur (misal latar belakang, landasan teori, pembahasan). Bagian yang bersumber dari data, hasil, atau pekerjaan saya sendiri (misal metodologi dan hasil) tidak perlu paper.
- Batasi supaya cepat: cari secukupnya dan berhenti begitu tiap klaim penting sudah punya sumber. Jangan melebihi target jumlah di bawah.
- Lokasi folder: buat folder `referensi/` di root folder yang sedang dibuka di Antigravity (hasil pwd pada langkah 0), bukan di home atau folder acak. Kalau folder sudah ada, pakai dan jangan menghapus isinya. Kalau berjalan di claude.ai, buat di /mnt/user-data/outputs/referensi/.
- Cari paper yang berkaitan dengan topik tiap section lewat pencarian web, dengan kata kunci bahasa Inggris dan Indonesia. Prioritaskan jurnal dan prosiding, 5 tahun terakhir kecuali karya klasik yang memang dasar bidangnya. Jumlah: sesuai isian, atau default 5 sampai 10 untuk dokumen besar dan 3 sampai 5 untuk tugas kecil.
- Referensi yang sudah ada di bahan saya tetap diprioritaskan dan tidak perlu dicari ulang. Kalau PDF-nya tersedia, unduh juga.
- Unduh hanya dari sumber akses terbuka yang sah: arXiv, PubMed Central, DOAJ, jurnal open access, repositori institusi, atau tautan PDF resmi dari penulis. Dilarang memakai Sci-Hub, mirror ilegal, atau cara apa pun untuk melewati paywall. Kalau paper berbayar, jangan diunduh: catat metadata yang terverifikasi dari halaman sumbernya, beri status "berbayar, belum terunduh", dan minta saya mengunduh manual.
- Verifikasi tiap file: PDF benar-benar terbuka dan berisi paper (bukan halaman HTML atau error), lalu judul, penulis, tahun, dan venue cocok dengan halaman sumber. Metadata diambil dari file atau halaman sumber, bukan dari ingatan.
- Kutipan hanya boleh memuat klaim yang benar-benar ada di teks paper yang sudah dibaca (minimal abstrak, pendahuluan, dan bagian yang relevan). Utamakan parafrase. Kutipan langsung harus pendek, memakai tanda kutip, dan disertai nomor halaman.
- Nama file: NamaBelakangPenulisPertama_Tahun_KataKunciJudul.pdf, tanpa spasi (contoh: Halfond_2006_SQLInjection.pdf).
- Buat `referensi/DAFTAR_REFERENSI.md` berisi: nomor sitasi, metadata lengkap, DOI atau URL, nama file, status (terunduh, berbayar, atau gagal unduh), dan satu kalimat klaim yang didukung paper itu. Isi folder hanya PDF referensi dan file daftar ini.
- Kalau unduhan gagal karena jaringan atau domain diblokir, jangan mengarang. Verifikasi metadata dari halaman sumber lewat pencarian web, catat URL PDF langsung di DAFTAR_REFERENSI.md dengan status "gagal unduh: jaringan", dan laporkan domain yang perlu diizinkan atau minta saya mengunduh manual. Sitasi hanya boleh dipakai kalau isi klaimnya benar-benar terbaca dari halaman atau abstrak. Kalau tidak terbaca, pakai placeholder [KUTIPAN].

3. RENDER DIAGRAM JADI GAMBAR (JANGAN DITINGGAL SEBAGAI KODE)
- Simpan tiap diagram sebagai file .mmd (atau .dot kalau memakai Graphviz), lalu render ke PNG.
- Konfigurasi Mermaid wajib memakai config tetap ini:
  {"theme":"base","themeVariables":{"primaryColor":"#ffffff","primaryBorderColor":"#000000","primaryTextColor":"#000000","lineColor":"#000000","secondaryColor":"#f2f2f2","tertiaryColor":"#ffffff","noteBkgColor":"#f2f2f2","noteTextColor":"#000000","noteBorderColor":"#000000","actorBkg":"#ffffff","actorBorder":"#000000","actorTextColor":"#000000","actorLineColor":"#000000","signalColor":"#000000","signalTextColor":"#000000","fontFamily":"Liberation Serif"}}
- Background putih, scale minimal 3 agar tajam saat dicetak.
- Kalau memakai Graphviz atau matplotlib: node putih atau abu terang (#f2f2f2), garis dan teks hitam, font serif, tanpa warna lain, dengan struktur yang sama seperti diagram yang direncanakan.
- Kalau semua cara render gagal, baru sisipkan blok kode di section terkait, dan laporkan jelas diagram mana yang belum ter-render beserta alasannya.
- Grafik dari data (bar, line, dan sejenisnya) dibuat dengan matplotlib, grayscale, font serif, memakai data yang benar-benar ada di bahan. Kalau tidak ada data, jangan membuat grafik.

4. PASANG GAMBAR KE DOCX
- Sisipkan gambar di section yang membahas topiknya, bukan di lampiran.
- Urutan per gambar:
  1. Paragraf pengantar konteks (1 sampai 2 kalimat) yang merujuk gambar ("seperti pada Gambar 2")
  2. Gambar, rata tengah, rasio aspek terjaga
  3. Keterangan di bawah gambar: "Gambar X. Judul gambar" (X berurutan, atau format bab seperti 4.3 kalau kampus memakainya)
  4. Paragraf penjelasan alur atau komponen yang digambarkan
- Batas ukuran mengikuti area teks. Dengan margin default (kiri 4 cm, kanan 3 cm) lebar area teks A4 hanya 14 cm, jadi lebar gambar maksimal 14 cm dan tinggi maksimal 18 cm. Kalau diagram melebihi batas itu, ganti arah (TD ke LR atau sebaliknya), pecah menjadi beberapa diagram, atau sederhanakan. Jangan memperkecil sampai teks di dalam gambar tidak terbaca.
- Gambar dan keterangannya harus selalu di halaman yang sama (keep with next).
- Simpan juga file sumber (.mmd atau .dot) dan PNG tiap diagram sebagai output tambahan.

5. FOTO DAN SCREENSHOT ASLI
- Screenshot sistem, terminal, atau hardware tidak boleh dikarang atau digambar ulang seolah asli.
- Sisipkan kotak bingkai (border hitam tipis, isi abu sangat terang #f2f2f2, teks di tengah) berisi deskripsi spesifik, misal: "Screenshot terminal hasil SQL Injection pada endpoint /login". Ukurannya proporsional seperti gambar asli.
- Beri keterangan "Gambar X. ..." seperti gambar lain. Saya tinggal mengganti kotaknya dengan foto asli.
- Kalau saya sudah memberikan foto atau screenshot asli, sisipkan dengan warna aslinya (lihat aturan prioritas 1), rata tengah, rasio aspek terjaga, batas lebar 14 cm dan tinggi 18 cm, dengan keterangan seperti gambar lain. Jangan dikonversi ke grayscale.

6. VERIFIKASI HASIL (WAJIB SEBELUM DISERAHKAN)
- Konversi .docx ke PDF dengan soffice, lalu ke PNG per halaman dengan pdftoppm pada resolusi 80 sampai 100 dpi. Periksa per batch beberapa halaman agar konteks tidak habis.
- Lihat setiap halaman sebagai gambar dan periksa checklist:
  - Tidak ada kode Mermaid atau Graphviz mentah yang tertinggal
  - Semua diagram ter-render, tidak terpotong, teks di dalamnya terbaca
  - Gambar tidak melewati margin dan tidak terpisah dari keterangannya
  - Nomor gambar dan tabel berurutan, cocok dengan rujukan di teks
  - Font Times New Roman di seluruh dokumen (cek juga tabel, keterangan, header, footer, dan nomor halaman di file .docx)
  - Teks, heading, hyperlink, tabel, diagram, dan grafik hanya hitam, putih, abu-abu. Foto dan screenshot asli dari saya tetap berwarna asli (tidak ter-grayscale)
  - Tidak ada em dash atau en dash (cari karakter — dan – di seluruh isi dokumen, termasuk header, footer, tabel, dan properti dokumen)
  - Ukuran kertas A4, margin, spasi, dan indentasi sesuai bagian FORMAT HALAMAN
  - Semua istilah asing bahasa Inggris dimiringkan di setiap kemunculannya (isi, heading, tabel, keterangan), dan nama produk, singkatan, serta istilah baku tidak ikut dimiringkan
  - Ketentuan umum terpenuhi: tiap bab punya paragraf pengantar, tidak ada sub judul tunggal, angka, satuan, dan tanggal sesuai aturan, kutipan panjang berbentuk blok, kode program berketerangan
  - Tabel: border hitam solid, background putih, header bold, tidak melebar keluar halaman, judul tabel di atas
  - Identitas ada di halaman judul dan/atau header
  - Heading rapi, tidak ada halaman kosong, tidak ada heading yatim di dasar halaman
  - Hierarki judul dan poin makin menjorok di tiap tingkat, baris lanjutan sejajar dengan teks (hanging indent), dan penomoran berasal dari list Word asli, bukan ketikan manual. Periksa langsung di gambar halaman, bukan hanya dari kode: ambil satu poin yang teksnya lebih dari satu baris dan pastikan baris keduanya lurus dengan huruf pertama teks baris pertama, bukan dengan nomor atau margin kiri
  - (Kalau memakai referensi) setiap [n] di teks ada di Daftar Pustaka, dan setiap entri Daftar Pustaka dirujuk di teks
  - (Kalau memakai referensi) folder referensi/ ada di lokasi yang benar, setiap PDF di dalamnya terbuka dan cocok dengan entri di DAFTAR_REFERENSI.md, dan setiap sitasi punya file atau status yang jujur (berbayar atau gagal unduh)
  - (Kalau memakai referensi) klaim yang dikutip memang ada di paper yang dirujuk, bukan hanya cocok dengan judulnya
  - Tidak ada catatan meta atau sisa komentar, tracked changes, atau properti dokumen berisi nama lain
  - Placeholder hanya dari jenis yang diizinkan dan dicetak bold
- Kalau ada yang gagal: perbaiki, generate ulang, cek lagi, ulangi sampai lolos. Kalau ada yang tetap tidak bisa diperbaiki, laporkan apa adanya di pesan akhir. Jangan menyatakan lolos kalau belum dicek.

=== FORMAT HALAMAN (DEFAULT, DITIMPA PEDOMAN KAMPUS JIKA ADA) ===
- Kertas A4, portrait.
- Margin: kiri 4 cm, atas 4 cm, kanan 3 cm, bawah 3 cm.
- Font Times New Roman 12 pt untuk isi. Heading 1: 14 pt bold, huruf kapital, rata tengah (misal "BAB I PENDAHULUAN"). Heading 2: 12 pt bold, kapital di awal tiap kata. Heading 3: 12 pt bold italic.
- Spasi isi: sesuai isian "Spasi isi" (1,5 atau 2). Tanpa jarak tambahan sebelum atau sesudah paragraf (space before/after 0), tidak ada baris kosong antarparagraf.
- Spasi tunggal (1,0) untuk: isi tabel, keterangan gambar dan tabel, kutipan langsung yang panjang, dan baris di dalam satu entri Daftar Pustaka. Antar entri Daftar Pustaka diberi jarak satu spasi kosong.
- Paragraf rata kiri-kanan (justify), baris pertama menjorok 1 cm.
- Penomoran heading bertingkat: BAB I, lalu 1.1, lalu 1.1.1 (default). Kalau pedoman kampus memakai huruf (A, B, C) untuk sub judul, ikuti pedoman itu. Pilih satu sistem dan konsisten di seluruh dokumen.

HIERARKI JUDUL DAN POIN (INDENTASI BERTINGKAT):
- Prinsipnya: makin dalam tingkatnya, makin menjorok ke kanan. Sub judul lebih menjorok daripada judul di atasnya, dan poin di bawah sub judul lebih menjorok lagi.
- Semua penomoran dan indentasi dibuat dengan fitur multilevel list dan style Word yang sebenarnya (numbering config atau style Heading), bukan dengan mengetik nomor, spasi, atau tab manual.
- Setiap judul bernomor dan setiap poin (A., 1., a., (1)) WAJIB memakai hanging indent: nomor berada di posisi kiri, dan seluruh baris teks, termasuk baris kedua dan seterusnya, sejajar lurus dengan huruf pertama teks setelah nomor. Di Word, atur indent Left sebesar posisi teks dan Hanging sebesar lebar nomor (di docx-js: indent {left, hanging}), bukan firstLine.
- Kesalahan yang dilarang: hanya baris pertama yang menjorok (first-line indent) sementara baris lanjutan kembali ke margin kiri atau ke bawah nomor. Contoh salah: "b. Contoh penerapan ..." pada baris pertama, lalu baris kedua mulai dari margin kiri. Contoh benar: baris kedua mulai tepat di bawah huruf "C" pada kata "Contoh".
- Indent baris pertama sebesar 1 cm hanya untuk paragraf isi biasa yang bukan poin dan bukan judul.
- Ukuran indentasi default (posisi nomor dari margin kiri, dan lebar hanging):
  - Tingkat 1, BAB I: rata tengah, tanpa indentasi.
  - Tingkat 2, sub judul (1.1 atau A): nomor di 0 cm, hanging 1 cm.
  - Tingkat 3, sub-sub judul (1.1.1 atau 1): nomor di 1 cm, hanging 1,25 cm.
  - Tingkat 4 (a, b, c): nomor di 2,25 cm, hanging 0,75 cm.
  - Tingkat 5 ((1), (2)): nomor di 3 cm, hanging 0,75 cm.
- Poin berjenjang di dalam isi (bukan heading) memakai urutan simbol tetap: A. lalu 1. lalu a. lalu (1) lalu tanda hubung (-). Contoh bentuk: A. poin utama, di bawahnya 1. poin turunan yang lebih menjorok, di bawahnya a. poin lebih dalam yang makin menjorok.
- Paragraf penjelasan atau lanjutan di bawah sebuah poin diindentasi penuh sejajar dengan awal teks poin itu (Left sama dengan posisi teks poin, tanpa first-line indent tambahan, semua barisnya lurus), bukan kembali ke margin kiri.
- Spasi antar poin mengikuti spasi isi, tanpa baris kosong tambahan. Jangan membuat lebih dari lima tingkat. Kalau hierarki lebih dalam dari itu, gabungkan atau pecah menjadi sub judul baru.
- Kalimat pengantar poin diakhiri titik dua, dan poin yang berupa kalimat lengkap diawali huruf kapital dan diakhiri titik. Poin yang berupa frasa diawali huruf kecil dan diakhiri titik koma, dengan poin terakhir diakhiri titik.
- Nomor halaman: bagian awal (kata pengantar, daftar isi, daftar gambar, daftar tabel) memakai angka Romawi kecil (i, ii, iii); isi dimulai dari angka Arab 1. Posisi bawah tengah pada halaman awal bab, dan kanan atas pada halaman lainnya.
- Halaman awal disesuaikan jenis dokumen:
  - Laporan praktikum, tugas, atau makalah: halaman judul, daftar isi, daftar gambar, dan daftar tabel (kalau ada gambar atau tabel). Tidak perlu lembar pengesahan.
  - Laporan KP, proposal, atau tugas akhir: halaman judul, lembar pengesahan (dibuat kosong untuk tanda tangan, tanpa nama pejabat yang dikarang), kata pengantar, abstrak, daftar isi, daftar gambar, daftar tabel.
  - Dilarang membuat logo sendiri. Beri ruang kosong dengan bingkai tipis bertuliskan "Logo Universitas" di halaman judul.
- Daftar isi, daftar gambar, dan daftar tabel dibuat otomatis (field Word), lengkap dengan nomor halaman, dan sudah ter-update saat diserahkan.

=== ATURAN PENULISAN ===

IDENTITAS (ditaruh di halaman judul):
- Nama  : Fajar Geran Arifin
- NPM   : 237006079
- Kelas : C Informatika
- Lengkapi dengan mata kuliah, dosen pengampu, program studi, universitas, dan tahun dari bagian KEBUTUHAN DOKUMEN. Field yang kosong dilewati, jangan diisi karangan.

BAHASA:
- Bahasa Indonesia formal, baku, akademik, ejaan mengikuti PUEBI/KBBI.
- Kalimat cenderung pasif dan tidak memakai kata "saya", "kami", atau "kita" di isi (kecuali kata pengantar).
- Semua istilah asing (termasuk bahasa Inggris) dicetak miring di setiap kemunculannya, bukan hanya saat pertama muncul. Berlaku di isi, heading, tabel, dan keterangan gambar atau tabel. Contoh: *firewall*, *machine learning*, *SQL injection*.
- Yang tidak dimiringkan: nama diri, nama produk, merek, library, dan framework (MySQL, Laravel, Python), singkatan (SQL, API), serta istilah yang sudah diserap ke bahasa Indonesia (server, internet, data, program). Kalau ragu apakah sebuah istilah sudah baku, cek KBBI daring. Kalau tetap ragu, miringkan.
- Kalimat atau kutipan utuh berbahasa asing diberi tanda kutip dan dimiringkan seluruhnya. Abstract berbahasa Inggris (kalau diminta) juga dimiringkan seluruhnya.
- Miring dibuat dengan format italic pada teks di Word, bukan dengan warna atau garis bawah. Di Daftar Pustaka, bagian yang dimiringkan mengikuti gaya sitasi (IEEE: nama jurnal atau prosiding; APA: judul jurnal atau buku).
- Singkatan dijelaskan lengkap saat pertama muncul, misal *Structured Query Language* (SQL).
- Tanpa em dash dan en dash (lihat aturan prioritas).

GAYA HUMANIZE (aturan konkret):
- Variasikan panjang kalimat: campur kalimat pendek dan kalimat majemuk. Jangan membuat semua kalimat berpola sama.
- Hindari pembuka klise seperti "Di era digital yang berkembang pesat" atau "Pada zaman modern ini".
- Setiap klaim harus terkait bahan saya. Kalau tidak ada dasarnya, hapus kalimatnya atau tandai dengan placeholder [KUTIPAN].
- Jangan menumpuk kata sambung penanda transisi ("selain itu", "oleh karena itu", "dengan demikian", "lebih lanjut") pada paragraf berurutan. Pakai transisi seperlunya, atau biarkan urutan gagasan yang membawa alur.
- Hindari daftar tiga hal yang seragam di setiap paragraf dan kalimat penutup yang hanya mengulang isi paragraf.
- Pakai istilah teknis yang tepat sesuai bahan, jangan diganti kata umum yang menggeser makna.

KETENTUAN UMUM LAPORAN:
Struktur isi default (disesuaikan jenis dokumen, dan ditimpa kalau saya memberi kerangka atau pedoman):
- Laporan praktikum: Pendahuluan (latar belakang, tujuan), Landasan Teori, Alat dan Bahan, Langkah Kerja atau Metodologi, Hasil dan Pembahasan, Kesimpulan, Daftar Pustaka (kalau dipakai), Lampiran.
- Makalah: Pendahuluan, Pembahasan, Penutup (kesimpulan dan saran), Daftar Pustaka.
- Laporan KP, proposal, atau tugas akhir: BAB I Pendahuluan, BAB II Landasan Teori atau Tinjauan Pustaka, BAB III Metodologi atau Pelaksanaan, BAB IV Hasil dan Pembahasan, BAB V Penutup, Daftar Pustaka, Lampiran.

Aturan isi:
- Tiap bab diawali paragraf pengantar sebelum sub judul pertama. Tidak ada sub judul tunggal (kalau ada 1.1 harus ada 1.2).
- Satu paragraf memuat satu gagasan pokok, minimal tiga kalimat. Hindari paragraf satu kalimat.
- Kesimpulan menjawab tujuan atau rumusan masalah secara berurutan dan tidak memuat data baru. Saran (kalau ada) realistis dan berkaitan dengan temuan.
- Abstrak (untuk dokumen besar): satu paragraf 150 sampai 250 kata, spasi tunggal, memuat latar singkat, tujuan, metode, dan hasil, ditutup 3 sampai 5 kata kunci.
- Kutipan langsung kurang dari 40 kata ditulis di dalam kalimat dengan tanda kutip. Kutipan 40 kata atau lebih dibuat blok menjorok, spasi tunggal, tanpa tanda kutip. Utamakan parafrase.
- Lampiran diberi huruf dan judul (Lampiran A, Lampiran B), dan dirujuk dari isi.

Aturan penulisan:
- Angka satu sampai sepuluh ditulis dengan huruf dalam kalimat ("tiga tahap"), angka 11 ke atas dengan angka. Kalimat tidak diawali angka. Angka yang disertai satuan, persen, atau data tetap ditulis angka (3 cm, 5%).
- Desimal memakai koma ("3,5") dan ribuan memakai titik ("12.500") di teks. Nilai dari output sistem, kode, atau data asli boleh dibiarkan apa adanya.
- Ada spasi antara angka dan satuan ("10 cm", "5 GB"). Persen ditulis tanpa spasi ("50%").
- Tanggal ditulis "1 Oktober 2026".
- Rujukan di teks memakai huruf kapital: "Gambar 2", "Tabel 3", "Kode 1", dan muncul sebelum objeknya.
- Tidak memakai tanda seru, emoji, singkatan tidak baku, atau bahasa percakapan. Tidak memakai bold atau huruf kapital semua untuk penekanan di dalam isi.
- Potongan kode program diberi keterangan "Kode X. Judul" di atas kodenya, memakai font Courier New 10 pt, spasi tunggal, latar abu sangat terang dengan bingkai tipis, dan tidak melewati margin. Ini satu-satunya pengecualian dari aturan Times New Roman. Kode lebih dari 30 baris dipindah ke Lampiran.

TABEL:
- Judul di atas tabel dengan format "Tabel X. Judul tabel" (X berurutan), rata kiri atau tengah secara konsisten.
- Sel background putih, teks hitam, border hitam solid, header bold. Tidak ada warna lain.
- Setiap tabel dirujuk di teks ("seperti pada Tabel 2") sebelum tabel muncul.
- Tabel tidak boleh melewati margin. Tabel yang panjang dilanjutkan ke halaman berikutnya dengan header berulang.

PLACEHOLDER (hanya empat jenis ini yang boleh ada di dokumen, semuanya dicetak BOLD supaya mudah dicari):
- Kalau referensi tidak dibutuhkan, placeholder [REF] dan [KUTIPAN] tidak dipakai sama sekali.
- Referensi yang tidak ada di bahan dan tidak ditemukan sumber terverifikasinya di langkah 2: [REF: butuh paper tentang topik spesifik]
- Pernyataan yang butuh sitasi tetapi tidak ada sumber terbaca yang mendukungnya: [KUTIPAN: butuh sumber untuk pernyataan yang perlu dikutip]
- Data yang tidak ada di bahan tetapi dibutuhkan: [DATA: butuh data tentang hal spesifik]
- Kotak screenshot atau foto asli (lihat langkah 5)
- Selain keempat jenis itu, dilarang ada catatan seperti "silakan isi bagian ini", "TBD", atau komentar pengarang.

REFERENSI DAN SITASI (hanya berlaku kalau dokumen butuh referensi, lihat langkah 2):
- Baca bahan saya dulu, gunakan referensi yang sudah ada dengan format yang benar. Referensi tambahan berasal dari paper yang ditemukan dan diverifikasi di langkah 2, disimpan di folder referensi/.
- Jangan mengarang judul, penulis, tahun, penerbit, atau DOI, dan jangan merangkum paper yang belum dibaca. DOI hanya ditulis kalau terlihat di halaman atau file sumber. Ragu valid atau tidak: jadikan placeholder.
- Gaya sitasi sesuai isian (default IEEE: nomor dalam kurung siku, berurutan sesuai kemunculan pertama di teks).
- Sisipkan sitasi secara natural di paragraf yang relevan (contoh: "Menurut [1], serangan SQL Injection terjadi ketika..."), tersebar merata, hanya untuk referensi yang benar-benar relevan.
- Buat bagian Daftar Pustaka di akhir dokumen. Setiap [n] di teks harus ada di Daftar Pustaka dan sebaliknya. Placeholder [REF] tetap dicatat sebagai entri placeholder di urutan yang sesuai.

=== OUTPUT AKHIR ===
- File .docx lengkap dan siap pakai, dikirim lewat present_files (di claude.ai) atau disimpan di folder workspace (di Antigravity), lengkap dengan path-nya. Sertakan file sumber diagram (.mmd atau .dot) dan PNG-nya sebagai file terpisah.
- Pesan penutup singkat, isinya hanya:
  1. Daftar diagram dan grafik yang sudah terpasang
  2. Kalau referensi dipakai: lokasi folder referensi/ dan daftar paper: mana yang terunduh, mana yang berbayar atau gagal unduh. Kalau langkah referensi dilewati, tulis satu kalimat alasannya
  2b. Daftar yang masih placeholder (screenshot asli, [REF], [KUTIPAN], [DATA])
  3. Section yang bahannya tipis dan cara Claude menanganinya
  4. Ringkasan hasil verifikasi, perbaikan yang dilakukan, dan kegagalan yang belum teratasi (kalau ada)
- Jangan menulis ulang isi dokumen di chat, dan jangan memakai em dash di pesan penutup.

Langsung kerjakan sekarang berdasarkan kebutuhan di atas.
````

---

## Cara pakai

1. Isi bagian `=== KEBUTUHAN DOKUMEN ===`. Field yang tidak relevan boleh dikosongkan.
2. Kalau dosen atau kampus punya pedoman format, tempel di field "Pedoman kampus/dosen". Aturan itu menimpa default.
3. Foto atau screenshot asli yang kamu berikan tidak akan diubah warnanya. Paper referensi akan diunduh ke folder `referensi/` di folder yang sedang dibuka. Yang tersisa untuk kamu: ganti kotak bingkai dengan screenshot atau foto asli, unduh manual paper berbayar, isi placeholder `[REF]`, `[KUTIPAN]`, `[DATA]` yang masih ada, lalu klik kanan daftar isi, gambar, dan tabel untuk Update Field.

---

*Last updated: September 2026 | Codejar, Fajar Geran Arifin*
