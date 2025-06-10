import pdfplumber
from io import BytesIO
import logging
logging.getLogger("pdfminer").setLevel(logging.ERROR)
import re
import utils

class TranscriptReader:
    def is_transcript(self, pdf_data: bytes) -> bool:
        keyword = "芝浦工業大学"
        with pdfplumber.open(BytesIO(pdf_data)) as pdf:
            page = pdf.pages[0]
            words = page.extract_words()
            for word in words:
                if word['text'] == keyword and word['x0'] < 490 and word['top'] < 35:
                    return True
        return False
    
    def get_course_data(self, pdf_data: bytes):
        courses = []
        pattern = re.compile(r'(.+?)\s+([A-Z0-9]{7,})\s+(\d+)\s+(\d)\s+([SABCDGF#])\s+(\d)\s+\d{2}')

        with pdfplumber.open(BytesIO(pdf_data)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue

                utils.text_replace(text)
                lines = text.split("\n")

            for line in lines:
                match = re.match(pattern, line)
                if match:
                    subject_name = match.group(1).strip()
                    code = match.group(2)
                    grade = match.group(5)
                    courses.append({
                        "科目名": subject_name,
                        "科目コード": code,
                        "成績": grade
                    })

            utils.make_send_data(courses)



            return  courses
