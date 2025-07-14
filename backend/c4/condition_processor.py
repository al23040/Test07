from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum


class DayOfWeek(Enum):
    MONDAY = "月"
    TUESDAY = "火"
    WEDNESDAY = "水"
    THURSDAY = "木"
    FRIDAY = "金"
    SATURDAY = "土"
    SUNDAY = "日"


class CourseCategory(Enum):
    UNIVERSITY_COMMON = "全学共通科目"
    COMMON_MATH = "共通数理科目"
    LANGUAGE = "言語科目"
    INFORMATICS = "情報科目"
    HEALTH_PE = "体育健康科目"
    MAJOR = "専門科目"
    COMMON_ENGINEERING = "共通工学系教養科目"
    HUMANITIES_SOCIAL = "人文社会系教養科目"


class RequirementType(Enum):
    COMPULSORY = "必修"
    ELECTIVE_COMPULSORY = "選択必修"
    ELECTIVE = "選択"


@dataclass
class Course:
    subject_name: str
    code: str
    grade: Optional[str]
    category: CourseCategory
    requirement: RequirementType
    credit: int
    semester: int
    year: int
    time_slot: Optional[str] = None
    day_of_week: Optional[DayOfWeek] = None
    prerequisites: List[str] = None

    def __post_init__(self):
        if self.prerequisites is None:
            self.prerequisites = []


@dataclass
class UserConditions:
    min_units: int
    max_units: int
    preferences: List[str]
    avoid_first_period: bool = False
    preferred_time_slots: List[str] = None
    preferred_categories: List[CourseCategory] = None
    preferred_days: List[DayOfWeek] = None
    avoided_days: List[DayOfWeek] = None

    def __post_init__(self):
        if self.preferred_time_slots is None:
            self.preferred_time_slots = []
        if self.preferred_categories is None:
            self.preferred_categories = []
        if self.preferred_days is None:
            self.preferred_days = []
        if self.avoided_days is None:
            self.avoided_days = []


@dataclass
class SuggestedCoursePattern:
    semester: int
    year: int
    courses: List[Course]
    total_credits: int
    category_credits: Dict[CourseCategory, int]


@dataclass
class PlanPattern:
    pattern_id: str
    description: str
    yearly_patterns: List[List[SuggestedCoursePattern]]
    total_credits: int
    graduation_feasible: bool


