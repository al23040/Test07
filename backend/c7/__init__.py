from c2.authorization import Authorization
from c5.account_manager import AccountManager
from c4.condition_processor import ConditionProcessor, UserConditions
from .api import register_c7_api
#from .enums import CourseCategory, DayOfWeek

# Optional API import (only if Flask is available)
try:
    from .api import register_c7_api

    __all__ = [
        'RequireInfo',
        'Authorization',
        'AccountManager',
        'ConditionProcessor',
        'UserConditions',
        'CourseCategory',
        'DayOfWeek',
        'register_c7_api',
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