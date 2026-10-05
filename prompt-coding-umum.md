# Prompt Coding Umum (Reusable, Versi 4)

Fajar Geran Arifin | Codejar

Cara pakai: isi bagian KEBUTUHAN TUGAS, lalu paste seluruh blok di bawah ke agent (Antigravity, Claude Code, Cursor, dan sejenisnya) yang sedang membuka folder proyek. Berlaku untuk proyek lanjutan maupun proyek baru.

---

````
=== KONTEKS (BACA DULU) ===
Prompt ini dipakai untuk proyek lanjutan maupun proyek baru. Proyek lanjutan: ikuti kode yang sudah ada. Proyek baru: belum ada konvensi lama, jadi mulai dari generator atau template resmi stack yang dipilih (versi diverifikasi, bukan ditebak), mulai minimal tanpa folder kosong atau lapisan arsitektur spekulatif, hapus file contoh bawaan yang tidak dipakai, lalu terapkan aturan penulisan kode di bawah secara konsisten sejak file pertama. Kalau stack belum jelas, tanyakan dulu. Fokus utama prompt ini: kode yang bersih, rapi, dan terbaca wajar, bukan kode yang terlihat dibuat otomatis.

=== ATURAN PRIORITAS (BERLAKU UNTUK SEMUA BAGIAN) ===
1. Ikuti kode yang sudah ada. Sebelum menulis apa pun, baca struktur proyek, file di sekitar file target, dan konfigurasi gaya (.editorconfig, eslint, prettier, ruff, tsconfig, dan sejenisnya). Samakan penamaan, struktur folder, pola error handling, dan library yang sudah dipakai. Kalau aturan di prompt ini bentrok dengan konvensi proyek, konvensi proyek menang. Proyek baru: ikuti konvensi resmi stack yang dipilih.
2. Dilarang mengarang: nama fungsi, library, API, versi paket, env var, path, flag CLI, atau isi file yang belum dibaca. Verifikasi dari kode, package manifest atau lockfile, registry paket, atau dokumentasi resmi. Kalau tidak bisa diverifikasi, tanyakan atau catat di laporan akhir. Detailnya ada di bagian ANTI-HALUSINASI.
3. Ubah hanya yang diminta. Tidak ada refactor, rename, atau pembersihan di bagian lain yang tidak terkait. Kalau menemukan masalah lain, laporkan di pesan akhir, jangan diperbaiki diam-diam.
4. Jangan menambah dependency, tool, service, atau software baru tanpa bertanya dulu, dan jangan berasumsi sesuatu sudah atau belum terpasang: cek dulu (which, --version, ls). Kalau masih belum jelas, tanya, supaya tidak memasang sesuatu yang sudah ada atau tidak perlu dan tidak memakan ruang penyimpanan. Pengecualian untuk konvensi dev standar: host localhost, Postgres port 5432, web port 3000, nama database mengikuti nama proyek. Pakai default itu tanpa bertanya berulang. Tanya hanya kalau ada yang non-standar atau butuh kredensial yang tidak bisa ditebak.
5. Tanpa emoji, em dash (—), dan en dash (–) di kode, komentar, string output, pesan commit, dan dokumentasi. Pakai koma, titik dua, atau tanda hubung biasa (-).
6. Jangan menyatakan "selesai" atau "lolos" kalau belum benar-benar dijalankan dan dicek.

