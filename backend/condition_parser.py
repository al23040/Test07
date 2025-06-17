from typing import List, Dict, Optional, Any, Callable
from condition_processor import Course, UserConditions, SuggestedCoursePattern, CourseCategory
from registration_pattern_calculator import RegistrationPatternCalculator


class ConditionParser:
    """
    M2 条件変換部 (Condition Parser)
    Select and execute appropriate course registration pattern processing methods based on desired conditions
    """
    
    def __init__(self):
        self.pattern_calculator = RegistrationPatternCalculator()
        self.condition_handlers = {
            'avoid_first_period': self.get_registration_pattern_avoiding_first_hour_class,
            'prefer_afternoon': self._handle_afternoon_preference,
            'intensive_major': self._handle_intensive_major,
            'light_load': self._handle_light_load,
            'research_focused': self._handle_research_focused,
            'balanced': self._handle_balanced_approach
        }
    
    def parse_and_execute(self, 
                         conditions: Dict[str, Any],
                         user_id: int,
                         completed_courses: List[Course],
                         available_courses: List[Course],
                         necessary_subjects: Dict[str, Course]) -> List[SuggestedCoursePattern]:
        """
        Parse user conditions and execute appropriate pattern generation method
        
        Args:
            conditions: User's desired conditions as dictionary
            user_id: User identification
            completed_courses: Already completed courses
            available_courses: All available courses
            necessary_subjects: Required subjects for graduation
            
        Returns:
            List of suggested course patterns based on conditions
        """
        # Convert conditions dictionary to UserConditions object
        user_conditions = self._parse_conditions_to_object(conditions)
        
        # Determine which condition handlers to apply
        active_handlers = self._identify_active_handlers(conditions)
        
        # Execute appropriate handlers
        all_patterns = []
        for handler_name in active_handlers:
            if handler_name in self.condition_handlers:
                handler = self.condition_handlers[handler_name]
                try:
                    patterns = handler(
                        user_conditions,
                        completed_courses,
                        available_courses,
                        necessary_subjects
                    )
                    all_patterns.extend(patterns)
                except Exception as e:
                    print(f"Error executing handler {handler_name}: {e}")
                    continue
        
        # If no specific handlers were triggered, use default balanced approach
        if not all_patterns:
            all_patterns = self._handle_balanced_approach(
                user_conditions,
                completed_courses,
                available_courses,
                necessary_subjects
            )
        
        # Remove duplicates and rank patterns
        unique_patterns = self._deduplicate_patterns(all_patterns)
        ranked_patterns = self._rank_patterns(unique_patterns, user_conditions)
        
        return ranked_patterns[:5]  # Return top 5 patterns
    
    def get_registration_pattern_avoiding_first_hour_class(self,
                                                          user_conditions: UserConditions,
                                                          completed_courses: List[Course],
                                                          available_courses: List[Course],
                                                          necessary_subjects: Dict[str, Course]) -> List[SuggestedCoursePattern]:
        """
        Calculate course registration patterns with condition "avoiding first-period classes"
        Specific algorithm mentioned in specifications
        """
        # Set avoid first period flag
        user_conditions.avoid_first_period = True
        
        # Filter out first period courses from available courses
        filtered_courses = [
            course for course in available_courses
            if not (course.time_slot and '1' in course.time_slot)
        ]
        
        # Generate patterns using filtered courses
        patterns = self.pattern_calculator.get_registration_pattern(
            user_conditions,
            completed_courses,
            filtered_courses,
            necessary_subjects
        )
        
        # Convert PlanPattern to SuggestedCoursePattern for current semester
        current_semester_patterns = []
        for pattern in patterns:
            if pattern.yearly_patterns and len(pattern.yearly_patterns) > 0:
                # Get first year, first semester pattern
                first_year_first_semester = pattern.yearly_patterns[0][0]
                
                # Create modified pattern with "no first period" description
                modified_pattern = SuggestedCoursePattern(
                    semester=first_year_first_semester.semester,
                    year=first_year_first_semester.year,
                    courses=first_year_first_semester.courses,
                    total_credits=first_year_first_semester.total_credits,
                    category_credits=first_year_first_semester.category_credits
                )
                current_semester_patterns.append(modified_pattern)
        
        return current_semester_patterns
    
    def _parse_conditions_to_object(self, conditions: Dict[str, Any]) -> UserConditions:
        """Convert conditions dictionary to UserConditions object"""
        return UserConditions(
            min_units=conditions.get('min_units', 12),
            max_units=conditions.get('max_units', 22),
            preferences=conditions.get('preferences', []),
            avoid_first_period=conditions.get('avoid_first_period', False),
            preferred_time_slots=conditions.get('preferred_time_slots', []),
            preferred_categories=self._parse_preferred_categories(conditions.get('preferred_categories', []))
        )
    
    def _parse_preferred_categories(self, category_strings: List[str]) -> List[CourseCategory]:
        """Convert category strings to CourseCategory enums"""
        category_mapping = {
            '全学共通科目': CourseCategory.UNIVERSITY_COMMON,
            '共通数理科目': CourseCategory.COMMON_MATH,
            '言語科目': CourseCategory.LANGUAGE,
            '情報科目': CourseCategory.INFORMATICS,
            '体育健康科目': CourseCategory.HEALTH_PE,
            '専門科目': CourseCategory.MAJOR
        }
        
        return [category_mapping[cat] for cat in category_strings if cat in category_mapping]
    
    def _identify_active_handlers(self, conditions: Dict[str, Any]) -> List[str]:
        """Identify which condition handlers should be activated"""
        active_handlers = []
        
        # Check for specific conditions
        if conditions.get('avoid_first_period', False):
            active_handlers.append('avoid_first_period')
        
        if 'afternoon' in conditions.get('preferences', []):
            active_handlers.append('prefer_afternoon')
        
        if 'intensive_major' in conditions.get('preferences', []):
            active_handlers.append('intensive_major')
        
        if conditions.get('max_units', 22) <= 15:
            active_handlers.append('light_load')
        
        if '研究室' in conditions.get('preferences', []) or 'research' in conditions.get('preferences', []):
            active_handlers.append('research_focused')
        
        # Default to balanced if no specific conditions
        if not active_handlers:
            active_handlers.append('balanced')
        
        return active_handlers
    
    def _handle_afternoon_preference(self,
                                    user_conditions: UserConditions,
                                    completed_courses: List[Course],
                                    available_courses: List[Course],
                                    necessary_subjects: Dict[str, Course]) -> List[SuggestedCoursePattern]:
        """Handle preference for afternoon classes"""
        # Set preferred time slots to afternoon
        user_conditions.preferred_time_slots = ['3', '4', '5']  # 3rd, 4th, 5th periods
        
        # Filter courses to afternoon slots
        afternoon_courses = [
            course for course in available_courses
            if course.time_slot and any(slot in course.time_slot for slot in ['3', '4', '5'])
        ]
        
        patterns = self.pattern_calculator.get_registration_pattern(
            user_conditions,
            completed_courses,
            afternoon_courses,
            necessary_subjects
        )
        
        return self._convert_plan_patterns_to_suggested(patterns)
    
    def _handle_intensive_major(self,
                               user_conditions: UserConditions,
                               completed_courses: List[Course],
                               available_courses: List[Course],
                               necessary_subjects: Dict[str, Course]) -> List[SuggestedCoursePattern]:
        """Handle intensive major course preference"""
        # Set preferred categories to major subjects
        user_conditions.preferred_categories = [CourseCategory.MAJOR]
        
        # Increase max units to allow for intensive schedule
        user_conditions.max_units = min(25, user_conditions.max_units + 3)
        
        patterns = self.pattern_calculator.get_registration_pattern(
            user_conditions,
            completed_courses,
            available_courses,
            necessary_subjects
        )
        
        return self._convert_plan_patterns_to_suggested(patterns)
    
    def _handle_light_load(self,
                          user_conditions: UserConditions,
                          completed_courses: List[Course],
                          available_courses: List[Course],
                          necessary_subjects: Dict[str, Course]) -> List[SuggestedCoursePattern]:
        """Handle light course load preference"""
        # Reduce max units for lighter load
        user_conditions.max_units = min(user_conditions.max_units, 16)
        user_conditions.min_units = min(user_conditions.min_units, 12)
        
        patterns = self.pattern_calculator.get_registration_pattern(
            user_conditions,
            completed_courses,
            available_courses,
            necessary_subjects
        )
        
        return self._convert_plan_patterns_to_suggested(patterns)
    
    def _handle_research_focused(self,
                                user_conditions: UserConditions,
                                completed_courses: List[Course],
                                available_courses: List[Course],
                                necessary_subjects: Dict[str, Course]) -> List[SuggestedCoursePattern]:
        """Handle research-focused preference (preparing for lab assignment)"""
        # Prioritize major courses and advanced subjects
        user_conditions.preferred_categories = [CourseCategory.MAJOR, CourseCategory.INFORMATICS]
        
        # Filter for advanced courses (3rd year and above)
        advanced_courses = [
            course for course in available_courses
            if course.year >= 3 or course.category in [CourseCategory.MAJOR, CourseCategory.INFORMATICS]
        ]
        
        patterns = self.pattern_calculator.get_registration_pattern(
            user_conditions,
            completed_courses,
            advanced_courses,
            necessary_subjects
        )
        
        return self._convert_plan_patterns_to_suggested(patterns)
    
    def _handle_balanced_approach(self,
                                 user_conditions: UserConditions,
                                 completed_courses: List[Course],
                                 available_courses: List[Course],
                                 necessary_subjects: Dict[str, Course]) -> List[SuggestedCoursePattern]:
        """Handle balanced course selection approach"""
        patterns = self.pattern_calculator.get_registration_pattern(
            user_conditions,
            completed_courses,
            available_courses,
            necessary_subjects
        )
        
        return self._convert_plan_patterns_to_suggested(patterns)
    
    def _convert_plan_patterns_to_suggested(self, plan_patterns: List) -> List[SuggestedCoursePattern]:
        """Convert PlanPattern objects to SuggestedCoursePattern objects"""
        suggested_patterns = []
        
        for plan_pattern in plan_patterns:
            if hasattr(plan_pattern, 'yearly_patterns') and plan_pattern.yearly_patterns:
                # Get current semester pattern (first year, first semester)
                current_pattern = plan_pattern.yearly_patterns[0][0]
                suggested_patterns.append(current_pattern)
        
        return suggested_patterns
    
    def _deduplicate_patterns(self, patterns: List[SuggestedCoursePattern]) -> List[SuggestedCoursePattern]:
        """Remove duplicate patterns based on course combinations"""
        unique_patterns = []
        seen_combinations = set()
        
        for pattern in patterns:
            # Create signature based on course codes
            course_codes = tuple(sorted([course.code for course in pattern.courses]))
            
            if course_codes not in seen_combinations:
                seen_combinations.add(course_codes)
                unique_patterns.append(pattern)
        
        return unique_patterns
    
    def _rank_patterns(self, patterns: List[SuggestedCoursePattern], user_conditions: UserConditions) -> List[SuggestedCoursePattern]:
        """Rank patterns based on how well they match user conditions"""
        def pattern_score(pattern: SuggestedCoursePattern) -> float:
            score = 0.0
            
            # Credit range preference
            if user_conditions.min_units <= pattern.total_credits <= user_conditions.max_units:
                score += 10.0
            else:
                # Penalty for being outside preferred range
                score -= abs(pattern.total_credits - (user_conditions.min_units + user_conditions.max_units) / 2)
            
            # Category preference
            if user_conditions.preferred_categories:
                preferred_credits = sum(
                    pattern.category_credits.get(cat, 0) 
                    for cat in user_conditions.preferred_categories
                )
                score += preferred_credits * 0.5
            
            # Time slot preference
            if user_conditions.preferred_time_slots:
                matching_time_courses = sum(
                    1 for course in pattern.courses
                    if course.time_slot and any(slot in course.time_slot for slot in user_conditions.preferred_time_slots)
                )
                score += matching_time_courses * 2.0
            
            # Avoid first period penalty
            if user_conditions.avoid_first_period:
                first_period_courses = sum(
                    1 for course in pattern.courses
                    if course.time_slot and '1' in course.time_slot
                )
                score -= first_period_courses * 5.0
            
            # Balance bonus (diverse categories)
            category_count = sum(1 for credits in pattern.category_credits.values() if credits > 0)
            score += category_count * 1.0
            
            return score
        
        # Sort patterns by score (highest first)
        return sorted(patterns, key=pattern_score, reverse=True)