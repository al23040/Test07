"""
Taken Course - Updated to use C5 models while maintaining compatibility
"""

# Import from C5 models for enhanced functionality
from c5_models import TakenCourse as C5TakenCourse

# Re-export for compatibility
TakenCourse = C5TakenCourse

# Legacy compatibility class
class LegacyTakenCourse:
    """Legacy TakenCourse class for backward compatibility"""
    def __init__(self, name: str):
        self.name = name
        
    def to_c5_taken_course(self, subject_id: int = None) -> TakenCourse:
        """Convert to new C5 TakenCourse format"""
        return TakenCourse(
            subject_id=subject_id or hash(self.name) % 10000,
            subject_name=self.name,
            evaluation='C',
            credits=2,
            passed=True,
            semester=1,
            year=1
        )
