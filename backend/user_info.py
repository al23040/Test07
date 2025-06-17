"""
User Info - Updated to use C5 models while maintaining compatibility
"""

# Import from C5 models for enhanced functionality
from c5_models import UserInfo as C5UserInfo, TakenCourse

# Re-export for compatibility
UserInfo = C5UserInfo

# Legacy compatibility class
class LegacyUserInfo:
    """Legacy UserInfo class for backward compatibility"""
    def __init__(self, user_id: int, taken_course: TakenCourse):
        self.user_id = user_id
        self.taken_course = taken_course  # Single course (legacy)
        
    def to_c5_user_info(self) -> UserInfo:
        """Convert to new C5 UserInfo format"""
        return UserInfo(
            user_id=self.user_id,
            taken_courses=[self.taken_course] if self.taken_course else []
        )
