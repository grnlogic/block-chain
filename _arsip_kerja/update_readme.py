import re

with open('prototype/README.md', 'r') as f:
    content = f.read()

# Replace old hashes
content = content.replace('0x518b13a4ce348fce61776abcda2631f404701d6d87ece2e2b02bbf24ee270f23', '0x6879c11e179813273132ad5cb23b58bd713d41c6535c41fec7f54ca4f3a70647')
content = content.replace('0x50119ec3abc119e162a13042da3189e520df8c72c2975ba4746a18493a8d7b53', '0xaf555924fd6db1366a269faabd6dcc2efedce4a7177a9674c8bee194bf777dc9')
content = content.replace('0x88f262e31bff2ae06085297af770cd83e0bcfc871e54d6ff7ba0d5cf48191516', '0xc4d1a22493f0f84e3416456ec240f9a0ad2e1a1a976e8ae39fb84a7d8eadbd45')
content = content.replace('32.307 unit', '32.339 unit')
content = content.replace('2.760 gas', '2.772 gas')
content = content.replace('8.547 unit', '8.567 unit')
content = content.replace('0x71702fdc749f2e62e547924b18e3ede59c6095c908219fbcbac2096b8212c5b4', '0x5f7c0830433cffc9c496b95bf191b8af442891db243c0d144f189b29428ee96d')

# Replace W3C VC status to Recommendation 15 Mei 2025
content = content.replace('W3C Proposed Recommendation, Sep. 2024', 'W3C Recommendation, 15 Mei 2025')
content = content.replace('W3C Candidate Recommendation, 2024', 'W3C Recommendation, 15 Mei 2025')

# Replace Merkle citation in Acceptance criteria table
content = content.replace(
    'Konsep Kompresi Merkle Tree (Merkle, 1989, "A Certified Digital Signature", CRYPTO \'89, LNCS 435, Springer-Verlag) & Pengukuran Empiris EVM: Merkle (1989) hanya mendukung konsep kompresi',
    'Konsep Kompresi Pohon Autentikasi (Merkle, U.S. Patent 4,309,569, 1982) & Pengukuran Empiris EVM: Paten Merkle (1982) memformulasikan tree authentication dan kompresi'
)

# Replace Nielsen citation in Acceptance criteria table
content = content.replace(
    'Konsisten dengan pedoman umum batas responsivitas interaksi manusia-komputer (Nielsen, 1993, *Usability Engineering*, Academic Press):',
    'Konsisten dengan pedoman batas responsivitas interaksi manusia-komputer (Nielsen, 1993, "Response Times: The 3 Important Limits", Nielsen Norman Group):'
)

# Update Section Transparansi
old_transp_pat = re.compile(r'### Transparansi Status Penelusuran Sumber Referensi[\s\S]*?(?=---\n\n## 9\. Indeks Bukti)')

new_transp = '''### Transparansi Status Penelusuran dan Verifikasi Sumber Referensi
Sesuai prinsip integritas akademik dan tahapan verifikasi referensi, seluruh 12 dokumen sumber resmi yang dirujuk telah diunduh/disnapshot langsung ke folder `uts-blockchain-submission/referensi/`, diverifikasi integritasnya melalui *checksum* SHA-256, dan dicocokkan nomor halaman/bagian pembukti klaimnya pada berkas `INDEX.md`:
1. **W3C Verifiable Credentials Data Model v2.0 (15 Mei 2025):** Snapshot web resmi (147 hal., SHA-256: `bdd0ec67...`). Bagian 4.10 (*Status*, hal. 40–42) memvalidasi skema `credentialStatus`.
2. **Dokumentasi Resmi Ethereum Developer JSON-RPC API (2024):** Snapshot web resmi (54 hal., SHA-256: `48e8adf7...`). Hal. 28–29 memvalidasi klausul eksekusi pesan lokal tanpa transaksi dan bebas gas (*eth_call consumes zero gas*).
3. **OpenZeppelin Contracts v5.x Documentation (AccessControl & Pausable):** Snapshot web resmi (75 hal. + 237 hal., SHA-256: `54ae0f71...` & `d830c957...`). Memvalidasi RBAC (`AccessControlUnauthorizedAccount`) dan jeda darurat (`whenNotPaused`, `EnforcedPause`).
4. **Paten Ralph C. Merkle (U.S. Patent 4,309,569, 1982):** PDF paten resmi USPTO / Google Patents (6 hal., SHA-256: `cf1fc4d7...`). Kolom 3–4 memvalidasi formulasi pohon autentikasi biner dan bukti jalur Merkle berukuran $\\lceil \\log_2 n \\rceil$.
5. **Saltzer & Schroeder (1975, Edisi Daring Resmi MIT):** Snapshot naskah penulis di domain MIT (`web.mit.edu/Saltzer`, 16 hal., SHA-256: `dec33ed1...`). Bagian I.A.1.f (hal. 5) memvalidasi prinsip *Least Privilege*, *Separation of Privilege*, dan *Fail-Safe Defaults*.
6. **Bertoni et al. (The Keccak reference v3.0, 2011):** PDF naskah resmi dari keccak.team (70 hal., SHA-256: `834e74ed...`). Bagian 1.1.2 Definisi 1 (hal. 7) memvalidasi aturan *multi-rate padding* `pad10*1`.
7. **Jakob Nielsen (Response Times: The 3 Important Limits, NN/g 1993):** Snapshot artikel resmi Nielsen Norman Group (7 hal., SHA-256: `bccebce3...`). Memvalidasi petikan Bab 5 *Usability Engineering* untuk ambang batas persepsi 1,0 detik alur kognitif.
8. **W3C Bitstring Status List v1.0 (15 Mei 2025):** Snapshot web resmi W3C (34 hal., SHA-256: `9ed1fb29...`). Memvalidasi pembanding arsitektur kompresi status pencabutan kredensial.
9. **IETF RFC 8785 (JSON Canonicalization Scheme, 2020):** PDF resmi RFC Editor (20 hal., SHA-256: `1796e120...`). Bagian 3.2.3 (hal. 6–7) memvalidasi pengurutan kunci leksikografis UTF-16 code units.
10. **UU RI No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP):** PDF naskah resmi Lembaran Negara dari JDIH BPK (51 hal., SHA-256: `ed952dea...`). Pasal 8 (hal. 6) memvalidasi hak subjek data untuk menghapus/memusnahkan data pribadi (*Right to Erasure*), serta Pasal 43 & 44 (hal. 18) memvalidasi kewajiban pengendali data.
11. **EIP-2028: Transaction Data Gas Cost Reduction (2019):** Snapshot spesifikasi Ethereum (6 hal., SHA-256: `88ed6756...`). Hal. 1–2 memvalidasi pengurangan biaya calldata non-nol menjadi 16 gas/byte.
12. **NIST FIPS 202 (2015):** PDF naskah resmi NIST (38 hal., SHA-256: `15926078...`). Bagian 6.1 (hal. 28) memvalidasi penambahan domain separator 2-bit `01` pada standar SHA3-256.

'''

content = old_transp_pat.sub(lambda m: new_transp, content)

# Update UU PDP mentions
content = content.replace('hak penghapusan data (Right to Erasure, Pasal 43 UU PDP)', 'hak penghapusan data pribadi (Right to Erasure, Pasal 8 dan Pasal 43 UU PDP No. 27/2022)')

with open('prototype/README.md', 'w') as f:
    f.write(content)

print('prototype/README.md successfully updated and synchronized.')
