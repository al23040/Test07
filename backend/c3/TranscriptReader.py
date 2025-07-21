from typing import Optional

import pdfplumber
from io import BytesIO
import logging

logging.getLogger("pdfminer").setLevel(logging.ERROR)
import re
from . import utils
from typing import List, Tuple


class TranscriptReader:
    def __init__(self):
        self.term: Optional[dict] = None
        self.semester_offered: Optional[int] = None
        self.year_offered: Optional[int] = None
        self.user_id: Optional[int] = None

    def is_transcript(self, pdf_data: bytes) -> bool:
        keyword = "芝浦工業大学"
        with pdfplumber.open(BytesIO(pdf_data)) as pdf:
            page = pdf.pages[0]
            words = page.extract_words()
            full_text = page.extract_text()
            user_id_pattern = re.compile(r"AL(\d{5})")
            for word in words:
                if word['text'] == keyword and word['x0'] < 490 and word['top'] < 35:
                    term_pattern = re.compile(r"(20\d{2})年度\s*(前期|後期)")
                    found_terms: list[Tuple[int, str]] = []

                    for p in pdf.pages:
                        text = p.extract_text()
                        if text:
                            for match in term_pattern.finditer(text):
                                year = int(match.group(1))
                                semester = match.group(2)
                                found_terms.append((year, semester))

                    if found_terms:
                        def sort_key(term):
                            return term[0], 1 if term[1] == "前期" else 2

                        latest = max(found_terms, key=sort_key)
                        self.year_offered = latest[0]
                        self.semester_offered = 1 if latest[1] == "前期" else 2

                        #get_user_ud
                        um = user_id_pattern.search(full_text)
                        self.user_id = um.group(1)

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

                text = utils.text_replace(text)
                lines = text.split("\n")

            for line in lines:
                match = re.match(pattern, line)
                if match:
                    subject_name = match.group(1).strip()
                    code = match.group(2)
                    grade = match.group(5)
                    courses.append({
                        "subject_name": subject_name,
                        "code": code,
                        "grade": grade
                    })

            send_courses = utils.make_send_courses(courses)
            send_available_courses = utils.make_send_available_courses(self.semester_offered, self.year_offered, send_courses)
            make_send_credits_data = utils.make_send_credits_data(send_courses)
            utils.submit_available_courses(self.user_id, self.semester_offered, self.year_offered)

            return {
                "user_id": self.user_id,
                "courses": send_courses,
                "available_courses": send_available_courses,
                "credit_data": make_send_credits_data
            }