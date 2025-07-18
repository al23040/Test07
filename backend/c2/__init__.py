from .authorization import Authorization
from c5.account_manager import AccountManager
from .api import register_c2_api

# Optional API import (requires Flask)
try:
    from .api import register_c2_api
    __all__ = [
        'register_c5_api',
        'Authorization',
        'AccountManager',
    ]
except ImportError:
    # Flask not available, skip API registration
    __all__ = [
        'Authorization',
        'AccountManager',
    ]
