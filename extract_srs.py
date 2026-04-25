from docx import Document

doc_path = r"C:\Users\keert\OneDrive - Amrita vishwa vidyapeetham\Sem 6 Proj\Software Engineering\SRS\final\SRS Final.docx"

doc = Document(doc_path)

for para in doc.paragraphs:
    print(para.text)