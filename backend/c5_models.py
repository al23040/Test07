"""
C5 アカウント管理部 (Account Management Component) - Data Models
Classes and data structures for user management
"""

from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class CourseStatus(Enum):
    """Course completion status"""
    PASSED = "passed"
    FAILED = "failed"
    IN_PROGRESS = "in_progress"
    NOT_TAKEN = "not_taken"


class GradeType(Enum):
    """Grade evaluation types"""
    A_PLUS = "A+"
    A = "A"
    B = "B"
    C = "C"
    F = "F"
    X = "X"  # Withdrawal


@dataclass
class TakenCourse:
    """Enhanced TakenCourse class according to specifications"""
    subject_id: int
    subject_name: str
    evaluation: str  # Grade (A, B, C, F, etc.)
    credits: int
    passed: bool
    semester: int
    year: int
    category: str = ""
    
    def __post_init__(self):
        """Validate course data after initialization"""
        if self.evaluation in ['F', 'X']:
            self.passed = False
        elif self.evaluation in ['A+', 'A', 'B', 'C']:
            self.passed = True


@dataclass
class UserInfo:
    """Enhanced UserInfo class according to specifications"""
    user_id: int
    taken_courses: List[TakenCourse] = field(default_factory=list)
    total_credits: int = 0
    gpa: float = 0.0
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        """Calculate totals after initialization"""
        self.calculate_totals()
    
    def calculate_totals(self) -> None:
        """Calculate total credits and GPA"""
        passed_courses = [course for course in self.taken_courses if course.passed]
        self.total_credits = sum(course.credits for course in passed_courses)
        
        # Calculate GPA
        if passed_courses:
            grade_points = {"A+": 4.3, "A": 4.0, "B": 3.0, "C": 2.0}
            total_points = sum(
                grade_points.get(course.evaluation, 0.0) * course.credits 
                for course in passed_courses 
                if course.evaluation in grade_points
            )
            total_credit_hours = sum(
                course.credits for course in passed_courses 
                if course.evaluation in grade_points
            )
            self.gpa = total_points / total_credit_hours if total_credit_hours > 0 else 0.0
        else:
            self.gpa = 0.0
    
    def add_course(self, course: TakenCourse) -> bool:
        """Add a new course to user's record"""
        # Check if course already exists
        for existing_course in self.taken_courses:
            if existing_course.subject_id == course.subject_id:
                # Update existing course
                existing_course.evaluation = course.evaluation
                existing_course.passed = course.passed
                existing_course.updated_at = datetime.now()
                self.calculate_totals()
                return True
        
        # Add new course
        self.taken_courses.append(course)
        self.calculate_totals()
        self.updated_at = datetime.now()
        return True
    
    def remove_course(self, subject_id: int) -> bool:
        """Remove a course from user's record"""
        for i, course in enumerate(self.taken_courses):
            if course.subject_id == subject_id:
                del self.taken_courses[i]
                self.calculate_totals()
                self.updated_at = datetime.now()
                return True
        return False
    
    def get_courses_by_category(self, category: str) -> List[TakenCourse]:
        """Get courses filtered by category"""
        return [course for course in self.taken_courses if course.category == category]
    
    def get_passed_courses(self) -> List[TakenCourse]:
        """Get only passed courses"""
        return [course for course in self.taken_courses if course.passed]
    
    def get_failed_courses(self) -> List[TakenCourse]:
        """Get only failed courses"""
        return [course for course in self.taken_courses if not course.passed]


@dataclass
class UserAccount:
    """User account information for authentication"""
    user_id: int
    password_hash: str
    created_at: datetime = field(default_factory=datetime.now)
    last_login: Optional[datetime] = None
    is_active: bool = True
    
    def update_last_login(self):
        """Update last login timestamp"""
        self.last_login = datetime.now()


@dataclass
class CourseRegistrationInfo:
    """Course registration information"""
    user_id: int
    subject_id: int
    subject_name: str
    evaluation: str
    credits: int
    passed: bool
    semester: int
    year: int
    category: str
    registration_date: datetime = field(default_factory=datetime.now)
    
    def to_taken_course(self) -> TakenCourse:
        """Convert to TakenCourse object"""
        return TakenCourse(
            subject_id=self.subject_id,
            subject_name=self.subject_name,
            evaluation=self.evaluation,
            credits=self.credits,
            passed=self.passed,
            semester=self.semester,
            year=self.year,
            category=self.category
        )


@dataclass
class UserStatistics:
    """User academic statistics"""
    user_id: int
    total_credits: int
    total_passed_credits: int
    total_failed_credits: int
    gpa: float
    courses_taken: int
    courses_passed: int
    courses_failed: int
    completion_rate: float
    
    @classmethod
    def from_user_info(cls, user_info: UserInfo) -> 'UserStatistics':
        """Create statistics from UserInfo"""
        passed_courses = user_info.get_passed_courses()
        failed_courses = user_info.get_failed_courses()
        
        total_credits = sum(course.credits for course in user_info.taken_courses)
        passed_credits = sum(course.credits for course in passed_courses)
        failed_credits = sum(course.credits for course in failed_courses)
        
        courses_taken = len(user_info.taken_courses)
        courses_passed = len(passed_courses)
        courses_failed = len(failed_courses)
        
        completion_rate = (courses_passed / courses_taken * 100) if courses_taken > 0 else 0.0
        
        return cls(
            user_id=user_info.user_id,
            total_credits=total_credits,
            total_passed_credits=passed_credits,
            total_failed_credits=failed_credits,
            gpa=user_info.gpa,
            courses_taken=courses_taken,
            courses_passed=courses_passed,
            courses_failed=courses_failed,
            completion_rate=completion_rate
        )


# Type aliases for better code readability
UserId = int
SubjectId = int
CourseData = Dict[str, Any]
RegistrationResult = Dict[str, Any]