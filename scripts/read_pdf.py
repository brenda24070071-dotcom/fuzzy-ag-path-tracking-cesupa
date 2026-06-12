import PyPDF2
import sys

pdf_path = sys.argv[1]
reader = PyPDF2.PdfReader(pdf_path)
text = ''
for page in reader.pages:
    text += page.extract_text() or ''

# Write full text
with open('pdf_output_full.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Done. Total chars: {len(text)}")
