import fitz
import os

def convert_pdf_to_text(pdf_file, output_dir):
    with fitz.open(pdf_file) as doc:
        text = ""
        for page in doc:
            text += page.get_text()

    output_file = os.path.join(output_dir, os.path.basename(pdf_file).replace('.pdf', '.txt'))
    with open(output_file, 'w') as f:
        f.write(text)

if __name__ == "__main__":
    leech_dir = "/leech"
    pages_dir = "/pages"
    
    for filename in os.listdir(leech_dir):
        if filename.endswith(".pdf"):
            convert_pdf_to_text(os.path.join(leech_dir, filename), pages_dir)

