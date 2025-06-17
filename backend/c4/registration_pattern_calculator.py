from typing import List, Dict, Optional, Set
from .condition_processor import Course, UserConditions, SuggestedCoursePattern, PlanPattern, CourseCategory, RequirementType


class RegistrationPatternCalculator:
    """
    M1 履修パターン算出部 (Registration Pattern Calculator)
    Calculate multiple course registration patterns up to 4th year
    """

    def __init__(self):
        self.semesters_per_year = 2
        self.total_years = 4
        self.min_credits_per_semester = 10
        self.max_credits_per_semester = 25

    def get_registration_pattern(self,
                                user_conditions: UserConditions,
                                completed_courses: List[Course],
                                available_courses: List[Course],
                                necessary_subjects: Dict[str, Course]) -> List[PlanPattern]:
        """
        Calculate multiple course registration patterns up to 4th year

        Args:
            user_conditions: User's desired conditions
            completed_courses: Already completed courses
            available_courses: All available courses in the system
            necessary_subjects: Required subjects for graduation

        Returns:
            List of viable course registration patterns
        """
        patterns = []

        # Calculate remaining graduation requirements
        remaining_reqs = self._calculate_remaining_requirements(completed_courses, necessary_subjects)

        # Filter available courses based on completion status
        eligible_courses = self._get_eligible_courses(completed_courses, available_courses)

        # Generate different pattern strategies
        pattern_strategies = [
            ("standard", self._generate_standard_pattern),
            ("intensive", self._generate_intensive_pattern),
            ("distributed", self._generate_distributed_pattern)
        ]

        for strategy_name, strategy_func in pattern_strategies:
            try:
                pattern = strategy_func(
                    user_conditions,
                    eligible_courses,
                    remaining_reqs,
                    strategy_name
                )
                if pattern and self._validate_pattern(pattern, remaining_reqs):
                    patterns.append(pattern)
            except Exception as e:
                print(f"Error generating {strategy_name} pattern: {e}")
                continue

        return patterns

    def _calculate_remaining_requirements(self,
                                        completed_courses: List[Course],
                                        necessary_subjects: Dict[str, Course]) -> Dict[CourseCategory, Dict[str, int]]:
        """Calculate remaining credits needed for graduation"""
        # Graduation requirements for Information Engineering
        base_requirements = {
            CourseCategory.UNIVERSITY_COMMON: {'compulsory': 8, 'elective': 0},
            CourseCategory.COMMON_MATH: {'compulsory': 12, 'elective': 0},
            CourseCategory.LANGUAGE: {'compulsory': 8, 'elective': 0},
            CourseCategory.INFORMATICS: {'compulsory': 4, 'elective': 0},
            CourseCategory.HEALTH_PE: {'compulsory': 2, 'elective': 0},
            CourseCategory.MAJOR: {'compulsory': 40, 'elective': 50}
        }

        # Calculate completed credits by category
        completed_credits = {}
        for category in CourseCategory:
            completed_credits[category] = {'compulsory': 0, 'elective': 0}

        for course in completed_courses:
            if self._is_course_passed(course):
                req_type = 'compulsory' if course.requirement == RequirementType.COMPULSORY else 'elective'
                completed_credits[course.category][req_type] += course.credit

        # Calculate remaining requirements
        remaining = {}
        for category in CourseCategory:
            remaining[category] = {
                'compulsory': max(0, base_requirements[category]['compulsory'] -
                                completed_credits[category]['compulsory']),
                'elective': max(0, base_requirements[category]['elective'] -
                              completed_credits[category]['elective'])
            }

        return remaining

    def _get_eligible_courses(self,
                             completed_courses: List[Course],
                             available_courses: List[Course]) -> List[Course]:
        """Get courses eligible for registration (not already completed)"""
        completed_codes = {course.code for course in completed_courses if self._is_course_passed(course)}
        return [course for course in available_courses if course.code not in completed_codes]

    def _is_course_passed(self, course: Course) -> bool:
        """Check if a course was passed (not failed or withdrawn)"""
        return course.grade is not None and course.grade not in ['F', 'X', '']

    def _generate_standard_pattern(self,
                                  user_conditions: UserConditions,
                                  eligible_courses: List[Course],
                                  remaining_reqs: Dict[CourseCategory, Dict[str, int]],
                                  strategy_name: str) -> PlanPattern:
        """Generate standard graduation pattern - balanced semester loading"""
        yearly_patterns = []
        working_reqs = {cat: req.copy() for cat, req in remaining_reqs.items()}
        used_courses = set()

        for year in range(1, self.total_years + 1):
            year_patterns = []

            for semester in range(1, self.semesters_per_year + 1):
                semester_courses = self._select_semester_courses(
                    eligible_courses,
                    working_reqs,
                    user_conditions,
                    year,
                    semester,
                    used_courses,
                    target_credits=18  # Standard semester load
                )

                # Update working requirements and used courses
                for course in semester_courses:
                    used_courses.add(course.code)
                    req_type = 'compulsory' if course.requirement == RequirementType.COMPULSORY else 'elective'
                    working_reqs[course.category][req_type] = max(0,
                        working_reqs[course.category][req_type] - course.credit)

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
            pattern_id=f"{strategy_name}_001",
            description="標準パターン - 各学期に均等に科目を配置し、着実に卒業要件を満たす",
            yearly_patterns=yearly_patterns,
            total_credits=total_credits,
            graduation_feasible=self._check_graduation_feasibility(working_reqs, total_credits)
        )

    def _generate_intensive_pattern(self,
                                   user_conditions: UserConditions,
                                   eligible_courses: List[Course],
                                   remaining_reqs: Dict[CourseCategory, Dict[str, int]],
                                   strategy_name: str) -> PlanPattern:
        """Generate intensive pattern - front-loaded with major courses"""
        yearly_patterns = []
        working_reqs = {cat: req.copy() for cat, req in remaining_reqs.items()}
        used_courses = set()

        # Prioritize major courses in early years
        major_priority_years = [1, 2]

        for year in range(1, self.total_years + 1):
            year_patterns = []
            target_credits = 20 if year in major_priority_years else 16

            for semester in range(1, self.semesters_per_year + 1):
                # Prioritize major courses in early years
                priority_categories = [CourseCategory.MAJOR] if year in major_priority_years else []

                semester_courses = self._select_semester_courses(
                    eligible_courses,
                    working_reqs,
                    user_conditions,
                    year,
                    semester,
                    used_courses,
                    target_credits=target_credits,
                    priority_categories=priority_categories
                )

                # Update working requirements and used courses
                for course in semester_courses:
                    used_courses.add(course.code)
                    req_type = 'compulsory' if course.requirement == RequirementType.COMPULSORY else 'elective'
                    working_reqs[course.category][req_type] = max(0,
                        working_reqs[course.category][req_type] - course.credit)

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
            pattern_id=f"{strategy_name}_002",
            description="集中パターン - 前半に専門科目を集中し、研究室配属に向けて準備",
            yearly_patterns=yearly_patterns,
            total_credits=total_credits,
            graduation_feasible=self._check_graduation_feasibility(working_reqs, total_credits)
        )

    def _generate_distributed_pattern(self,
                                     user_conditions: UserConditions,
                                     eligible_courses: List[Course],
                                     remaining_reqs: Dict[CourseCategory, Dict[str, int]],
                                     strategy_name: str) -> PlanPattern:
        """Generate distributed pattern - spread requirements evenly"""
        yearly_patterns = []
        working_reqs = {cat: req.copy() for cat, req in remaining_reqs.items()}
        used_courses = set()

        for year in range(1, self.total_years + 1):
            year_patterns = []

            for semester in range(1, self.semesters_per_year + 1):
                semester_courses = self._select_semester_courses(
                    eligible_courses,
                    working_reqs,
                    user_conditions,
                    year,
                    semester,
                    used_courses,
                    target_credits=15,  # Lighter semester load
                    distribute_categories=True
                )

                # Update working requirements and used courses
                for course in semester_courses:
                    used_courses.add(course.code)
                    req_type = 'compulsory' if course.requirement == RequirementType.COMPULSORY else 'elective'
                    working_reqs[course.category][req_type] = max(0,
                        working_reqs[course.category][req_type] - course.credit)

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
            pattern_id=f"{strategy_name}_003",
            description="分散パターン - 各カテゴリの科目を均等に配置し、学習負荷を平準化",
            yearly_patterns=yearly_patterns,
            total_credits=total_credits,
            graduation_feasible=self._check_graduation_feasibility(working_reqs, total_credits)
        )

    def _select_semester_courses(self,
                                eligible_courses: List[Course],
                                remaining_reqs: Dict[CourseCategory, Dict[str, int]],
                                user_conditions: UserConditions,
                                year: int,
                                semester: int,
                                used_courses: Set[str],
                                target_credits: int = 18,
                                priority_categories: List[CourseCategory] = None,
                                distribute_categories: bool = False) -> List[Course]:
        """Select optimal courses for a specific semester"""
        available_for_semester = [
            course for course in eligible_courses
            if (course.code not in used_courses and
                course.year <= year and
                self._check_prerequisites(course, used_courses))
        ]

        selected_courses = []
        current_credits = 0

        # First priority: Required courses
        for category in CourseCategory:
            if remaining_reqs[category]['compulsory'] > 0:
                category_courses = [
                    c for c in available_for_semester
                    if (c.category == category and
                        c.requirement == RequirementType.COMPULSORY and
                        current_credits + c.credit <= min(target_credits, user_conditions.max_units))
                ]

                # Sort by year (take earlier year courses first)
                category_courses.sort(key=lambda x: x.year)

                for course in category_courses[:2]:  # Limit courses per category per semester
                    selected_courses.append(course)
                    current_credits += course.credit
                    if current_credits >= target_credits:
                        break

        # Second priority: Priority categories (if specified)
        if priority_categories and current_credits < target_credits:
            for category in priority_categories:
                category_courses = [
                    c for c in available_for_semester
                    if (c.category == category and
                        c not in selected_courses and
                        current_credits + c.credit <= min(target_credits, user_conditions.max_units))
                ]

                for course in category_courses[:2]:
                    selected_courses.append(course)
                    current_credits += course.credit
                    if current_credits >= target_credits:
                        break

        # Third priority: Fill to minimum credits
        remaining_courses = [
            c for c in available_for_semester
            if (c not in selected_courses and
                current_credits + c.credit <= user_conditions.max_units)
        ]

        # Apply user condition filtering
        remaining_courses = self._filter_by_user_conditions(remaining_courses, user_conditions)

        # Sort by priority (required first, then by category need)
        remaining_courses.sort(key=lambda x: self._course_priority_score(x, remaining_reqs))

        for course in remaining_courses:
            if current_credits >= user_conditions.min_units:
                break
            if current_credits + course.credit <= user_conditions.max_units:
                selected_courses.append(course)
                current_credits += course.credit

        return selected_courses

    def _check_prerequisites(self, course: Course, completed_course_codes: Set[str]) -> bool:
        """Check if course prerequisites are satisfied"""
        if not course.prerequisites:
            return True
        return all(prereq in completed_course_codes for prereq in course.prerequisites)

    def _filter_by_user_conditions(self, courses: List[Course], conditions: UserConditions) -> List[Course]:
        """Filter courses based on user preferences"""
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

            filtered.append(course)

        return filtered

    def _course_priority_score(self, course: Course, remaining_reqs: Dict[CourseCategory, Dict[str, int]]) -> int:
        """Calculate priority score for course selection"""
        score = 0

        # Higher priority for required courses
        if course.requirement == RequirementType.COMPULSORY:
            score += 100

        # Higher priority for categories with remaining requirements
        req_type = 'compulsory' if course.requirement == RequirementType.COMPULSORY else 'elective'
        if remaining_reqs[course.category][req_type] > 0:
            score += 50

        # Prefer lower year courses (foundational)
        score += (5 - course.year) * 10

        return score

    def _calculate_category_credits(self, courses: List[Course]) -> Dict[CourseCategory, int]:
        """Calculate total credits by category"""
        credits = {}
        for category in CourseCategory:
            credits[category] = sum(course.credit for course in courses if course.category == category)
        return credits

    def _validate_pattern(self, pattern: PlanPattern, remaining_reqs: Dict[CourseCategory, Dict[str, int]]) -> bool:
        """Validate if pattern meets graduation requirements"""
        if not pattern.graduation_feasible:
            return False

        # Check minimum total credits
        if pattern.total_credits < 124:  # Minimum for graduation
            return False

        # Check if each semester has reasonable credit load
        for year_patterns in pattern.yearly_patterns:
            for semester_pattern in year_patterns:
                if semester_pattern.total_credits > 25:  # Maximum allowed per semester
                    return False
                if semester_pattern.total_credits < 10 and len(semester_pattern.courses) > 0:  # Minimum reasonable load
                    return False

        return True

    def _check_graduation_feasibility(self, remaining_reqs: Dict[CourseCategory, Dict[str, int]], total_credits: int) -> bool:
        """Check if the pattern enables graduation"""
        # Check if all required credits are covered
        total_remaining = sum(
            sum(reqs.values()) for reqs in remaining_reqs.values()
        )

        return total_remaining == 0 and total_credits >= 124
