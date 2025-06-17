"""
C4 条件処理部 (Condition Processing Component)
Course recommendation and pattern generation module
"""

from .condition_processor import ConditionProcessor
from .condition_parser import ConditionParser
from .registration_pattern_calculator import RegistrationPatternCalculator

# Optional API import (requires Flask)
try:
    from .api import register_c4_api
    __all__ = [
        'register_c4_api',
        'ConditionProcessor', 
        'ConditionParser',
        'RegistrationPatternCalculator'
    ]
except ImportError:
    # Flask not available, skip API registration
    __all__ = [
        'ConditionProcessor', 
        'ConditionParser',
        'RegistrationPatternCalculator'
    ]