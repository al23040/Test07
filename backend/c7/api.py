from flask import Flask, request, jsonify
from RequireInfo import RequireInfo
from c4.condition_processor import ConditionProcessor, UserConditions
from c4.enums import CourseCategory, DayOfWeek

app = Flask(__name__)

# メモリ上に保存する辞書（テスト用）
all_user_conditions = {}
condition_processor = ConditionProcessor()
require_info = RequireInfo(condition_processor, all_user_conditions)

@app.route('/user_conditions', methods=['POST'])
def receive_user_conditions():
    try:
        form_data = request.json
        if not form_data:
            return jsonify({"error": "リクエストボディが空です"}), 400

        user_conditions = require_info.create_user_conditions_from_form(form_data)
        saved = require_info.save_user_conditions(user_conditions.user_id, user_conditions)
        if not saved:
            return jsonify({"error": "条件の保存に失敗しました"}), 400

        return jsonify({"status": "ok", "user_id": user_conditions.user_id})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user_conditions/<int:user_id>', methods=['GET'])
def get_user_conditions(user_id):
    user_conditions = require_info.get_user_conditions(user_id)
    if user_conditions is None:
        return jsonify({"error": f"学籍番号 {user_id} の条件は存在しません"}), 404

    result = {
        "user_id": user_conditions.user_id,
        "min_units": user_conditions.min_units,
        "max_units": user_conditions.max_units,
        "preferences": user_conditions.preferences,
        "avoid_first_period": user_conditions.avoid_first_period,
        "preferred_time_slots": user_conditions.preferred_time_slots,
        "preferred_categories": [cat.value for cat in user_conditions.preferred_categories],
        "preferred_days": [day.value for day in user_conditions.preferred_days],
        "avoided_days": [day.value for day in user_conditions.avoided_days]
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)