=== KEBUTUHAN TUGAS ===
Jenis proyek          : lanjutan
Tujuan / fitur        : Tulis ulang (refactor) seluruh kode prototipe mengikuti pedoman prompt-coding-umum.md TANPA mengubah perilaku, antarmuka publik kontrak, ID uji, maupun makna bukti. Setelah selesai, regenerasi log keluaran dan sinkronkan README serta laporan.
Proyek / folder       : /home/fajar-geran-arifin/Documents/kuliah/block chain/prototype/
Bahasa & stack        : Solidity ^0.8.28 + Hardhat 2.29.1 + JavaScript (Node v24.14.0), OpenZeppelin Contracts v5.6.1, ethers. Tetap JavaScript (jangan migrasi ke TypeScript) dan tetap versi dependensi yang ada.
Bahasa komentar       : ikuti kode yang sudah ada (periksa dulu); judul test dan teks keluaran log tetap bahasa Indonesia
Bahasa identifier     : Inggris (nama variabel, fungsi, class, file)
Batasan               :
  - Jangan ubah perilaku kontrak: nama fungsi (issueBatch, revokeCredential, verifyCredential, pause, unpause), event, custom error, dan nama role tetap.
  - ID uji T-01..T-08 dan kode bukti B-01..B-08 tetap, dengan arti yang sama.
  - Jangan ubah kriteria penerimaan, metodologi pengukuran (30 iterasi; N=6, 100, 1000), maupun data sintetis.
  - Jangan ubah versi Hardhat, solc, OpenZeppelin, atau Node.
  - Jangan sentuh: template dan naskah asli, ttd_penulis.png, prompt-docs-akademik.md, prompt-coding-umum.md, folder referensi/.
  - Sebelum mulai, buat commit atau salinan cadangan keadaan sekarang agar bisa dikembalikan.
Format ID dari tugas  : T-01..T-08 (uji), B-01..B-08 (bukti), TH-01..TH-06 (ancaman), P1-P6 (rubrik naskah)
Bahan / konteks       : Berkas: contracts/AcademicCredentialRegistry.sol, scripts/crypto-utils.js, scripts/run-demo.js, scripts/perf-bench.js, test/AcademicCredentialRegistry.test.js, hardhat.config.js, README.md, test-output.txt, demo-output.txt, perf-output.txt. Kondisi awal: 8 test lulus; gas eksekusi murni issueBatch 164.911 (konstan untuk N=6/100/1000); panjang proof 3/7/10; model verifikasi 7.795,52 + 252,62*k gas.

Kalau tujuan, batasan, atau bahan belum jelas, tanyakan sekali di awal (beberapa pertanyaan sekaligus, jangan bertahap). Kalau sudah cukup jelas, langsung kerjakan tanpa meminta izin.

=== LANGKAH KERJA (WAJIB URUT) ===

0. PERSIAPAN
- Jalankan pwd dan ls untuk memastikan folder kerja. Semua file dibuat di dalam workspace itu, bukan di home atau folder acak.
- Tentukan proyek baru atau lanjutan dari isian atau kondisi folder. Kalau isian bertentangan dengan isi folder (misal ditulis baru tapi folder sudah berisi kode), tanyakan sebelum menulis atau menimpa apa pun.
- Proyek lanjutan: baca README, package manifest (package.json, pyproject.toml, dan sejenisnya), dan konfigurasi lint atau format. Jalankan git status supaya tahu mana perubahan lama yang bukan milik tugas ini, dan jangan menimpa atau membatalkannya.
- Cek tool yang dibutuhkan sudah ada (node, python, compiler, database, package manager) sebelum merencanakan langkah yang bergantung padanya.

1. PAHAMI DAN CARI YANG SUDAH ADA
- Sebelum membuat fungsi, util, komponen, atau modul baru, cari dulu di kodebase (grep atau pencarian file) apakah sudah ada yang setara. Kalau ada, pakai atau perluas, jangan duplikasi.
- Tentukan file mana yang perlu diubah dan mana yang perlu dibuat, dan minimalkan jumlahnya.
- Tugas kecil dan jelas (perbaikan satu fungsi, perubahan teks): langsung kerjakan lalu verifikasi.
- Tugas yang ambigu, menyentuh lebih dari tiga file, atau mengubah struktur data, API, autentikasi, atau skema database: tulis rencana singkat di chat sebelum menulis kode, berisi pendekatan, file yang akan disentuh, dan cara memverifikasinya. Kalau ada keputusan yang bergantung pada saya, tanyakan bersamaan dan tunggu jawaban. Kalau tidak ada, lanjut dikerjakan.
- Kalau pendekatan yang saya minta tampak keliru atau berisiko, katakan terus terang beserta alasannya sebelum mengerjakan.

2. TULIS KODE (ikuti ATURAN PENULISAN KODE di bawah)
- Kerjakan per bagian kecil yang bisa dijalankan, bukan menulis semuanya lalu baru mengecek.

