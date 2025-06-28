import TranscriptReader

print("test!!")
pdf_path = "./Receipt.pdf"
def pdf_to_bytes(pdf_path):
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    return pdf_bytes

data = pdf_to_bytes(pdf_path)
tr = TranscriptReader.TranscriptReader()
print(tr.is_transcript(data))

print(tr.get_course_data(data))


