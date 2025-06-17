"""
C5 アカウント管理部 (Account Management Component)
User account and course management module
"""

from .account_manager import AccountManager
from .database import C5DatabaseManager
from .models import UserInfo, TakenCourse, UserAccount, CourseRegistrationInfo, UserStatistics

# Optional API import (requires Flask)
try:
    from .api import register_c5_api
    __all__ = [
        'register_c5_api',
        'AccountManager',
        'C5DatabaseManager',
        'UserInfo',
        'TakenCourse',
        'UserAccount',
        'CourseRegistrationInfo',
        'UserStatistics'
    ]
except ImportError:
    # Flask not available, skip API registration
    __all__ = [
        'AccountManager',
        'C5DatabaseManager',
        'UserInfo',
        'TakenCourse',
        'UserAccount',
        'CourseRegistrationInfo',
        'UserStatistics'
    ]