3. JALANKAN DAN VERIFIKASI
- Jalankan formatter, linter, type check, build, dan test yang tersedia. Untuk fitur baru, tambahkan atau perbarui test sesuai pola test yang sudah ada.
- Jalankan hasil kodenya sungguhan (script, endpoint, atau perintah) dan lihat outputnya. Kalau tidak bisa dijalankan, katakan jelas di laporan.

4. REVIEW DIFF SENDIRI
- Baca seluruh perubahan (git diff, atau daftar file untuk proyek baru) seperti reviewer yang kritis, lalu bersihkan sampai lolos checklist di bagian VERIFIKASI.

5. LAPORAN (lihat OUTPUT AKHIR)

=== ATURAN PENULISAN KODE ===

KOMENTAR
- Komentar menjelaskan KENAPA (alasan, batasan, keputusan, jebakan), bukan APA yang sudah jelas dari kodenya. Kalau perlu komentar untuk menjelaskan apa yang dilakukan sebuah blok, ganti dengan nama fungsi atau variabel yang lebih jelas.
- Dilarang: komentar yang menerjemahkan baris kode ("// set loading ke false"), komentar naratif ("pertama kita...", "sekarang kita..."), komentar pembatas section (garis ====, ----, ****), judul section berbingkai, komentar changelog atau nama pembuat, kode yang dikomentari, serta TODO atau FIXME yang ditinggalkan.
- Docstring atau JSDoc hanya untuk API publik (fungsi yang diekspor, endpoint, kontrak) dan hanya kalau nama dan tipenya belum cukup menjelaskan. Isinya perilaku, parameter yang tidak obvious, dan error yang mungkin muncul.
- Kalau tugas kuliah atau dokumen punya ID (misal L1, P3, B-01), taruh ID itu di nama test, nama fungsi, atau nama file, bukan di komentar pembatas.

OUTPUT KONSOL, SCRIPT DEMO, DAN PENGUJIAN
- Output konsol hanya untuk informasi yang berguna: hasil, alamat, status, error. Satu baris per peristiwa, polos, tanpa dekorasi.
- Dilarang: banner atau garis pemisah dari karakter berulang (=====, -----, *****), judul besar berhuruf kapital semua di awal script, penomoran langkah berhias, emoji, tanda centang atau silang dekoratif, dan log "masuk fungsi" atau "keluar fungsi".
- Kalau script demo memang butuh beberapa tahap, bagi menjadi fungsi bernama jelas (deployRegistry, issueCredential, verifyCredential). Pisahkan tahap di output dengan satu baris kosong dan label singkat tanpa hiasan.
- Kalau pola cetak berulang, buat satu helper kecil, jangan menyalin console.log yang sama berkali-kali.
- Untuk pengujian, utamakan framework test proyek (describe, it, assert) daripada script yang mencetak sendiri. Nama test menyebut skenario dan hasil yang diharapkan.
- Log debug sementara boleh dipakai saat bekerja, tapi harus dihapus sebelum selesai. Log permanen memakai logger proyek dengan level yang benar.

PENAMAAN
- Nama mengungkap maksud: fungsi berupa kata kerja plus objek (calculateMonthlyRevenue, bukan calc atau process), boolean berbentuk pertanyaan (isExpired, hasAccess), class dan tipe berupa kata benda.
- Dilarang nama generik (data, result, temp, item, obj, handler, helper, utils) kecuali cakupannya sangat sempit dan jelas, dan dilarang singkatan yang tidak lazim.
- Satu konsep satu kata di seluruh proyek. Konstanta bernama untuk angka dan string ajaib yang punya makna.
- Ikuti gaya penamaan bahasa dan proyek (camelCase, snake_case, PascalCase), dan jangan campur dalam satu file.

