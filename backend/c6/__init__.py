from .api import register_c6_api
from CoursesInfo import get_user_courses

try:
    from .api import register_c6_api
    __all__ = [
        'register_c6api',
        'get_user_courses',
    ]
except ImportError:
    __all__ = [
        'get_user_courses',
    ]