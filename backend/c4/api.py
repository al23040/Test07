from flask import Flask, request, jsonify
from typing import List, Dict, Optional, Any
import json
from datetime import datetime

from .condition_processor import ConditionProcessor, UserConditions, Course, CourseCategory, RequirementType, DayOfWeek
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

                # Convert to JSON response matching frontend format
                if recommendations:
                    recommendation = recommendations[0]  # Take first recommendation
                    recommended_subjects = [
                        {
                            'id': course.code,
                            'name': course.subject_name,
                            'units': course.credit,
                            'category': course.category.value,
                            'semester': '前期' if recommendation.semester == 1 else '後期'
                        }
                        for course in recommendation.courses
                    ]
                    
                    current_semester_schedule = self._convert_to_schedule_format(recommendation.courses)
                    
                    response_data = {
                        'totalUnits': 124,  # Total required units for graduation
                        'remainingUnits': max(0, 124 - sum(c.credit for c in completed_courses if c.grade and c.grade not in ['F', 'X'])),
                        'basicTechExamCompletionRate': 85,  # Placeholder value
                        'recommendedSubjects': recommended_subjects,
                        'notes': f'{recommendation.year}年生{recommendation.semester}学期のおすすめ科目です。',
                        'currentSemesterSchedule': current_semester_schedule,
                        'year': recommendation.year,
                        'semester': '前期' if recommendation.semester == 1 else '後期'
                    }
                else:
                    response_data = {
                        'totalUnits': 124,
                        'remainingUnits': 0,
                        'basicTechExamCompletionRate': 85,
                        'recommendedSubjects': [],
                        'notes': 'おすすめ科目が見つかりませんでした。',
                        'currentSemesterSchedule': {},
                        'year': 1,
                        'semester': '前期'
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

                # Convert to JSON response matching frontend format
                pattern_id = data.get('pattern_id')  # Check if specific pattern requested
                
                if pattern_id:
                    # Return specific pattern details
                    found_pattern = next((p for p in patterns if p.pattern_id == pattern_id), None)
                    if found_pattern:
                        response_data = self._plan_pattern_to_dict(found_pattern)
                    else:
                        return jsonify({'error': 'Pattern not found'}), 404
                else:
                    # Return summary of all patterns
                    pattern_summaries = [
                        {
                            'id': pattern.pattern_id,
                            'name': f'パターン{pattern.pattern_id.replace("pattern", "")}',
                            'description': pattern.description,
                            'totalUnits': pattern.total_credits
                        }
                        for pattern in patterns
                    ]
                    response_data = pattern_summaries

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
            preferred_categories=self._parse_course_categories(conditions_dict.get('preferred_categories', [])),
            preferred_days=self._parse_days_of_week(conditions_dict.get('preferred_days', [])),
            avoided_days=self._parse_days_of_week(conditions_dict.get('avoided_days', []))
        )

    def _parse_courses(self, courses_data: List[Dict[str, Any]]) -> List[Course]:
        """Parse course data from JSON to Course objects"""
        courses = []

        for course_data in courses_data:
            try:
                day_of_week = None
                if 'day_of_week' in course_data and course_data['day_of_week']:
                    try:
                        day_of_week = DayOfWeek(course_data['day_of_week'])
                    except ValueError:
                        day_of_week = None
                
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
                    day_of_week=day_of_week,
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

    def _parse_days_of_week(self, day_strings: List[str]) -> List[DayOfWeek]:
        """Parse day strings to DayOfWeek enums"""
        days = []
        day_mapping = {
            '月': DayOfWeek.MONDAY,
            '火': DayOfWeek.TUESDAY,
            '水': DayOfWeek.WEDNESDAY,
            '木': DayOfWeek.THURSDAY,
            '金': DayOfWeek.FRIDAY,
            '土': DayOfWeek.SATURDAY,
            '日': DayOfWeek.SUNDAY,
            'Monday': DayOfWeek.MONDAY,
            'Tuesday': DayOfWeek.TUESDAY,
            'Wednesday': DayOfWeek.WEDNESDAY,
            'Thursday': DayOfWeek.THURSDAY,
            'Friday': DayOfWeek.FRIDAY,
            'Saturday': DayOfWeek.SATURDAY,
            'Sunday': DayOfWeek.SUNDAY
        }

        for day_str in day_strings:
            if day_str in day_mapping:
                days.append(day_mapping[day_str])

        return days

    def _convert_to_schedule_format(self, courses: List[Course]) -> Dict[str, Dict[str, Optional[str]]]:
        """Convert courses to the frontend schedule format"""
        # Initialize empty schedule
        schedule = {
            '月': {'1限': None, '2限': None, '3限': None, '4限': None, '5限': None},
            '火': {'1限': None, '2限': None, '3限': None, '4限': None, '5限': None},
            '水': {'1限': None, '2限': None, '3限': None, '4限': None, '5限': None},
            '木': {'1限': None, '2限': None, '3限': None, '4限': None, '5限': None},
            '金': {'1限': None, '2限': None, '3限': None, '4限': None, '5限': None}
        }
        
        # Map time slots to period names
        time_slot_mapping = {
            '1': '1限', '1-2': '1限',
            '2': '2限', '2-3': '2限', 
            '3': '3限', '3-4': '3限',
            '4': '4限', '4-5': '4限',
            '5': '5限'
        }
        
        # Place courses in schedule
        for course in courses:
            if course.day_of_week and course.time_slot:
                day_key = course.day_of_week.value
                time_period = time_slot_mapping.get(course.time_slot, '1限')
                
                if day_key in schedule and time_period in schedule[day_key]:
                    schedule[day_key][time_period] = course.subject_name
        
        return schedule

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
        """Convert PlanPattern to dictionary for JSON response matching frontend format"""
        semesters = []
        
        # Convert yearly_patterns to flat semester list with schedule format
        for year_patterns in pattern.yearly_patterns:
            for semester_pattern in year_patterns:
                semester_data = {
                    'year': semester_pattern.year,
                    'semester': '前期' if semester_pattern.semester == 1 else '後期',
                    'schedule': self._convert_to_schedule_format(semester_pattern.courses)
                }
                semesters.append(semester_data)
        
        # Extract number from pattern_id (e.g., "pattern1" -> "1")
        pattern_number = pattern.pattern_id.replace('pattern', '')
        
        return {
            'id': pattern.pattern_id,
            'name': f'パターン{pattern_number}',
            'description': pattern.description,
            'totalUnits': pattern.total_credits,
            'semesters': semesters
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
            'day_of_week': course.day_of_week.value if course.day_of_week else None,
            'prerequisites': course.prerequisites
        }

    def _summarize_conditions(self, conditions: Dict[str, Any]) -> Dict[str, Any]:
        """Create a summary of applied conditions"""
        summary = {
            'credit_range': f"{conditions.get('min_units', 12)}-{conditions.get('max_units', 22)}単位",
            'avoid_first_period': conditions.get('avoid_first_period', False),
            'preferences': conditions.get('preferences', []),
            'preferred_time_slots': conditions.get('preferred_time_slots', []),
            'preferred_categories': conditions.get('preferred_categories', []),
            'preferred_days': conditions.get('preferred_days', []),
            'avoided_days': conditions.get('avoided_days', [])
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
