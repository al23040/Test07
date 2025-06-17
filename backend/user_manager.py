"""
User Manager - Updated to use C5 Account Management Component
Maintains compatibility with existing imports while using new C5 implementation
"""

from typing import Optional
from c5_account_manager import AccountManager
from c5_models import UserInfo

# Initialize the C5 Account Manager
_account_manager = AccountManager()


def get_user_info(user_id: int) -> Optional[UserInfo]:
    """
    Get user information using C5 Account Management Component
    Maintains compatibility with existing code
    """
    return _account_manager.get_user_info(user_id)


# Additional compatibility functions
def register_subjects(user_id: int, taken_course) -> bool:
    """
    Register subjects for user - compatibility function
    """
    if hasattr(taken_course, 'name'):
        # Handle old TakenCourse format
        from c5_models import TakenCourse
        course = TakenCourse(
            subject_id=hash(taken_course.name) % 10000,  # Generate ID from name
            subject_name=taken_course.name,
            evaluation='C',
            credits=2,
            passed=True,
            semester=1,
            year=1
        )
        return _account_manager.update_user_course(user_id, course)
    return False


# Expose C5 functionality through user_manager
def create_user_account(user_id: int, password: str) -> bool:
    """Create new user account"""
    return _account_manager.create_user_account(user_id, password)


def authenticate_user(user_id: int, password: str) -> bool:
    """Authenticate user credentials"""
    return _account_manager.authenticate_user(user_id, password)
