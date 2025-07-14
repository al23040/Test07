from flask import Flask, request, jsonify
from c3.utils import get_completed_courses, get_available_courses

import requests


class C7API:
    def __init__(self, app: Flask):
        self.app = app
        self._register_routes()

    def _register_routes(self):
        @self.app.route('/api/c7/user_conditions/<int:user_id>', methods=['POST'])
        #def get_user_conditions():
        def get_user_conditions(user_id):
            data = request.get_json()
            #user_id = int(data['user_id'])
            conditions = {
                "min_units": data.get("min_units"),
                "max_units": data.get("max_units"),
                "preferences": data.get("preferences"),
                "avoid_first_period": data.get("avoid_first_period"),
                "preferred_time_slots": data.get("preferred_time_slots"),
                "preferred_categories": data.get("preferred_categories"),
                "preferred_days": data.get("preferred_days"),
                "avoided_days": data.get("avoided_days")
            }
            completed_courses = get_completed_courses(user_id)
            all_courses = get_available_courses(user_id)

            send_data = {
                "user_id": user_id,
                "conditions": conditions,
                "completed_courses": completed_courses,
                "all_courses": all_courses
            }
            response = requests.post('http://localhost:5000/api/c4/four-year-patterns', json=send_data)

            return jsonify(response.json()), 200

def register_c7_api(app: Flask) -> C7API:
    return C7API(app)