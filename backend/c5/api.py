"""
C5 アカウント管理部 (Account Management Component) - API Integration
HTTP API endpoints for user account and course management
"""

from flask import Flask, request, jsonify
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from .account_manager import AccountManager
from .models import TakenCourse, UserInfo


class C5API:
    """
    C5 Account Management Component API Interface
    Handles HTTP requests for user management and course registration
    """

    def __init__(self, app: Flask):
        self.app = app
        self.account_manager = AccountManager()

        # Register API routes
        self._register_routes()

    def _register_routes(self):
        """Register API endpoints for C5 functionality"""

        @self.app.route('/api/c5/users/register', methods=['POST'])
        def register_user():
            """
            User registration endpoint
            Implements C5 new user registration functionality
            """
            try:
                data = request.get_json()

                # Validate required fields
                if 'user_id' not in data or 'password' not in data:
                    return jsonify({'error': 'Missing user_id or password'}), 400

                user_id = data['user_id']
                password = data['password']

                # Validate student ID format (5 digits)
                if not (10000 <= user_id <= 99999):
                    return jsonify({'error': 'Student ID must be 5 digits'}), 400

                # Create user account
                success = self.account_manager.create_user_account(user_id, password)

                if success:
                    return jsonify({
                        'status': 'success',
                        'message': 'User registered successfully',
                        'user_id': user_id,
                        'timestamp': datetime.now().isoformat()
                    }), 201
                else:
                    return jsonify({
                        'status': 'error',
                        'message': 'Registration failed - user may already exist',
                        'timestamp': datetime.now().isoformat()
                    }), 409

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500

        @self.app.route('/api/c5/users/login', methods=['POST'])
        def login_user():
            """
            User login endpoint
            Implements C5 login functionality for C2 integration
            """
            try:
                data = request.get_json()

                if 'user_id' not in data or 'password' not in data:
                    return jsonify({'error': 'Missing user_id or password'}), 400

                user_id = data['user_id']
                password = data['password']

                # Authenticate user
                authenticated = self.account_manager.authenticate_user(user_id, password)

                if authenticated:
                    # Get user information for login
                    user_info = self.account_manager.login_user(user_id)

                    if user_info:
                        return jsonify({
                            'status': 'success',
                            'message': 'Login successful',
                            'user_data': {
                                'user_id': user_info.user_id,
                                'total_credits': user_info.total_credits,
                                'gpa': user_info.gpa,
                                'courses_count': len(user_info.taken_courses)
                            },
                            'timestamp': datetime.now().isoformat()
                        }), 200
                    else:
                        return jsonify({
                            'status': 'error',
                            'message': 'User data not found',
                            'timestamp': datetime.now().isoformat()
                        }), 404
                else:
                    return jsonify({
                        'status': 'error',
                        'message': 'Invalid credentials',
                        'timestamp': datetime.now().isoformat()
                    }), 401

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500

        @self.app.route('/api/c5/users/<int:user_id>/info', methods=['GET'])
        def get_user_info(user_id: int):
            """
            Get user information endpoint
            Implements C5 user data retrieval functionality
            """
            try:
                user_info = self.account_manager.get_user_info(user_id)

                if user_info:
                    return jsonify({
                        'status': 'success',
                        'user_info': {
                            'user_id': user_info.user_id,
                            'total_credits': user_info.total_credits,
                            'gpa': user_info.gpa,
                            'courses': [
                                {
                                    'subject_id': course.subject_id,
                                    'subject_name': course.subject_name,
                                    'evaluation': course.evaluation,
                                    'credits': course.credits,
                                    'passed': course.passed,
                                    'semester': course.semester,
                                    'year': course.year,
                                    'category': course.category
                                }
                                for course in user_info.taken_courses
                            ]
                        },
                        'timestamp': datetime.now().isoformat()
                    }), 200
                else:
                    return jsonify({
                        'status': 'error',
                        'message': 'User not found',
                        'timestamp': datetime.now().isoformat()
                    }), 404

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500

        @self.app.route('/api/c5/users/<int:user_id>/courses', methods=['POST'])
        def register_user_courses(user_id: int):
            """
            Register user courses endpoint
            Implements C5 course registration functionality
            """
            try:
                data = request.get_json()

                if 'courses' not in data:
                    return jsonify({'error': 'Missing courses data'}), 400

                courses_data = data['courses']

                # Parse courses data
                taken_courses = []
                for course_data in courses_data:
                    try:
                        course = TakenCourse(
                            subject_id=course_data['subject_id'],
                            subject_name=course_data['subject_name'],
                            evaluation=course_data.get('evaluation', 'C'),
                            credits=course_data['credits'],
                            passed=course_data.get('passed', True),
                            semester=course_data.get('semester', 1),
                            year=course_data.get('year', 1),
                            category=course_data.get('category', '')
                        )
                        taken_courses.append(course)
                    except KeyError as e:
                        return jsonify({
                            'error': f'Missing required field in course data: {e}',
                            'timestamp': datetime.now().isoformat()
                        }), 400

                # Register courses
                success = self.account_manager.register_user_courses(user_id, taken_courses)

                if success:
                    return jsonify({
                        'status': 'success',
                        'message': f'Successfully registered {len(taken_courses)} courses',
                        'courses_registered': len(taken_courses),
                        'timestamp': datetime.now().isoformat()
                    }), 200
                else:
                    return jsonify({
                        'status': 'error',
                        'message': 'Course registration failed',
                        'timestamp': datetime.now().isoformat()
                    }), 500

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500

        @self.app.route('/api/c5/users/<int:user_id>/courses', methods=['GET'])
        def get_user_courses(user_id: int):
            """
            Get user courses endpoint
            Retrieve all courses for a specific user
            """
            try:
                courses = self.account_manager.get_user_courses(user_id)

                return jsonify({
                    'status': 'success',
                    'user_id': user_id,
                    'courses': courses,
                    'courses_count': len(courses),
                    'timestamp': datetime.now().isoformat()
                }), 200

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500

        @self.app.route('/api/c5/users/<int:user_id>/courses/<int:subject_id>', methods=['PUT'])
        def update_user_course(user_id: int, subject_id: int):
            """
            Update specific course for user
            Supports course editing functionality
            """
            try:
                data = request.get_json()

                # Create updated course object
                course = TakenCourse(
                    subject_id=subject_id,
                    subject_name=data['subject_name'],
                    evaluation=data.get('evaluation', 'C'),
                    credits=data['credits'],
                    passed=data.get('passed', True),
                    semester=data.get('semester', 1),
                    year=data.get('year', 1),
                    category=data.get('category', '')
                )

                success = self.account_manager.update_user_course(user_id, course)

                if success:
                    return jsonify({
                        'status': 'success',
                        'message': 'Course updated successfully',
                        'timestamp': datetime.now().isoformat()
                    }), 200
                else:
                    return jsonify({
                        'status': 'error',
                        'message': 'Course update failed',
                        'timestamp': datetime.now().isoformat()
                    }), 500

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500

        @self.app.route('/api/c5/users/<int:user_id>/statistics', methods=['GET'])
        def get_user_statistics(user_id: int):
            """
            Get user academic statistics
            Provides comprehensive user performance data
            """
            try:
                stats = self.account_manager.get_user_statistics(user_id)

                if stats:
                    return jsonify({
                        'status': 'success',
                        'statistics': {
                            'user_id': stats.user_id,
                            'total_credits': stats.total_credits,
                            'total_passed_credits': stats.total_passed_credits,
                            'total_failed_credits': stats.total_failed_credits,
                            'gpa': stats.gpa,
                            'courses_taken': stats.courses_taken,
                            'courses_passed': stats.courses_passed,
                            'courses_failed': stats.courses_failed,
                            'completion_rate': stats.completion_rate
                        },
                        'timestamp': datetime.now().isoformat()
                    }), 200
                else:
                    return jsonify({
                        'status': 'error',
                        'message': 'User statistics not found',
                        'timestamp': datetime.now().isoformat()
                    }), 404

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500

        @self.app.route('/api/c5/users/<int:user_id>/verify', methods=['POST'])
        def verify_user_info(user_id: int):
            """
            Verify user information endpoint
            Implements C5 user verification for recommendation system
            """
            try:
                verified = self.account_manager.verify_user_info(user_id)

                if verified:
                    return jsonify({
                        'status': 'success',
                        'message': 'User information verified',
                        'verified': True,
                        'timestamp': datetime.now().isoformat()
                    }), 200
                else:
                    return jsonify({
                        'status': 'error',
                        'message': 'User verification failed',
                        'verified': False,
                        'timestamp': datetime.now().isoformat()
                    }), 404

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500

        @self.app.route('/api/c5/users/<int:user_id>/export', methods=['GET'])
        def export_user_data(user_id: int):
            """
            Export user data as JSON
            Useful for data backup and transfer
            """
            try:
                json_data = self.account_manager.export_user_data(user_id)

                if json_data:
                    return jsonify({
                        'status': 'success',
                        'data': json.loads(json_data),
                        'timestamp': datetime.now().isoformat()
                    }), 200
                else:
                    return jsonify({
                        'status': 'error',
                        'message': 'User data not found',
                        'timestamp': datetime.now().isoformat()
                    }), 404

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500

        @self.app.route('/api/c5/users', methods=['GET'])
        def get_all_users():
            """
            Get all users endpoint
            Administrative function
            """
            try:
                users = self.account_manager.get_all_users()

                return jsonify({
                    'status': 'success',
                    'users': users,
                    'count': len(users),
                    'timestamp': datetime.now().isoformat()
                }), 200

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500

        # F3 Subject Management Endpoints

        @self.app.route('/api/c5/subjects', methods=['POST'])
        def add_subject():
            """
            Add new subject to F3 (subjects table)
            """
            try:
                data = request.get_json()

                required_fields = ['subject_id', 'subject_name', 'credits', 'category',
                                 'requirement_type', 'semester_offered', 'year_offered']
                for field in required_fields:
                    if field not in data:
                        return jsonify({'error': f'Missing required field: {field}'}), 400

                success = self.account_manager.db_manager.add_subject(
                    subject_id=data['subject_id'],
                    subject_name=data['subject_name'],
                    credits=data['credits'],
                    category=data['category'],
                    requirement_type=data['requirement_type'],
                    semester_offered=data['semester_offered'],
                    year_offered=data['year_offered'],
                    time_slot=data.get('time_slot', ''),
                    prerequisites=data.get('prerequisites', []),
                    description=data.get('description', '')
                )

                if success:
                    return jsonify({
                        'status': 'success',
                        'message': 'Subject added successfully',
                        'subject_id': data['subject_id'],
                        'timestamp': datetime.now().isoformat()
                    }), 201
                else:
                    return jsonify({
                        'status': 'error',
                        'message': 'Failed to add subject',
                        'timestamp': datetime.now().isoformat()
                    }), 500

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500

        @self.app.route('/api/c5/subjects/<int:subject_id>', methods=['GET'])
        def get_subject(subject_id: int):
            """
            Get subject information from F3 (subjects table)
            """
            try:
                subject = self.account_manager.db_manager.get_subject(subject_id)

                if subject:
                    return jsonify({
                        'status': 'success',
                        'subject': subject,
                        'timestamp': datetime.now().isoformat()
                    }), 200
                else:
                    return jsonify({
                        'status': 'error',
                        'message': 'Subject not found',
                        'timestamp': datetime.now().isoformat()
                    }), 404

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500

        @self.app.route('/api/c5/subjects', methods=['GET'])
        def get_all_subjects():
            """
            Get all subjects from F3 (subjects table)
            """
            try:
                subjects = self.account_manager.db_manager.get_all_subjects()

                return jsonify({
                    'status': 'success',
                    'subjects': subjects,
                    'count': len(subjects),
                    'timestamp': datetime.now().isoformat()
                }), 200

            except Exception as e:
                return jsonify({
                    'status': 'error',
                    'message': str(e),
                    'timestamp': datetime.now().isoformat()
                }), 500


def register_c5_api(app: Flask) -> C5API:
    """
    Register C5 API endpoints with Flask app

    Args:
        app: Flask application instance

    Returns:
        C5API instance
    """
    return C5API(app)
