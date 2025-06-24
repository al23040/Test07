"""
C5 アカウント管理部 (Account Management Component) - Database Manager
Enhanced database operations for user account and course management
"""

import sqlite3
import hashlib
import json
from typing import List, Optional, Dict, Any, Tuple
from datetime import datetime
from contextlib import contextmanager

from .models import UserInfo, UserAccount, TakenCourse, CourseRegistrationInfo, UserStatistics


class C5DatabaseManager:
    """
    Enhanced database manager for C5 Account Management Component
    Handles user accounts, course registrations, and user data management
    """

    def __init__(self, db_path: str = 'course_registration.db'):
        self.db_path = db_path
        self.initialize_database()

    def initialize_database(self):
        """Initialize database with required tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Users table for authentication (F1)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')

            # F2: Course registrations table (evaluated courses)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS registrations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    subject_id TEXT NOT NULL,
                    evaluation TEXT NOT NULL,
                    passed BOOLEAN NOT NULL,
                    semester_taken INTEGER NOT NULL,
                    year_taken INTEGER NOT NULL,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id),
                    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id),
                    UNIQUE(user_id, subject_id)
                )
            ''')

            # F3: Subjects master table (subject information)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS subjects (
                    subject_id TEXT PRIMARY KEY,
                    subject_name TEXT NOT NULL,
                    credits INTEGER NOT NULL,
                    category TEXT NOT NULL,
                    requirement_type TEXT NOT NULL,
                    semester_offered INTEGER NOT NULL,
                    year_offered INTEGER NOT NULL,
                    time_slot TEXT,
                    day_of_week TEXT,
                    prerequisites TEXT DEFAULT '[]',
                    description TEXT DEFAULT ''
                )
            ''')
            

            # User profiles for additional information
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id INTEGER PRIMARY KEY,
                    total_credits INTEGER DEFAULT 0,
                    gpa REAL DEFAULT 0.0,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )
            ''')

            conn.commit()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
        finally:
            conn.close()

    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    # User Account Management Methods

    def add_user(self, user_id: int, password: str) -> bool:
        """
        Add new user account
        Implements: C5 new user registration functionality
        """
        try:
            password_hash = self.hash_password(password)
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Insert user account
                cursor.execute('''
                    INSERT INTO users (user_id, password_hash)
                    VALUES (?, ?)
                ''', (user_id, password_hash))

                # Initialize user profile
                cursor.execute('''
                    INSERT INTO user_profiles (user_id)
                    VALUES (?)
                ''', (user_id,))

                conn.commit()
                return True

        except sqlite3.IntegrityError:
            # User already exists
            return False
        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    def check_user_credentials(self, user_id: int, password: str) -> bool:
        """
        Verify user credentials
        Implements: C5 login functionality for C2 integration
        """
        try:
            password_hash = self.hash_password(password)
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT user_id FROM users
                    WHERE user_id = ? AND password_hash = ? AND is_active = 1
                ''', (user_id, password_hash))

                result = cursor.fetchone()
                if result:
                    # Update last login
                    cursor.execute('''
                        UPDATE users SET last_login = CURRENT_TIMESTAMP
                        WHERE user_id = ?
                    ''', (user_id,))
                    conn.commit()
                    return True
                return False

        except Exception as e:
            print(f"Error checking user credentials: {e}")
            return False

    def get_user_account(self, user_id: int) -> Optional[UserAccount]:
        """Get user account information"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT user_id, password_hash, created_at, last_login, is_active
                    FROM users WHERE user_id = ?
                ''', (user_id,))

                row = cursor.fetchone()
                if row:
                    return UserAccount(
                        user_id=row['user_id'],
                        password_hash=row['password_hash'],
                        created_at=datetime.fromisoformat(row['created_at']) if row['created_at'] else datetime.now(),
                        last_login=datetime.fromisoformat(row['last_login']) if row['last_login'] else None,
                        is_active=bool(row['is_active'])
                    )
                return None

        except Exception as e:
            print(f"Error getting user account: {e}")
            return None

    # Course Registration Management Methods

    def register_course(self, registration_info: CourseRegistrationInfo) -> bool:
        """
        Register a course for a user
        Implements: C5 course registration functionality
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # First ensure the subject exists in F3 (subjects table)
                self._ensure_subject_exists(cursor, registration_info)

                # Insert or update course registration in F2 (registrations table)
                cursor.execute('''
                    INSERT OR REPLACE INTO registrations
                    (user_id, subject_id, evaluation, passed, semester_taken, year_taken, registration_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    registration_info.user_id,
                    registration_info.subject_id,
                    registration_info.evaluation,
                    registration_info.passed,
                    registration_info.semester,
                    registration_info.year,
                    registration_info.registration_date.isoformat()
                ))

                conn.commit()

                # Update user profile statistics
                self._update_user_statistics(user_id=registration_info.user_id)

                return True

        except Exception as e:
            print(f"Error registering course: {e}")
            return False

    def register_multiple_courses(self, user_id: int, courses: List[TakenCourse]) -> bool:
        """
        Register multiple courses for a user
        Implements: Batch course registration functionality
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                for course in courses:
                    # Ensure subject exists in F3 (subjects table)
                    self._ensure_subject_exists_from_course(cursor, course)

                    # Insert or update registration in F2 (registrations table)
                    cursor.execute('''
                        INSERT OR REPLACE INTO registrations
                        (user_id, subject_id, evaluation, passed, semester_taken, year_taken)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
                        user_id,
                        course.subject_id,
                        course.evaluation,
                        course.passed,
                        course.semester,
                        course.year
                    ))

                conn.commit()

                # Update user profile statistics
                self._update_user_statistics(user_id=user_id)

                return True

        except Exception as e:
            print(f"Error registering multiple courses: {e}")
            return False

    def get_user_courses(self, user_id: int) -> List[TakenCourse]:
        """
        Get all courses for a user
        Implements: C5 course retrieval functionality
        """
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT r.subject_id, s.subject_name, r.evaluation, s.credits, r.passed,
                           r.semester_taken, r.year_taken, s.category
                    FROM registrations r
                    JOIN subjects s ON r.subject_id = s.subject_id
                    WHERE r.user_id = ?
                    ORDER BY r.year_taken, r.semester_taken, s.subject_name
                ''', (user_id,))

                courses = []
                for row in cursor.fetchall():
                    course = TakenCourse(
                        subject_id=row['subject_id'],
                        subject_name=row['subject_name'],
                        evaluation=row['evaluation'],
                        credits=row['credits'],
                        passed=bool(row['passed']),
                        semester=row['semester_taken'],
                        year=row['year_taken'],
                        category=row['category']
                    )
                    courses.append(course)

                return courses

        except Exception as e:
            print(f"Error getting user courses: {e}")
            return []

    def get_user_info(self, user_id: int) -> Optional[UserInfo]:
        """
        Get complete user information including courses
        Implements: C5 main user info retrieval functionality
        """
        try:
            # Check if user exists
            if not self.get_user_account(user_id):
                return None

            # Get user courses
            taken_courses = self.get_user_courses(user_id)

            # Create UserInfo object
            user_info = UserInfo(
                user_id=user_id,
                taken_courses=taken_courses
            )

            return user_info

        except Exception as e:
            print(f"Error getting user info: {e}")
            return None

    def _update_user_statistics(self, user_id: int) -> None:
        """Update user profile statistics"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Calculate statistics using JOIN between F2 and F3
                cursor.execute('''
                    SELECT
                        SUM(CASE WHEN r.passed = 1 THEN s.credits ELSE 0 END) as total_credits,
                        COUNT(*) as total_courses,
                        SUM(CASE WHEN r.passed = 1 THEN 1 ELSE 0 END) as passed_courses
                    FROM registrations r
                    JOIN subjects s ON r.subject_id = s.subject_id
                    WHERE r.user_id = ?
                ''', (user_id,))

                stats = cursor.fetchone()
                total_credits = stats['total_credits'] or 0

                # Calculate GPA using JOIN between F2 and F3
                cursor.execute('''
                    SELECT r.evaluation, s.credits
                    FROM registrations r
                    JOIN subjects s ON r.subject_id = s.subject_id
                    WHERE r.user_id = ? AND r.passed = 1 AND r.evaluation IN ('A+', 'A', 'B', 'C')
                ''', (user_id,))

                grade_points = {"A+": 4.3, "A": 4.0, "B": 3.0, "C": 2.0}
                total_points = 0
                total_credit_hours = 0

                for row in cursor.fetchall():
                    points = grade_points.get(row['evaluation'], 0.0)
                    credits = row['credits']
                    total_points += points * credits
                    total_credit_hours += credits

                gpa = total_points / total_credit_hours if total_credit_hours > 0 else 0.0

                # Update user profile
                cursor.execute('''
                    UPDATE user_profiles
                    SET total_credits = ?, gpa = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (total_credits, gpa, user_id))

                conn.commit()

        except Exception as e:
            print(f"Error updating user statistics: {e}")

    def get_user_statistics(self, user_id: int) -> Optional[UserStatistics]:
        """Get user academic statistics"""
        user_info = self.get_user_info(user_id)
        if user_info:
            return UserStatistics.from_user_info(user_info)
        return None

    def delete_user(self, user_id: int) -> bool:
        """Delete user and all associated data"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Delete user courses
                cursor.execute('DELETE FROM registrations WHERE user_id = ?', (user_id,))

                # Delete user profile
                cursor.execute('DELETE FROM user_profiles WHERE user_id = ?', (user_id,))

                # Delete user account
                cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))

                conn.commit()
                return True

        except Exception as e:
            print(f"Error deleting user: {e}")
            return False

    def get_all_users(self) -> List[int]:
        """Get list of all user IDs"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT user_id FROM users WHERE is_active = 1')
                return [row['user_id'] for row in cursor.fetchall()]

        except Exception as e:
            print(f"Error getting all users: {e}")
            return []

    # Helper methods for subject management

    def _ensure_subject_exists(self, cursor, registration_info: CourseRegistrationInfo) -> None:
        """Ensure subject exists in F3 (subjects table)"""
        cursor.execute('SELECT subject_id FROM subjects WHERE subject_id = ?', (registration_info.subject_id,))
        if not cursor.fetchone():
            # Insert subject into F3 if it doesn't exist
            cursor.execute('''
                INSERT INTO subjects
                (subject_id, subject_name, credits, category, requirement_type,
                 semester_offered, year_offered, time_slot, day_of_week, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                registration_info.subject_id,
                registration_info.subject_name,
                registration_info.credits,
                registration_info.category,
                'ELECTIVE',  # Default requirement type
                registration_info.semester,
                registration_info.year,
                '',  # Default time slot
                '',  # Default day of week
                f'Auto-created subject for {registration_info.subject_name}'
            ))

    def _ensure_subject_exists_from_course(self, cursor, course: TakenCourse) -> None:
        """Ensure subject exists in F3 (subjects table) from TakenCourse"""
        cursor.execute('SELECT subject_id FROM subjects WHERE subject_id = ?', (course.subject_id,))
        if not cursor.fetchone():
            # Insert subject into F3 if it doesn't exist
            cursor.execute('''
                INSERT INTO subjects
                (subject_id, subject_name, credits, category, requirement_type,
                 semester_offered, year_offered, time_slot, day_of_week, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                course.subject_id,
                course.subject_name,
                course.credits,
                course.category,
                'ELECTIVE',  # Default requirement type
                course.semester,
                course.year,
                '',  # Default time slot
                '',  # Default day of week
                f'Auto-created subject for {course.subject_name}'
            ))

    # Subject management methods

    def add_subject(self, subject_id: str, subject_name: str, credits: int,
                   category: str, requirement_type: str, semester_offered: int,
                   year_offered: int, time_slot: str = '', day_of_week: str = '',
                   prerequisites: List[str] = None, description: str = '') -> bool:
        """Add a new subject to F3 (subjects table)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                prereq_json = json.dumps(prerequisites) if prerequisites else '[]'

                cursor.execute('''
                    INSERT INTO subjects
                    (subject_id, subject_name, credits, category, requirement_type,
                     semester_offered, year_offered, time_slot, day_of_week, prerequisites, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    subject_id, subject_name, credits, category, requirement_type,
                    semester_offered, year_offered, time_slot, day_of_week, prereq_json, description
                ))

                conn.commit()
                return True

        except Exception as e:
            print(f"Error adding subject: {e}")
            return False

    def get_subject(self, subject_id: str) -> Optional[Dict[str, Any]]:
        """Get subject information from F3 (subjects table)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM subjects WHERE subject_id = ?
                ''', (subject_id,))

                row = cursor.fetchone()
                if row:
                    return {
                        'subject_id': row['subject_id'],
                        'subject_name': row['subject_name'],
                        'credits': row['credits'],
                        'category': row['category'],
                        'requirement_type': row['requirement_type'],
                        'semester_offered': row['semester_offered'],
                        'year_offered': row['year_offered'],
                        'time_slot': row['time_slot'],
                        'day_of_week': row['day_of_week'],
                        'prerequisites': json.loads(row['prerequisites']) if row['prerequisites'] else [],
                        'description': row['description']
                    }
                return None

        except Exception as e:
            print(f"Error getting subject: {e}")
            return None

    def get_all_subjects(self) -> List[Dict[str, Any]]:
        """Get all subjects from F3 (subjects table)"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM subjects ORDER BY subject_name')

                subjects = []
                for row in cursor.fetchall():
                    subject = {
                        'subject_id': row['subject_id'],
                        'subject_name': row['subject_name'],
                        'credits': row['credits'],
                        'category': row['category'],
                        'requirement_type': row['requirement_type'],
                        'semester_offered': row['semester_offered'],
                        'year_offered': row['year_offered'],
                        'time_slot': row['time_slot'],
                        'day_of_week': row['day_of_week'],
                        'prerequisites': json.loads(row['prerequisites']) if row['prerequisites'] else [],
                        'description': row['description']
                    }
                    subjects.append(subject)

                return subjects

        except Exception as e:
            print(f"Error getting all subjects: {e}")
            return []