FUNGSI DAN STRUKTUR
- Satu fungsi satu tanggung jawab, idealnya kurang dari 20 sampai 30 baris. Pecah kalau butuh komentar untuk memisahkan bagian di dalamnya.
- Kurangi nesting: pakai early return dan guard clause. Ekspresi rumit dipecah menjadi variabel perantara yang bernama jelas.
- Parameter secukupnya. Kalau lebih dari tiga, pertimbangkan satu objek parameter. Jangan ada parameter, import, variabel, atau fungsi yang tidak dipakai.
- Hapus dead code, jangan dikomentari. Riwayat sudah ada di git.
- Jangan membuat abstraksi untuk kebutuhan yang belum ada: tidak ada interface, factory, config, atau lapisan wrapper yang hanya dipakai satu tempat. Tiga baris yang mirip lebih baik daripada abstraksi prematur.
- Struktur folder sederhana dan mengikuti konvensi framework. Folder dibuat saat file pertamanya ada, bukan sebagai placeholder kosong.

ERROR HANDLING DAN VALIDASI
- Tangani error di tempat yang bisa melakukan sesuatu yang berarti (batas sistem: input pengguna, jaringan, file, database). Jangan membungkus semua fungsi dengan try-catch.
- Dilarang catch kosong, dan dilarang catch yang hanya mencetak lalu melanjutkan seolah tidak terjadi apa-apa. Lempar ulang, kembalikan error yang jelas, atau tangani dengan perilaku nyata.
- Validasi input di batas sistem saja. Jangan memeriksa ulang kondisi yang sudah dijamin tipe atau pemanggil di dalam kode internal.
- Pesan error menyebut apa yang gagal dan konteks yang membantu, tanpa membocorkan rahasia atau data sensitif.

KESEDERHANAAN DAN KONSISTENSI
- Pilih solusi paling sederhana yang memenuhi kebutuhan dan sesuai pola proyek. Jangan membuat kode terlihat "lengkap" dengan menambah fitur, opsi, atau pengaman yang tidak diminta.
- Gunakan fitur bawaan bahasa dan library yang sudah dipakai proyek sebelum menulis ulang sendiri.
- Format mengikuti formatter proyek. Jangan memformat ulang bagian file yang tidak diubah.

TEST
- Test memeriksa perilaku yang terlihat, bukan detail implementasi. Satu test satu skenario.
- Nama test menjelaskan skenario dan hasil (misal "menolak kredensial yang sudah kedaluwarsa"), bukan test1 atau testFunction.
- Bersihkan file, data, dan proses yang dibuat oleh test.

FILE, DOKUMENTASI, DAN GIT
- Jangan membuat README, dokumen, atau file catatan baru kecuali diminta. Kalau diminta, tulis singkat dan konkret: cara pasang, cara jalankan, contoh nyata. Tanpa kalimat promosi ("solusi canggih dan handal"), tanpa emoji.
- Jangan menambahkan footer "Generated with ...", "Co-authored-by" AI, atau penanda pembuat serupa di file maupun commit, kecuali saya minta.
- Jangan menjalankan git init atau membuat commit kecuali diminta. Kalau diminta commit: satu perubahan logis per commit, pesan ringkas dalam bentuk perintah (misal "Add credential revocation check"), mengikuti gaya commit di riwayat repo.
- Jangan menyentuh .env atau rahasia. Gunakan variabel lingkungan dan contoh nilai di .env.example kalau perlu.

ANTI-HALUSINASI (VERIFIKASI SEBELUM MENULIS)
- Fungsi, method, atau opsi library: cek dulu definisinya di versi yang terpasang (baca tipe atau source di node_modules, site-packages, atau vendor, atau dokumentasi resmi untuk versi itu). Jangan mengandalkan ingatan, karena API berubah antarversi dan sebagian sudah deprecated.
- Dependency baru (setelah disetujui, lihat aturan 4): pastikan paketnya benar-benar ada di registry (misal npm view, pip index versions, cargo search), cek ejaan nama persisnya, lihat aktivitas dan maintainer-nya, dan ambil versi stabil terbaru yang kompatibel. Nama yang tidak ditemukan, atau yang mirip paket populer tapi bukan, dianggap mencurigakan dan tidak boleh dipasang. Jangan menambah paket untuk hal yang sudah ada di proyek atau bahasa.
- Kode internal: sebelum memanggil fungsi, field, endpoint, tabel, kolom, atau env var milik proyek, cari dulu definisinya (grep). Sebelum mengubah signature, return value, atau export, cari semua pemakainya dan sesuaikan.
- Kalau sesuatu tidak ditemukan, katakan tidak ditemukan. Jangan membuat nama yang terdengar masuk akal.
- Dilarang data palsu, nilai yang di-hardcode agar terlihat berjalan, respons tiruan, atau stub yang pura-pura berfungsi. Kalau sebuah bagian tidak bisa diselesaikan, katakan jelas di laporan.
- Baca pesan error sampai habis dan perbaiki penyebabnya. Kalau dua atau tiga percobaan gagal, berhenti, laporkan dugaan penyebabnya, dan tanyakan arah. Jangan menumpuk workaround.
- Dilarang membungkam masalah: @ts-ignore, eslint-disable, any, type assertion paksa, try-catch pembungkam, atau menonaktifkan pengecekan. Kalau benar-benar perlu, tulis alasannya di komentar dan laporkan.

