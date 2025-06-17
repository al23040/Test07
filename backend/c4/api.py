from flask import Flask, request, jsonify
from typing import List, Dict, Optional, Any
import json
from datetime import datetime

from .condition_processor import ConditionProcessor, UserConditions, Course, CourseCategory, RequirementType
from .condition_parser import ConditionParser
from .registration_pattern_calculator import RegistrationPatternCalculator


class C4API:
    """
    C4 条件処理部 (Condition Processing Component) API Interface
    Handles HTTP requests for course recommendation and pattern generation
    """

    def __init__(self, app: Flask):
        self.app = app
        self.condition_processor = ConditionProcessor()
        self.condition_parser = ConditionParser()
        self.pattern_calculator = RegistrationPatternCalculator()

        # Register API routes
        self._register_routes()

    def _register_routes(self):
        """Register API endpoints for C4 functionality"""

        @self.app.route('/api/c4/current-semester-recommendation', methods=['POST'])
        def get_current_semester_recommendation():
            """
            今学期のおすすめ履修登録を表示
            API endpoint for current semester course recommendations
            """
            try:
                data = request.get_json()

                # Validate required fields
                required_fields = ['user_id', 'conditions', 'completed_courses', 'available_courses']
                for field in required_fields:
                    if field not in data:
                        return jsonify({'error': f'Missing required field: {field}'}), 400

                # Parse input data
                user_id = data['user_id']
                conditions_dict = data['conditions']
                completed_courses = self._parse_courses(data['completed_courses'])
                available_courses = self._parse_courses(data['available_courses'])

                # Convert conditions to UserConditions object
                user_conditions = self._parse_user_conditions(conditions_dict)

                # Generate current semester recommendations
                recommendations = self.condition_processor.process_current_semester_recommendation(
                    user_id,
                    user_conditions,
                    completed_courses,
                    available_courses
                )

                # Convert to JSON response
                response_data = {
                    'status': 'success',
                    'recommendations': [self._pattern_to_dict(pattern) for pattern in recommendations],
                    'timestamp': datetime.now().isoformat()
                }

                return jsonify(response_data), 200

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500

        @self.app.route('/api/c4/four-year-patterns', methods=['POST'])
        def get_four_year_patterns():
            """
            4年生までの履修登録パターンを表示
            API endpoint for 4-year course registration patterns
            """
            try:
                data = request.get_json()

                # Validate required fields
                required_fields = ['user_id', 'conditions', 'completed_courses', 'all_courses']
                for field in required_fields:
                    if field not in data:
                        return jsonify({'error': f'Missing required field: {field}'}), 400

                # Parse input data
                user_id = data['user_id']
                conditions_dict = data['conditions']
                completed_courses = self._parse_courses(data['completed_courses'])
                all_courses = self._parse_courses(data['all_courses'])

                # Convert conditions to UserConditions object
                user_conditions = self._parse_user_conditions(conditions_dict)

                # Generate 4-year patterns
                patterns = self.condition_processor.generate_four_year_patterns(
                    user_id,
                    user_conditions,
                    completed_courses,
                    all_courses
                )

                # Convert to JSON response
                response_data = {
                    'status': 'success',
                    'patterns': [self._plan_pattern_to_dict(pattern) for pattern in patterns],
                    'timestamp': datetime.now().isoformat()
                }

                return jsonify(response_data), 200

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500

        @self.app.route('/api/c4/condition-based-recommendation', methods=['POST'])
        def get_condition_based_recommendation():
            """
            条件に基づく推奨パターン
            API endpoint for condition-based course pattern recommendations
            """
            try:
                data = request.get_json()

                # Validate required fields
                required_fields = ['user_id', 'conditions', 'completed_courses', 'available_courses']
                for field in required_fields:
                    if field not in data:
                        return jsonify({'error': f'Missing required field: {field}'}), 400

                # Parse input data
                user_id = data['user_id']
                conditions = data['conditions']
                completed_courses = self._parse_courses(data['completed_courses'])
                available_courses = self._parse_courses(data['available_courses'])
                necessary_subjects = data.get('necessary_subjects', {})

                # Use condition parser to process complex conditions
                recommendations = self.condition_parser.parse_and_execute(
                    conditions,
                    user_id,
                    completed_courses,
                    available_courses,
                    necessary_subjects
                )

                # Convert to JSON response
                response_data = {
                    'status': 'success',
                    'recommendations': [self._pattern_to_dict(pattern) for pattern in recommendations],
                    'condition_summary': self._summarize_conditions(conditions),
                    'timestamp': datetime.now().isoformat()
                }

                return jsonify(response_data), 200

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500

        @self.app.route('/api/c4/avoid-first-period', methods=['POST'])
        def get_avoid_first_period_pattern():
            """
            1限を避ける履修パターン
            Specific API for avoiding first-period classes (as mentioned in specifications)
            """
            try:
                data = request.get_json()

                # Parse input data
                user_id = data['user_id']
                conditions_dict = data.get('conditions', {})
                completed_courses = self._parse_courses(data['completed_courses'])
                available_courses = self._parse_courses(data['available_courses'])
                necessary_subjects = data.get('necessary_subjects', {})

                # Set avoid first period condition
                user_conditions = self._parse_user_conditions(conditions_dict)
                user_conditions.avoid_first_period = True

                # Use specific method for avoiding first period
                recommendations = self.condition_parser.get_registration_pattern_avoiding_first_hour_class(
                    user_conditions,
                    completed_courses,
                    available_courses,
                    necessary_subjects
                )

                # Convert to JSON response
                response_data = {
                    'status': 'success',
                    'recommendations': [self._pattern_to_dict(pattern) for pattern in recommendations],
                    'condition_applied': '1限回避パターン',
                    'timestamp': datetime.now().isoformat()
                }

                return jsonify(response_data), 200

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500

    def _parse_user_conditions(self, conditions_dict: Dict[str, Any]) -> UserConditions:
        """Parse conditions dictionary to UserConditions object"""
        return UserConditions(
            min_units=conditions_dict.get('min_units', 12),
            max_units=conditions_dict.get('max_units', 22),
            preferences=conditions_dict.get('preferences', []),
            avoid_first_period=conditions_dict.get('avoid_first_period', False),
            preferred_time_slots=conditions_dict.get('preferred_time_slots', []),
            preferred_categories=self._parse_course_categories(conditions_dict.get('preferred_categories', []))
        )

    def _parse_courses(self, courses_data: List[Dict[str, Any]]) -> List[Course]:
        """Parse course data from JSON to Course objects"""
        courses = []

        for course_data in courses_data:
            try:
                course = Course(
                    subject_name=course_data['subject_name'],
                    code=course_data['code'],
                    grade=course_data.get('grade'),
                    category=CourseCategory(course_data['category']),
                    requirement=RequirementType(course_data['requirement']),
                    credit=course_data['credit'],
                    semester=course_data['semester'],
                    year=course_data['year'],
                    time_slot=course_data.get('time_slot'),
                    prerequisites=course_data.get('prerequisites', [])
                )
                courses.append(course)
            except (KeyError, ValueError) as e:
                print(f"Error parsing course data: {e}")
                continue

        return courses

    def _parse_course_categories(self, category_strings: List[str]) -> List[CourseCategory]:
        """Parse category strings to CourseCategory enums"""
        categories = []
        category_mapping = {
            '全学共通科目': CourseCategory.UNIVERSITY_COMMON,
            '共通数理科目': CourseCategory.COMMON_MATH,
            '言語科目': CourseCategory.LANGUAGE,
            '情報科目': CourseCategory.INFORMATICS,
            '体育健康科目': CourseCategory.HEALTH_PE,
            '専門科目': CourseCategory.MAJOR
        }

        for cat_str in category_strings:
            if cat_str in category_mapping:
                categories.append(category_mapping[cat_str])

        return categories

    def _pattern_to_dict(self, pattern) -> Dict[str, Any]:
        """Convert SuggestedCoursePattern to dictionary for JSON response"""
        return {
            'semester': pattern.semester,
            'year': pattern.year,
            'courses': [self._course_to_dict(course) for course in pattern.courses],
            'total_credits': pattern.total_credits,
            'category_credits': {cat.value: credits for cat, credits in pattern.category_credits.items()}
        }

    def _plan_pattern_to_dict(self, pattern) -> Dict[str, Any]:
        """Convert PlanPattern to dictionary for JSON response"""
        return {
            'pattern_id': pattern.pattern_id,
            'description': pattern.description,
            'yearly_patterns': [
                [self._pattern_to_dict(semester_pattern) for semester_pattern in year_patterns]
                for year_patterns in pattern.yearly_patterns
            ],
            'total_credits': pattern.total_credits,
            'graduation_feasible': pattern.graduation_feasible
        }

    def _course_to_dict(self, course: Course) -> Dict[str, Any]:
        """Convert Course object to dictionary for JSON response"""
        return {
            'subject_name': course.subject_name,
            'code': course.code,
            'grade': course.grade,
            'category': course.category.value,
            'requirement': course.requirement.value,
            'credit': course.credit,
            'semester': course.semester,
            'year': course.year,
            'time_slot': course.time_slot,
            'prerequisites': course.prerequisites
        }

    def _summarize_conditions(self, conditions: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of applied conditions"""
        summary = {
            'credit_range': f"{conditions.get('min_units', 12)}-{conditions.get('max_units', 22)}単位",
            'avoid_first_period': conditions.get('avoid_first_period', False),
            'preferences': conditions.get('preferences', []),
            'preferred_time_slots': conditions.get('preferred_time_slots', []),
            'preferred_categories': conditions.get('preferred_categories', [])
        }
        return summary


def register_c4_api(app: Flask) -> C4API:
    """
    Register C4 API endpoints with Flask app

    Args:
        app: Flask application instance

    Returns:
        C4API instance
    """
    return C4API(app)
