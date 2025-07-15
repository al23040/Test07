from flask import Flask, request, jsonify
from c3.utils import get_completed_courses, get_all_courses, get_available_courses
import json

import requests


class C7API:
    def __init__(self, app: Flask):
        self.app = app
        self._register_routes()

    def _register_routes(self):
        @self.app.route('/api/c7/user_conditions/<int:user_id>', methods=['POST'])
        def get_user_conditions(user_id):
            data = request.get_json()

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
            all_courses = get_all_courses(user_id)

            send_data = {
                "user_id": user_id,
                "conditions": conditions,
                "completed_courses": completed_courses,
                "all_courses": all_courses
            }

        # 4年パターン取得のためC4 APIを呼ぶ
            c4_response = requests.post('http://localhost:5000/api/c4/four-year-patterns', json=send_data)
            if c4_response.status_code != 200:
                return jsonify({"status": "error", "error": "4年パターンの取得に失敗しました"}), 500

            four_year_patterns = c4_response.json()

    # 必要ならここでユーザー条件の保存処理も行う（省略）

            return jsonify({
                "status": "ok",
                "message": "条件を受け取りました",
                "four_year_patterns": four_year_patterns
            }), 200

        @self.app.route('/api/c7/user_courses/<int:user_id>', methods=['POST'])
        def get_user_courses(user_id):
            data = request.get_json()
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
            available_courses = get_available_courses(user_id)

            send_data = {
                "user_id": user_id,
                "conditions": conditions,
                "completed_courses": completed_courses,
                "available_courses": available_courses
            }

            return jsonify(send_data), 200



def register_c7_api(app: Flask) -> C7API:
    return C7API(app)