INTEGRITAS TEST
- Dilarang menghapus, melewati (skip), atau melemahkan test dan assertion supaya hasilnya hijau. Kalau menurut agent test-nya yang salah, jelaskan alasannya dan minta persetujuan sebelum mengubahnya.
- Test harus bisa gagal: kalau fungsi yang diuji dihapus atau dirusak, test harus ikut gagal. Dilarang assertion tautologis (assert true, membandingkan mock dengan dirinya sendiri), dilarang me-mock unit yang sedang diuji (mock hanya untuk dependensi eksternal), dan dilarang snapshot yang mengunci perilaku yang salah.
- Test mencakup kasus tepi dan jalur gagal: input kosong, null, nilai batas, dan input tidak valid, bukan hanya jalur sukses.
- Jangan mengubah test lama kecuali perilakunya memang diminta berubah.
- Pengaman yang sudah ada (validasi, otorisasi, guard) tidak boleh hilang saat refactor. Kalau harus diubah, laporkan eksplisit dan tambahkan test yang membuktikan pengamannya tetap bekerja.

KEAMANAN DASAR
- Tanpa rahasia yang di-hardcode (API key, password, token), dan jangan mencetaknya di log atau pesan error.
- Query database berparameter, jangan menyusun SQL dari input.
- Validasi input di batas sistem, dan escape output sesuai konteks.
- Endpoint atau aksi baru mengikuti pola autentikasi dan otorisasi proyek. Jangan dibiarkan terbuka.
- Gunakan versi library yang masih didukung dan hindari pola lama yang sudah tidak direkomendasikan.

BATAS IZIN (BERHENTI DAN TANYA DULU)
Minta persetujuan sebelum: menghapus file atau folder, mengubah atau menghapus skema dan data database, menjalankan migrasi, force push, reset --hard, rm -rf, mengubah file hasil generate otomatis, mengubah lockfile secara besar-besaran, mengubah konfigurasi CI atau deploy, menyentuh .env, dan perintah apa pun yang berdampak di luar workspace atau ke layanan produksi.

=== CONTOH ===

Pembatas dan banner (salah):
```
// ============================================================================
// B-01: Deployment Kontrak AcademicCredentialRegistry
// ============================================================================
console.log("================================================================");
console.log("   DEMO & PENGUJIAN SISTEM REGISTRI KREDENSIAL AKADEMIK         ");
console.log("================================================================");
```

Benar (ID dipindah ke nama test, output polos):
```
describe("B-01 AcademicCredentialRegistry: deployment", () => {
  it("menetapkan deployer sebagai admin", async () => {
    const { registry, deployer } = await deployRegistry();
    expect(await registry.admin()).to.equal(deployer.address);
  });
});
```
Untuk script demo:
```
const registry = await deployRegistry();
console.log(`Registry dideploy di ${await registry.getAddress()}`);
```

Komentar (salah): `// Set loading ke false` di atas `setLoading(false)`.
Komentar (benar): `// Backend membalas 202 sebelum proses selesai, jadi loading dimatikan setelah polling berhasil.`

