import docx
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = docx.Document('uts-blockchain-submission/Laporan_UTS_Blockchain_237006079_v3.docx')
body = doc._body._element

# Find t14 and remove it temporarily from its current position
t14 = doc.tables[14]
t14_elem = t14._element
t14_parent = t14_elem.getparent()

# Check what children exist at the end of v3
print("Last 5 children of v3:")
for i in range(len(body) - 5, len(body)):
    tag = body[i].tag.split('}')[-1]
    print(f"  {i}: <{tag}>")

