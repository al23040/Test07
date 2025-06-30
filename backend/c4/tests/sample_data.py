"""
Sample data generator for testing C4 condition processing component
"""

from typing import List, Dict
from c4.condition_processor import Course, CourseCategory, RequirementType, DayOfWeek


def generate_comprehensive_course_catalog() -> List[Course]:
    """Generate a comprehensive course catalog for testing"""
    courses = []

    # Year 1 Courses
    # Major courses (専門科目) - Year 1
    courses.extend([
        Course("プログラミング基礎", "CS101", None, CourseCategory.MAJOR, RequirementType.COMPULSORY, 2, 1, 1, "2-3", DayOfWeek.MONDAY, []),
        Course("情報技術概論", "CS102", None, CourseCategory.MAJOR, RequirementType.COMPULSORY, 2, 2, 1, "2-3", DayOfWeek.TUESDAY, []),
        Course("コンピュータ基礎", "CS103", None, CourseCategory.MAJOR, RequirementType.COMPULSORY, 2, 1, 1, "4-5", DayOfWeek.WEDNESDAY, []),
        Course("情報数学", "CS104", None, CourseCategory.MAJOR, RequirementType.ELECTIVE, 2, 2, 1, "3-4", DayOfWeek.THURSDAY, []),
    ])

    # Year 2 Courses
    # Major courses (専門科目) - Year 2
    courses.extend([
        Course("データ構造とアルゴリズム", "CS201", None, CourseCategory.MAJOR, RequirementType.COMPULSORY, 2, 1, 2, "3-4", DayOfWeek.FRIDAY, ["CS101"]),
        Course("オブジェクト指向プログラミング", "CS202", None, CourseCategory.MAJOR, RequirementType.COMPULSORY, 2, 2, 2, "2-3", DayOfWeek.MONDAY, ["CS101"]),
        Course("システムプログラミング", "CS203", None, CourseCategory.MAJOR, RequirementType.ELECTIVE, 2, 1, 2, "4-5", DayOfWeek.TUESDAY, ["CS103"]),
        Course("Web技術基礎", "CS204", None, CourseCategory.MAJOR, RequirementType.ELECTIVE, 2, 2, 2, "3-4", DayOfWeek.WEDNESDAY, ["CS102"]),
        Course("データベース基礎", "CS205", None, CourseCategory.MAJOR, RequirementType.ELECTIVE, 2, 1, 2, "2-3", DayOfWeek.THURSDAY, ["CS201"]),
    ])

    # Year 3 Courses
    # Major courses (専門科目) - Year 3
    courses.extend([
        Course("ソフトウェア工学", "CS301", None, CourseCategory.MAJOR, RequirementType.COMPULSORY, 2, 1, 3, "2-3", DayOfWeek.FRIDAY, ["CS201", "CS202"]),
        Course("データベース設計", "CS302", None, CourseCategory.MAJOR, RequirementType.ELECTIVE, 2, 2, 3, "3-4", DayOfWeek.MONDAY, ["CS205"]),
        Course("ネットワークプログラミング", "CS303", None, CourseCategory.MAJOR, RequirementType.ELECTIVE, 2, 1, 3, "4-5", DayOfWeek.TUESDAY, ["CS204"]),
        Course("機械学習基礎", "CS304", None, CourseCategory.MAJOR, RequirementType.ELECTIVE, 2, 2, 3, "2-3", DayOfWeek.WEDNESDAY, ["CS201"]),
        Course("情報セキュリティ", "CS305", None, CourseCategory.MAJOR, RequirementType.ELECTIVE, 2, 1, 3, "3-4", DayOfWeek.THURSDAY, ["CS203"]),
    ])

    # Year 4 Courses
    # Major courses (専門科目) - Year 4
    courses.extend([
        Course("卒業研究I", "CS401", None, CourseCategory.MAJOR, RequirementType.COMPULSORY, 4, 1, 4, "1-2", DayOfWeek.FRIDAY, ["CS301"]),
        Course("卒業研究II", "CS402", None, CourseCategory.MAJOR, RequirementType.COMPULSORY, 4, 2, 4, "1-2", DayOfWeek.MONDAY, ["CS401"]),
        Course("プロジェクト管理", "CS403", None, CourseCategory.MAJOR, RequirementType.ELECTIVE, 2, 1, 4, "3-4", DayOfWeek.TUESDAY, ["CS301"]),
        Course("高度システム開発", "CS404", None, CourseCategory.MAJOR, RequirementType.ELECTIVE, 2, 2, 4, "3-4", DayOfWeek.WEDNESDAY, ["CS303"]),
    ])

    # Common Math courses (共通数理科目)
    courses.extend([
        Course("微分積分学I", "MATH101", None, CourseCategory.COMMON_MATH, RequirementType.COMPULSORY, 2, 1, 1, "2-3", DayOfWeek.TUESDAY, []),
        Course("微分積分学II", "MATH102", None, CourseCategory.COMMON_MATH, RequirementType.COMPULSORY, 2, 2, 1, "2-3", DayOfWeek.WEDNESDAY, ["MATH101"]),
        Course("線形代数学I", "MATH201", None, CourseCategory.COMMON_MATH, RequirementType.COMPULSORY, 2, 1, 1, "3-4", DayOfWeek.THURSDAY, []),
        Course("線形代数学II", "MATH202", None, CourseCategory.COMMON_MATH, RequirementType.COMPULSORY, 2, 2, 1, "3-4", DayOfWeek.FRIDAY, ["MATH201"]),
        Course("統計学", "MATH301", None, CourseCategory.COMMON_MATH, RequirementType.COMPULSORY, 2, 1, 2, "4-5", DayOfWeek.MONDAY, ["MATH102"]),
        Course("確率論", "MATH302", None, CourseCategory.COMMON_MATH, RequirementType.COMPULSORY, 2, 2, 2, "4-5", DayOfWeek.TUESDAY, ["MATH202"]),
    ])

    # Language courses (言語科目)
    courses.extend([
        Course("英語I", "ENG101", None, CourseCategory.LANGUAGE, RequirementType.COMPULSORY, 2, 1, 1, "2-3", DayOfWeek.WEDNESDAY, []),
        Course("英語II", "ENG102", None, CourseCategory.LANGUAGE, RequirementType.COMPULSORY, 2, 2, 1, "2-3", DayOfWeek.THURSDAY, ["ENG101"]),
        Course("英語III", "ENG201", None, CourseCategory.LANGUAGE, RequirementType.COMPULSORY, 2, 1, 2, "3-4", DayOfWeek.FRIDAY, ["ENG102"]),
        Course("英語IV", "ENG202", None, CourseCategory.LANGUAGE, RequirementType.COMPULSORY, 2, 2, 2, "3-4", DayOfWeek.MONDAY, ["ENG201"]),
        Course("第二外国語I", "LANG101", None, CourseCategory.LANGUAGE, RequirementType.ELECTIVE, 2, 1, 1, "4-5", DayOfWeek.TUESDAY, []),
        Course("第二外国語II", "LANG102", None, CourseCategory.LANGUAGE, RequirementType.ELECTIVE, 2, 2, 1, "4-5", DayOfWeek.WEDNESDAY, ["LANG101"]),
    ])

    # University common courses (全学共通科目)
    courses.extend([
        Course("情報リテラシー", "GEN101", None, CourseCategory.UNIVERSITY_COMMON, RequirementType.COMPULSORY, 2, 1, 1, "3-4", DayOfWeek.THURSDAY, []),
        Course("キャリアデザイン", "GEN102", None, CourseCategory.UNIVERSITY_COMMON, RequirementType.COMPULSORY, 2, 2, 1, "3-4", DayOfWeek.FRIDAY, []),
        Course("科学技術史", "GEN201", None, CourseCategory.UNIVERSITY_COMMON, RequirementType.COMPULSORY, 2, 1, 2, "4-5", DayOfWeek.WEDNESDAY, []),
        Course("技術者倫理", "GEN202", None, CourseCategory.UNIVERSITY_COMMON, RequirementType.COMPULSORY, 2, 2, 2, "4-5", DayOfWeek.THURSDAY, []),
    ])

    # PE courses (体育健康科目)
    courses.extend([
        Course("体育実技I", "PE101", None, CourseCategory.HEALTH_PE, RequirementType.COMPULSORY, 1, 1, 1, "2-3", DayOfWeek.FRIDAY, []),
        Course("体育実技II", "PE102", None, CourseCategory.HEALTH_PE, RequirementType.COMPULSORY, 1, 2, 1, "2-3", DayOfWeek.MONDAY, []),
    ])

    # Informatics courses (情報科目)
    courses.extend([
        Course("情報基礎", "INFO101", None, CourseCategory.INFORMATICS, RequirementType.COMPULSORY, 2, 1, 1, "3-4", DayOfWeek.MONDAY, []),
        Course("情報処理演習", "INFO102", None, CourseCategory.INFORMATICS, RequirementType.COMPULSORY, 2, 2, 1, "3-4", DayOfWeek.TUESDAY, ["INFO101"]),
    ])

    return courses


