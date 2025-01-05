from PyPDF2 import PdfReader, PdfWriter

input_pdf = "C:/Users/nites/Downloads/regalia.pdf"
output_pdf = "C:/Users/nites/Downloads/unprotected.pdf"
password = ""

reader = PdfReader(input_pdf)
reader.decrypt(password)

writer = PdfWriter()
for page in reader.pages:


    writer.add_page(page)

with open(output_pdf, "wb") as f:
    writer.write(f)

print(f"Unprotected PDF saved as {output_pdf}")
