import pdfplumber

def loadpdf(path):
    with pdfplumber.open(path) as pdf:
        pages = pdf.pages
        full_text = ""

        for page in pages:
            text = page.extract_text() or ""
            if text:
                full_text += text + "\n"
        print(full_text)
        return full_text


# /Users/melissajin/Downloads/syllabus.pdf