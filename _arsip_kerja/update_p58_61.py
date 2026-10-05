with open('build_verified_v4.py') as f:
    code = f.read()

target = """# 2. Update Paragraph 60
p60 = doc.paragraphs[60]
p60.text = (
    "• 2. Slope Model: Kemiringan (Slope) ≈ 251,3 gas/sibling: Merefleksikan perkiraan kasar opcode loop "
    "MerkleProof.verify [3], [4] per iterasi: KECCAK256 [6] (64 byte input: 42 gas) + MLOAD/MSTORE (6 gas) + "
    "percabangan & stack LT/JUMP/DUP/SWAP (~15 gas). Batas kelayakan ditetapkan <= 350 gas/sibling "
    "(memberikan safety margin ~39% di atas hasil ukur 251,3 gas/sibling)."
)
for r in p60.runs:
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10)"""

replacement = """# 2. Update Paragraphs 58, 59, 60, 61 (Model Regresi Linier)
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
    r.font.size = Pt(10)"""

assert target in code, "target not found"
code = code.replace(target, replacement, 1)

with open('build_verified_v4.py', 'w') as f:
    f.write(code)

print("build_verified_v4.py updated successfully.")
