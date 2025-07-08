from .RequireInfo import RequireInfo
from .authorization import Authorization
from .account_manager import AccountManager
from .condition_processor import ConditionProcessor, UserConditions
from .enums import CourseCategory, DayOfWeek

# Optional API import (only if Flask is available)
try:
    from .api import register_user_conditions_api

    __all__ = [
        'RequireInfo',
        'Authorization',
        'AccountManager',
        'ConditionProcessor',
        'UserConditions',
        'CourseCategory',
        'DayOfWeek',
        'register_user_conditions_api',
    ]
except ImportError:
    # Flask not available, skip API registration
    __all__ = [
        'RequireInfo',
        'Authorization',
        'AccountManager',
        'ConditionProcessor',
        'UserConditions',
        'CourseCategory',
        'DayOfWeek',
    ]
