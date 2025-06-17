"""
C5 アカウント管理部 (Account Management Component) - Main Implementation
Core user account and course management functionality
"""

from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
import json

from c5_models import UserInfo, UserAccount, TakenCourse, CourseRegistrationInfo, UserStatistics
from c5_database import C5DatabaseManager


class AccountManager:
    """
    Main C5 Account Management Component
    Implements the core functionality specified in the requirements
    """
    
    def __init__(self, db_path: str = 'course_registration.db'):
        self.db_manager = C5DatabaseManager(db_path)
    
    # Core C5 Operations as specified in requirements
    
    def login_user(self, user_id: int) -> Optional[UserInfo]:
        """
        ログイン (Login)
        Search for student ID, retrieve user information, send to authentication component
        
        Args:
            user_id: Student ID from W1 Login Screen
            
        Returns:
            UserInfo object if user exists, None otherwise
            
        Collaboration: C2 Authentication Component
        Output: User data to W1 Login Screen
        """
        try:
            user_info = self.db_manager.get_user_info(user_id)
            if user_info:
                # Log the access for audit purposes
                print(f"User {user_id} data retrieved for authentication")
                return user_info
            else:
                print(f"User {user_id} not found")
                return None
                
        except Exception as e:
            print(f"Error during user login: {e}")
            return None
    
    def register_user_courses(self, user_id: int, taken_courses: List[TakenCourse]) -> bool:
        """
        履修登録状況を入力 (Course Registration Status Input)
        Register completed courses and update user information
        
        Args:
            user_id: User identification
            taken_courses: List of completed courses from W4 Course Confirmation Screen
            
        Returns:
            bool: Registration completion status
            
        Output: Registration completion confirmation
        """
        try:
            # Validate user exists
            if not self.db_manager.get_user_account(user_id):
                print(f"User {user_id} does not exist")
                return False
            
            # Register courses
            success = self.db_manager.register_multiple_courses(user_id, taken_courses)
            
            if success:
                print(f"Successfully registered {len(taken_courses)} courses for user {user_id}")
                return True
            else:
                print(f"Failed to register courses for user {user_id}")
                return False
                
        except Exception as e:
            print(f"Error registering user courses: {e}")
            return False
    
    def verify_user_info(self, user_id: int) -> bool:
        """
        今学期のおすすめ履修登録を表示 (Display Current Semester Recommendations)
        Verify user information
        
        Args:
            user_id: User identification
            
        Returns:
            bool: Verification completion status
            
        Collaboration: C3 Course Processing Component
        Output: Confirmation completion
        """
        try:
            user_info = self.db_manager.get_user_info(user_id)
            if user_info:
                print(f"User {user_id} information verified successfully")
                return True
            else:
                print(f"User {user_id} information verification failed")
                return False
                
        except Exception as e:
            print(f"Error verifying user info: {e}")
            return False
    
    # User Management Methods
    
    def create_user_account(self, user_id: int, password: str) -> bool:
        """
        Create new user account
        Supports C2 Authentication Component for new user registration
        """
        try:
            # Validate student ID format (5 digits as per specifications)
            if not (10000 <= user_id <= 99999):
                print(f"Invalid student ID format: {user_id}")
                return False
            
            # Validate password requirements (8-64 characters, alphanumeric)
            if not self._validate_password(password):
                print("Password does not meet requirements")
                return False
            
            success = self.db_manager.add_user(user_id, password)
            if success:
                print(f"User account created successfully for {user_id}")
                return True
            else:
                print(f"Failed to create user account for {user_id} (may already exist)")
                return False
                
        except Exception as e:
            print(f"Error creating user account: {e}")
            return False
    
    def authenticate_user(self, user_id: int, password: str) -> bool:
        """
        Authenticate user credentials
        Supports C2 Authentication Component
        """
        try:
            success = self.db_manager.check_user_credentials(user_id, password)
            if success:
                print(f"User {user_id} authenticated successfully")
            else:
                print(f"Authentication failed for user {user_id}")
            return success
            
        except Exception as e:
            print(f"Error authenticating user: {e}")
            return False
    
    def get_user_info(self, user_id: int) -> Optional[UserInfo]:
        """
        Get complete user information
        Main method for retrieving user data
        """
        return self.db_manager.get_user_info(user_id)
    
    def update_user_course(self, user_id: int, course: TakenCourse) -> bool:
        """
        Update or add a single course for user
        Supports course editing functionality
        """
        try:
            registration_info = CourseRegistrationInfo(
                user_id=user_id,
                subject_id=course.subject_id,
                subject_name=course.subject_name,
                evaluation=course.evaluation,
                credits=course.credits,
                passed=course.passed,
                semester=course.semester,
                year=course.year,
                category=course.category
            )
            
            success = self.db_manager.register_course(registration_info)
            if success:
                print(f"Course {course.subject_name} updated for user {user_id}")
            return success
            
        except Exception as e:
            print(f"Error updating user course: {e}")
            return False
    
    def get_user_statistics(self, user_id: int) -> Optional[UserStatistics]:
        """
        Get user academic statistics
        Useful for progress tracking and reporting
        """
        return self.db_manager.get_user_statistics(user_id)
    
    def get_user_courses_by_category(self, user_id: int, category: str) -> List[TakenCourse]:
        """
        Get user courses filtered by category
        Supports category-specific course analysis
        """
        try:
            user_info = self.get_user_info(user_id)
            if user_info:
                return user_info.get_courses_by_category(category)
            return []
            
        except Exception as e:
            print(f"Error getting courses by category: {e}")
            return []
    
    def get_user_passed_courses(self, user_id: int) -> List[TakenCourse]:
        """
        Get only passed courses for user
        Useful for prerequisite checking and graduation requirement validation
        """
        try:
            user_info = self.get_user_info(user_id)
            if user_info:
                return user_info.get_passed_courses()
            return []
            
        except Exception as e:
            print(f"Error getting passed courses: {e}")
            return []
    
    def delete_user_account(self, user_id: int) -> bool:
        """
        Delete user account and all associated data
        Administrative function
        """
        try:
            success = self.db_manager.delete_user(user_id)
            if success:
                print(f"User account {user_id} deleted successfully")
            return success
            
        except Exception as e:
            print(f"Error deleting user account: {e}")
            return False
    
    def get_all_users(self) -> List[int]:
        """
        Get list of all user IDs
        Administrative function
        """
        return self.db_manager.get_all_users()
    
    # Server Interface Functions (I2) - as specified in requirements
    
    def get_user_data(self, student_id: int) -> Optional[Dict[str, Any]]:
        """
        Server interface function: get_user_data(student_id)
        Retrieve user information in dictionary format for API responses
        """
        try:
            user_info = self.get_user_info(student_id)
            if user_info:
                return {
                    'user_id': user_info.user_id,
                    'taken_courses': [
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
                    ],
                    'total_credits': user_info.total_credits,
                    'gpa': user_info.gpa
                }
            return None
            
        except Exception as e:
            print(f"Error getting user data: {e}")
            return None
    
    def register_user(self, student_id: int, password: str = None) -> bool:
        """
        Server interface function: register_user(student_id)
        Register new user (password optional for interface compatibility)
        """
        if password is None:
            # Generate default password if not provided
            password = f"temp{student_id}"
        
        return self.create_user_account(student_id, password)
    
    def register_courses(self, student_id: int, courses: List[Dict[str, Any]]) -> bool:
        """
        Server interface function: register_courses(student_id, courses)
        Register user's courses from dictionary format
        """
        try:
            taken_courses = []
            for course_data in courses:
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
            
            return self.register_user_courses(student_id, taken_courses)
            
        except Exception as e:
            print(f"Error registering courses from API: {e}")
            return False
    
    def get_user_courses(self, student_id: int) -> List[Dict[str, Any]]:
        """
        Server interface function: get_user_courses(student_id)
        Retrieve user's courses in dictionary format
        """
        try:
            user_info = self.get_user_info(student_id)
            if user_info:
                return [
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
            return []
            
        except Exception as e:
            print(f"Error getting user courses from API: {e}")
            return []
    
    # Utility Methods
    
    def _validate_password(self, password: str) -> bool:
        """
        Validate password according to specifications
        Requirements: 8-64 characters, alphanumeric
        """
        if not (8 <= len(password) <= 64):
            return False
        
        # Check for alphanumeric characters
        has_alpha = any(c.isalpha() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        return has_alpha and has_digit
    
    def export_user_data(self, user_id: int) -> Optional[str]:
        """
        Export user data as JSON string
        Useful for data backup and transfer
        """
        try:
            user_data = self.get_user_data(user_id)
            if user_data:
                return json.dumps(user_data, indent=2, ensure_ascii=False)
            return None
            
        except Exception as e:
            print(f"Error exporting user data: {e}")
            return None
    
    def import_user_data(self, user_id: int, json_data: str) -> bool:
        """
        Import user data from JSON string
        Useful for data restoration
        """
        try:
            user_data = json.loads(json_data)
            courses = user_data.get('taken_courses', [])
            
            return self.register_courses(user_id, courses)
            
        except Exception as e:
            print(f"Error importing user data: {e}")
            return False