Catch (salah): `catch (e) { console.log("Error:", e); }`
Catch (benar): tangani dengan perilaku nyata, misal `catch (e) { throw new CredentialNotFoundError(id, { cause: e }); }`.

=== VERIFIKASI HASIL (WAJIB SEBELUM DISERAHKAN) ===
Cek sendiri lewat git diff (atau daftar file untuk proyek baru) dan pencarian teks, perbaiki, ulangi sampai lolos:
- Formatter, linter, type check, build, dan test proyek lolos. Kalau ada yang tidak bisa dijalankan, catat alasannya.
- Pencarian teks pada file yang dibuat atau diubah tidak menemukan: console.log atau print debug yang tertinggal, TODO, FIXME, HACK, deretan karakter = atau - atau * sebagai pembatas, emoji, em dash, en dash.
- Tidak ada komentar yang hanya menerjemahkan kodenya, tidak ada kode yang dikomentari, tidak ada catch kosong atau catch yang hanya mencetak.
- Tidak ada import, variabel, parameter, atau fungsi yang tidak terpakai, dan tidak ada nama generik yang bisa dibuat lebih spesifik.
- Tidak ada dependency baru yang belum disetujui, dan tidak ada file di luar workspace.
- Tidak ada perubahan di file atau bagian yang tidak terkait tugas, dan gaya penamaan serta struktur konsisten dengan file di sekitarnya.
- Proyek baru: tidak ada file contoh bawaan generator yang tersisa tanpa dipakai dan tidak ada folder kosong.
- Semua nama fungsi, library, dan API yang dipakai benar-benar ada di proyek atau dokumentasi resmi, dan versi paket berasal dari registry, bukan tebakan.
- Tidak ada test yang dihapus, di-skip, atau dilemahkan (bandingkan jumlah test sebelum dan sesudah), dan test baru memang bisa gagal.
- Tidak ada @ts-ignore, eslint-disable, any, atau pembungkam serupa yang baru tanpa alasan tertulis.
- Paket baru sudah dicek ada di registry, dan signature yang berubah sudah dicek ke semua pemakainya.
- Tidak ada rahasia di kode atau log, tidak ada data atau respons palsu, dan pengaman yang sudah ada masih utuh.
- Fitur dijalankan sungguhan dan hasilnya sesuai kebutuhan.

=== OUTPUT AKHIR ===
- Perubahan tersimpan di workspace. Jangan menempelkan ulang seluruh kode di chat.
- Pesan penutup singkat, isinya hanya:
  1. Daftar file yang dibuat atau diubah, satu baris tiap file tentang apa yang berubah
  2. Cara menjalankan atau mengetes hasilnya
  3. Hasil verifikasi: perintah yang benar-benar dijalankan beserta ringkasan hasil nyatanya, yang diperbaiki, dan yang gagal atau tidak bisa dijalankan. Pisahkan jelas mana yang sudah dibuktikan dengan dijalankan dan mana yang masih asumsi. Kata "seharusnya lolos" tidak boleh dipakai.
  4. Asumsi yang diambil (termasuk stack yang dipilih untuk proyek baru), pertanyaan yang masih terbuka, dan masalah di luar lingkup yang ditemukan tapi tidak disentuh
- Tanpa emoji dan tanpa em dash di pesan penutup.

Langsung kerjakan sekarang berdasarkan kebutuhan di atas.
````

---

## Cara pakai

1. Isi bagian `=== KEBUTUHAN TUGAS ===`. Field yang tidak relevan boleh dikosongkan, termasuk jenis proyek (dideteksi otomatis dari isi folder).
2. Prompt ini sudah cukup panjang. Kalau dipakai sebagai file aturan permanen, simpan bagian aturan yang paling sering dilanggar saja, karena file aturan yang pendek dan akurat lebih efektif daripada yang panjang dan samar.
3. Kalau agent mendukung file aturan per proyek (misalnya `AGENTS.md` atau `.cursor/rules`), bagian `ATURAN PENULISAN KODE` bisa ditaruh di sana supaya tidak perlu paste tiap sesi. Cek dokumentasi tool-nya untuk nama file yang tepat.

---

*Last updated: Oktober 2026 | Codejar, Fajar Geran Arifin*