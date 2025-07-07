

from flask import Flask, request, jsonify
from datetime import datetime
from typing import Any, Dict
from .models import get_session

from c3.TranscriptReader import TranscriptReader
from c3.SaveCourseData import SaveCourseData

class C3API:
    def __init__(self, app: Flask):
        self.app = app
        self._register_routes()

    def _register_routes(self):
        @self.app.route('/api/c3/upload-pdf', methods=['POST'])
        def upload_pdf():
            file = request.files.get('file')
            pdf_bytes = file.read()
            tr = TranscriptReader()
            if tr.is_transcript(pdf_bytes) == False:
                return jsonify({'error': 'Invalid file.'}), 400

            send_data = tr.get_course_data(pdf_bytes)
            return jsonify(send_data), 200

        @self.app.route('/api/c3/courses/submit', methods=['POST'])
        def submit_courses():
            data = request.get_json()
            courses = data.get('courses', [])
            user_id = data.get('user_id')
            print(user_id, flush=True)
            session = get_session()
            scd = SaveCourseData(session)
            scd.submit_course_data(courses, user_id)
            return jsonify({"message": "Courses saved successfully"}), 201

def register_c3_api(app: Flask) -> C3API:
    """
    Register C3 API endpoints with Flask app

    Args:
        app: Flask application instance

    Returns:
        C3API instance
    """
    return C3API(app)







