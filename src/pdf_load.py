import pdfplumber

def loadpdf():
    path = input("Enter PDF Path: ")

    with pdfplumber.open(path) as pdf:
        pages = pdf.pages
        full_text = ""

        for page in pages:
            text = page.extract_text() or ""
            if text:
                full_text += text + "\n"
        
        with open("/Users/melissajin/syllabus-agent/data/syllabus.txt", "w", encoding="utf-8") as f:
                f.write(full_text)