class ConditionProcessor:
    def __init__(self):
        self.graduation_requirements = {
            CourseCategory.UNIVERSITY_COMMON: {'compulsory': 8, 'elective': 0},
            CourseCategory.COMMON_MATH: {'compulsory': 12, 'elective': 0},
            CourseCategory.LANGUAGE: {'compulsory': 8, 'elective': 0},
            CourseCategory.INFORMATICS: {'compulsory': 4, 'elective': 0},
            CourseCategory.HEALTH_PE: {'compulsory': 2, 'elective': 0},
            CourseCategory.MAJOR: {'compulsory': 40, 'elective': 50},
            CourseCategory.COMMON_ENGINEERING: {'compulsory': 0, 'elective': 0},
            CourseCategory.HUMANITIES_SOCIAL: {'compulsory': 0, 'elective': 6}
        }
        self.total_required_credits = 124

    def process_current_semester_recommendation(self,
                                               user_id: int,
                                               user_conditions: UserConditions,
                                               completed_courses: List[Course],
                                               available_courses: List[Course]) -> List[SuggestedCoursePattern]:
        """
        今学期のおすすめ履修登録を表示
        Generate current semester course registration recommendations
        """
        remaining_requirements = self._calculate_remaining_requirements(completed_courses)
        filtered_courses = self._filter_courses_by_conditions(available_courses, user_conditions)

        recommended_courses = self._select_optimal_courses(
            filtered_courses,
            remaining_requirements,
            user_conditions
        )

        current_semester = self._get_current_semester()
        current_year = self._get_current_year()

        pattern = SuggestedCoursePattern(
            semester=current_semester,
            year=current_year,
            courses=recommended_courses,
            total_credits=sum(course.credit for course in recommended_courses),
            category_credits=self._calculate_category_credits(recommended_courses)
        )

        return [pattern]

    def generate_four_year_patterns(self,
                                   user_id: int,
                                   user_conditions: UserConditions,
                                   completed_courses: List[Course],
                                   all_courses: List[Course]) -> List[PlanPattern]:
        """
        4年生までの履修登録パターンを表示
        Generate 4-year course registration patterns
        """
        patterns = []
        remaining_requirements = self._calculate_remaining_requirements(completed_courses)
        available_courses = self._get_available_courses(completed_courses, all_courses)

        # Generate multiple patterns with different strategies
        pattern1 = self._generate_balanced_pattern(available_courses, remaining_requirements, user_conditions)
        pattern2 = self._generate_early_major_pattern(available_courses, remaining_requirements, user_conditions)
        pattern3 = self._generate_flexible_pattern(available_courses, remaining_requirements, user_conditions)

        patterns.extend([pattern1, pattern2, pattern3])

        # Return all patterns, not just feasible ones for testing
        return patterns

    def _calculate_remaining_requirements(self, completed_courses: List[Course]) -> Dict[CourseCategory, Dict[str, int]]:
        """Calculate remaining graduation requirements"""
        completed_credits = {}
        for category in CourseCategory:
            completed_credits[category] = {'compulsory': 0, 'elective': 0}

        for course in completed_courses:
            if course.grade and course.grade not in ['F', 'X']:  # Passed courses
                req_type = 'compulsory' if course.requirement == RequirementType.COMPULSORY else 'elective'
                completed_credits[course.category][req_type] += course.credit

        remaining = {}
        for category in CourseCategory:
            remaining[category] = {
                'compulsory': max(0, self.graduation_requirements[category]['compulsory'] -
                                completed_credits[category]['compulsory']),
                'elective': max(0, self.graduation_requirements[category]['elective'] -
                              completed_credits[category]['elective'])
            }

        return remaining

    def _filter_courses_by_conditions(self, courses: List[Course], conditions: UserConditions) -> List[Course]:
        """Filter courses based on user conditions"""
        filtered = []

        for course in courses:
            # Check first period avoidance
            if conditions.avoid_first_period and course.time_slot and '1' in course.time_slot:
                continue

            # Check preferred time slots
            if conditions.preferred_time_slots:
                if not course.time_slot or not any(slot in course.time_slot for slot in conditions.preferred_time_slots):
                    continue

            # Check preferred categories
            if conditions.preferred_categories:
                if course.category not in conditions.preferred_categories:
                    continue

            # Check day-of-week preferences
            if course.day_of_week:
                # Check avoided days
                if conditions.avoided_days and course.day_of_week in conditions.avoided_days:
                    continue
                
                # Check preferred days (if specified, only include courses on these days)
                if conditions.preferred_days and course.day_of_week not in conditions.preferred_days:
                    continue

            filtered.append(course)

        return filtered

    def _select_optimal_courses(self,
                               available_courses: List[Course],
                               remaining_requirements: Dict[CourseCategory, Dict[str, int]],
                               conditions: UserConditions) -> List[Course]:
        """Select optimal courses for current semester"""
        selected = []
        total_credits = 0

        # First, select required courses
        for course in available_courses:
            if total_credits >= conditions.max_units:
                break

            category_remaining = remaining_requirements[course.category]
            req_type = 'compulsory' if course.requirement == RequirementType.COMPULSORY else 'elective'

            if category_remaining[req_type] > 0 and total_credits + course.credit <= conditions.max_units:
                selected.append(course)
                total_credits += course.credit
                category_remaining[req_type] -= course.credit

        # Then, add elective courses to reach minimum units
        for course in available_courses:
            if course in selected:
                continue

            if total_credits >= conditions.min_units:
                break

            if total_credits + course.credit <= conditions.max_units:
                selected.append(course)
                total_credits += course.credit

        return selected

    def _calculate_category_credits(self, courses: List[Course]) -> Dict[CourseCategory, int]:
        """Calculate credits by category"""
        credits = {}
        for category in CourseCategory:
            credits[category] = sum(course.credit for course in courses if course.category == category)
        return credits

    def _get_available_courses(self, completed_courses: List[Course], all_courses: List[Course]) -> List[Course]:
        """Get courses available for registration"""
        completed_codes = {course.code for course in completed_courses if course.grade not in ['F', 'X']}
        return [course for course in all_courses if course.code not in completed_codes]

    def _generate_balanced_pattern(self,
                                  available_courses: List[Course],
                                  remaining_requirements: Dict[CourseCategory, Dict[str, int]],
                                  conditions: UserConditions) -> PlanPattern:
        """Generate balanced 4-year pattern"""
        # Implementation for balanced course distribution
        yearly_patterns = []
        for year in range(1, 5):
            year_patterns = []
            for semester in range(1, 3):
                # Select courses for this semester
                semester_courses = self._select_semester_courses(
                    available_courses, remaining_requirements, conditions, year, semester
                )
                pattern = SuggestedCoursePattern(
                    semester=semester,
                    year=year,
                    courses=semester_courses,
                    total_credits=sum(c.credit for c in semester_courses),
                    category_credits=self._calculate_category_credits(semester_courses)
                )
                year_patterns.append(pattern)
            yearly_patterns.append(year_patterns)

        total_credits = sum(sum(p.total_credits for p in year) for year in yearly_patterns)

        return PlanPattern(
            pattern_id="pattern1",
            description="バランス型 - 各学期に均等に科目を配置",
            yearly_patterns=yearly_patterns,
            total_credits=total_credits,
            graduation_feasible=total_credits >= self.total_required_credits
        )

    def _generate_early_major_pattern(self,
                                     available_courses: List[Course],
                                     remaining_requirements: Dict[CourseCategory, Dict[str, int]],
                                     conditions: UserConditions) -> PlanPattern:
        """Generate early major focus pattern"""
        # Similar implementation focusing on major courses early
        return PlanPattern(
            pattern_id="pattern2",
            description="専門重視型 - 早期に専門科目を履修",
            yearly_patterns=[],
            total_credits=0,
            graduation_feasible=False
        )

    def _generate_flexible_pattern(self,
                                  available_courses: List[Course],
                                  remaining_requirements: Dict[CourseCategory, Dict[str, int]],
                                  conditions: UserConditions) -> PlanPattern:
        """Generate flexible pattern"""
        # Similar implementation with flexibility focus
        return PlanPattern(
            pattern_id="pattern3",
            description="フレキシブル型 - 柔軟性を重視した履修計画",
            yearly_patterns=[],
            total_credits=0,
            graduation_feasible=False
        )

    def _select_semester_courses(self,
                                available_courses: List[Course],
                                remaining_requirements: Dict[CourseCategory, Dict[str, int]],
                                conditions: UserConditions,
                                year: int,
                                semester: int) -> List[Course]:
        """Select courses for a specific semester"""
        # Implementation for semester-specific course selection
        semester_courses = []
        target_credits = (conditions.min_units + conditions.max_units) // 2

        # Filter courses available in this semester/year
        semester_available = [
            course for course in available_courses
            if course.year <= year and course.semester == semester
        ]

        # Apply condition filtering
        filtered_courses = self._filter_courses_by_conditions(semester_available, conditions)

        # Select optimal courses for this semester
        selected = self._select_optimal_courses(filtered_courses, remaining_requirements, conditions)

        return selected[:6]  # Limit to reasonable number of courses per semester

    def _get_current_semester(self) -> int:
        """Get current semester (1 or 2)"""
        # Implementation to determine current semester
        return 1

    def _get_current_year(self) -> int:
        """Get current academic year"""
        # Implementation to determine current year
        return 1
