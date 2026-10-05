# Panduan Pengumpulan UTS Blockchain & OBE

- **Nama:** Fajar Geran Arifin
- **NPM:** 237006079

## Struktur Folder
- `237006079_Fajar_Geran_Arifin_UTS_Blockchain_OBE.pdf`: Laporan naskah akhir (v7.5).
- `sumber/`: Naskah dokumen sumber (.docx).
- `pendukung/`: Kode smart contract, skrip pengujian, diagram, alat verifikasi, dan log.
- `pendukung_237006079.zip`: Arsip zip seluruh folder pendukung.

## Perintah Reproduksi Prototipe
Masuk ke direktori `pendukung/prototype/`:
```bash
npm install
npx hardhat compile
npm test
npm run demo
npm run bench
```

## Pengungkapan Penggunaan Alat Bantu Digital/AI

**Alat:** ChatGPT (OpenAI), Claude (Anthropic), Cursor, dan Google Antigravity (agen pemrograman berbantuan AI); Node.js v24.14.0 dan Solidity ^0.8.28; Hardhat v2.29.1 (kompilasi, pengujian, dan simulasi EVM lokal); OpenZeppelin Contracts v5.6.1 (AccessControl, Pausable, MerkleProof); merkletreejs v0.6.0 (pembentukan pohon Merkle dan Merkle proof off-chain); keccak256 v1.0.6 (hashing daun Merkle); Python 3.12.3 dengan python-docx v1.2.0 (otomasi penyusunan dokumen) dan skrip audit; Graphviz v2.43.0 (diagram arsitektur, alur transaksi, dan pohon Merkle); LibreOffice v24.2.7.2 (kompilasi DOCX ke PDF); poppler-utils (pdftotext) v24.02.0 (ekstraksi teks PDF untuk audit); exiftool v12.76 (metadata PDF); serta GitHub. Rujukan standar dan konsep utama: W3C Verifiable Credentials Data Model v2.0, W3C Bitstring Status List v1.0, RFC 8785 (JCS), Merkle tree, Keccak-256, NIST FIPS 202, dan EIP-2028.

**Dipakai untuk:** ChatGPT untuk diskusi awal menjajaki pemahaman topik; Claude untuk membantu menganalisis tugas sehingga saya lebih memahami konsep dan permasalahannya; Cursor dan Antigravity untuk membantu eksekusi kode, yaitu menulis, menjalankan, dan menguji prototipe AcademicCredentialRegistry.sol, skrip pengujian dan benchmark, serta skrip build dokumen laporan.

**Tidak dipakai untuk:** Bagian A (ujian kasus di kelas).

**Verifikasi:** Hasil pada Tabel 10 (unit test T-01 s.d. T-08) berasal dari eksekusi nyata AcademicCredentialRegistry.test.js dengan keluaran test-output.txt, dan dapat diulang dengan perintah cd prototype && npx hardhat test. Angka pada Lampiran E (30 run terukur) dan Lampiran F (isolasi selisih gas) berasal dari perf-output.txt dan exp_b06_output.txt. Kesesuaian angka dan hash pada laporan dengan berkas log diperiksa dengan verify_report.py dan hash_check.py. Berkas PDF primer rujukan standar tersimpan di folder referensi/ beserta checksum SHA-256 pada INDEX.md.

**Tanggung jawab:** Isi laporan, keputusan rancangan, dan kesimpulan menjadi tanggung jawab saya setelah ditinjau dan disesuaikan.