def generate_sample_completed_courses() -> List[Course]:
    """Generate sample completed courses for a 2nd year student"""
    return [
        # Year 1 completed courses
        Course("プログラミング基礎", "CS101", "A", CourseCategory.MAJOR, RequirementType.COMPULSORY, 2, 1, 1, "2-3", DayOfWeek.MONDAY, []),
        Course("情報技術概論", "CS102", "B", CourseCategory.MAJOR, RequirementType.COMPULSORY, 2, 2, 1, "2-3", DayOfWeek.TUESDAY, []),
        Course("コンピュータ基礎", "CS103", "A", CourseCategory.MAJOR, RequirementType.COMPULSORY, 2, 1, 1, "4-5", DayOfWeek.WEDNESDAY, []),

        Course("微分積分学I", "MATH101", "B", CourseCategory.COMMON_MATH, RequirementType.COMPULSORY, 2, 1, 1, "2-3", DayOfWeek.TUESDAY, []),
        Course("微分積分学II", "MATH102", "A", CourseCategory.COMMON_MATH, RequirementType.COMPULSORY, 2, 2, 1, "2-3", DayOfWeek.WEDNESDAY, ["MATH101"]),
        Course("線形代数学I", "MATH201", "B", CourseCategory.COMMON_MATH, RequirementType.COMPULSORY, 2, 1, 1, "3-4", DayOfWeek.THURSDAY, []),
        Course("線形代数学II", "MATH202", "A", CourseCategory.COMMON_MATH, RequirementType.COMPULSORY, 2, 2, 1, "3-4", DayOfWeek.FRIDAY, ["MATH201"]),

        Course("英語I", "ENG101", "A", CourseCategory.LANGUAGE, RequirementType.COMPULSORY, 2, 1, 1, "2-3", DayOfWeek.WEDNESDAY, []),
        Course("英語II", "ENG102", "B", CourseCategory.LANGUAGE, RequirementType.COMPULSORY, 2, 2, 1, "2-3", DayOfWeek.THURSDAY, ["ENG101"]),

        Course("情報リテラシー", "GEN101", "A", CourseCategory.UNIVERSITY_COMMON, RequirementType.COMPULSORY, 2, 1, 1, "3-4", DayOfWeek.THURSDAY, []),
        Course("キャリアデザイン", "GEN102", "A", CourseCategory.UNIVERSITY_COMMON, RequirementType.COMPULSORY, 2, 2, 1, "3-4", DayOfWeek.FRIDAY, []),

        Course("体育実技I", "PE101", "A", CourseCategory.HEALTH_PE, RequirementType.COMPULSORY, 1, 1, 1, "2-3", DayOfWeek.FRIDAY, []),
        Course("体育実技II", "PE102", "A", CourseCategory.HEALTH_PE, RequirementType.COMPULSORY, 1, 2, 1, "2-3", DayOfWeek.MONDAY, []),

        Course("情報基礎", "INFO101", "B", CourseCategory.INFORMATICS, RequirementType.COMPULSORY, 2, 1, 1, "3-4", DayOfWeek.MONDAY, []),
        Course("情報処理演習", "INFO102", "A", CourseCategory.INFORMATICS, RequirementType.COMPULSORY, 2, 2, 1, "3-4", DayOfWeek.TUESDAY, ["INFO101"]),
    ]


def get_graduation_requirements() -> Dict[str, Dict[str, int]]:
    """Get graduation requirements for Information Engineering"""
    return {
        'major_required': 16,  # 専門必修
        'major_elective': 50,  # 専門選択
        'common_math': 12,     # 共通数理
        'language': 8,         # 言語
        'university_common': 8, # 全学共通
        'informatics': 4,      # 情報
        'health_pe': 2,        # 体育健康
        'total_minimum': 124   # 卒業最低単位
    }
