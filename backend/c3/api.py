

from flask import Flask, request, jsonify
from datetime import datetime
from typing import Any, Dict
from models import get_session

from backend.c3.TranscriptReader import TranscriptReader
from backend.c3.SaveCourseData import SaveCourseData


class C3API:
    def __init__(self, app: Flask):
        self.app = app
        self._register_routes()

    def _register_routes(self):
        @self.app.route('/api/c3/upload-pdf', methods=['POST'])
        def upload_pdf():
            file = request.files.get('file')
            tr = TranscriptReader()
            if tr.is_transcript(file) == False:
                return jsonify({'error': 'Invalid file.'}), 400

            send_data = tr.get_course_data(file)
            return jsonify(send_data), 200

        @self.app.route('/api/c3/courses/submit', methods=['GET'])
        def submit_courses():
            courses = request.get_json()
            session = get_session()
            scd = SaveCourseData(session)
            scd.submit_course_data(courses, 1)
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







