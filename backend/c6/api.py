from flask import Flask, request, jsonify
from .CoursesInfo import get_user_courses
class C6API:

    def __init__(self, app: Flask):
        self.app = app 
        self._register_routes()

    def _register_routes(self):
        @self.app.route('/api/c6/user_grades', methods = ['POST'])
        def user_grades():
            try:
                data = request.get_json()
                user_id = data.get('user_id')
                if not user_id:
                    return jsonify({'error': "user_idがありません"}), 400
                
                course_data = get_user_courses(user_id)
                if not course_data:
                    return jsonify({'error': "不正な学籍番号です。"}), 400
                return jsonify(course_data), 200
            
            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                }), 500
            
def register_c6_api(app: Flask) -> C6API:
    return C6API(app)