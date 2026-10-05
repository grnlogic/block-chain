with open('build_verified_v4.py') as f:
    code = f.read()

# Replace comment "# --- Lampiran B: Keluaran Eksekusi B-05 ---" with page break before Lampiran B
old_part = "# --- Lampiran B: Keluaran Eksekusi B-05 ---"
new_part = """# --- Page Break before Lampiran B ---
p_pb_b = doc.add_paragraph()
p_pb_b.paragraph_format.space_before = Pt(0)
p_pb_b.paragraph_format.space_after = Pt(0)
p_pb_b.add_run().add_break(docx.enum.text.WD_BREAK.PAGE)
p_pb_b._p.getparent().remove(p_pb_b._p)
add_elem_before_sectPr(p_pb_b)

# --- Lampiran B: Keluaran Eksekusi B-05 ---"""

assert old_part in code
code = code.replace(old_part, new_part, 1)

with open('build_verified_v4.py', 'w') as f:
    f.write(code)

