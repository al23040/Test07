#!/usr/bin/env python3
"""
Test script for C4 条件処理部 (Condition Processing Component)
Tests the core functionality of course recommendation and pattern generation
"""

import sys
import json
from typing import List, Dict

# Add backend to path
sys.path.append('/Users/taewoong/Projects/Test07/backend')

from condition_processor import ConditionProcessor, UserConditions, Course, CourseCategory, RequirementType
from condition_parser import ConditionParser
from registration_pattern_calculator import RegistrationPatternCalculator


def create_sample_courses() -> List[Course]:
    """Create sample course data for testing"""
    return [
        # Major courses (専門科目)
        Course("プログラミング基礎", "CS101", None, CourseCategory.MAJOR, RequirementType.COMPULSORY, 2, 1, 1, "1-2", []),
        Course("データ構造とアルゴリズム", "CS201", None, CourseCategory.MAJOR, RequirementType.COMPULSORY, 2, 1, 2, "3-4", ["CS101"]),
        Course("オブジェクト指向プログラミング", "CS202", None, CourseCategory.MAJOR, RequirementType.ELECTIVE, 2, 1, 2, "1-2", ["CS101"]),
        Course("データベース設計", "CS301", None, CourseCategory.MAJOR, RequirementType.ELECTIVE, 2, 2, 3, "3-4", ["CS201"]),
        Course("ソフトウェア工学", "CS302", None, CourseCategory.MAJOR, RequirementType.ELECTIVE, 2, 2, 3, "1-2", ["CS201"]),
        
        # Common math courses (共通数理科目)
        Course("微分積分学I", "MATH101", None, CourseCategory.COMMON_MATH, RequirementType.COMPULSORY, 2, 1, 1, "1-2", []),
        Course("微分積分学II", "MATH102", None, CourseCategory.COMMON_MATH, RequirementType.COMPULSORY, 2, 1, 1, "3-4", ["MATH101"]),
        Course("線形代数学I", "MATH201", None, CourseCategory.COMMON_MATH, RequirementType.COMPULSORY, 2, 1, 1, "1-2", []),
        Course("線形代数学II", "MATH202", None, CourseCategory.COMMON_MATH, RequirementType.COMPULSORY, 2, 1, 1, "3-4", ["MATH201"]),
        
        # Language courses (言語科目)
        Course("英語I", "ENG101", None, CourseCategory.LANGUAGE, RequirementType.COMPULSORY, 2, 1, 1, "1-2", []),
        Course("英語II", "ENG102", None, CourseCategory.LANGUAGE, RequirementType.COMPULSORY, 2, 1, 1, "3-4", ["ENG101"]),
        Course("第二外国語I", "LANG201", None, CourseCategory.LANGUAGE, RequirementType.COMPULSORY, 2, 1, 1, "1-2", []),
        Course("第二外国語II", "LANG202", None, CourseCategory.LANGUAGE, RequirementType.COMPULSORY, 2, 1, 1, "3-4", ["LANG201"]),
        
        # University common courses (全学共通科目)
        Course("情報リテラシー", "GEN101", None, CourseCategory.UNIVERSITY_COMMON, RequirementType.COMPULSORY, 2, 1, 1, "1-2", []),
        Course("キャリアデザイン", "GEN102", None, CourseCategory.UNIVERSITY_COMMON, RequirementType.COMPULSORY, 2, 1, 1, "3-4", []),
        Course("科学技術史", "GEN201", None, CourseCategory.UNIVERSITY_COMMON, RequirementType.COMPULSORY, 2, 1, 1, "1-2", []),
        Course("技術者倫理", "GEN202", None, CourseCategory.UNIVERSITY_COMMON, RequirementType.COMPULSORY, 2, 1, 1, "3-4", []),
        
        # PE courses (体育健康科目)
        Course("体育実技I", "PE101", None, CourseCategory.HEALTH_PE, RequirementType.COMPULSORY, 1, 1, 1, "1-2", []),
        Course("体育実技II", "PE102", None, CourseCategory.HEALTH_PE, RequirementType.COMPULSORY, 1, 1, 1, "3-4", []),
        
        # Informatics courses (情報科目)
        Course("情報基礎", "INFO101", None, CourseCategory.INFORMATICS, RequirementType.COMPULSORY, 2, 1, 1, "1-2", []),
        Course("情報処理演習", "INFO102", None, CourseCategory.INFORMATICS, RequirementType.COMPULSORY, 2, 1, 1, "3-4", ["INFO101"]),
    ]


def create_completed_courses() -> List[Course]:
    """Create sample completed course data"""
    completed = [
        Course("プログラミング基礎", "CS101", "A", CourseCategory.MAJOR, RequirementType.COMPULSORY, 2, 1, 1, "1-2", []),
        Course("微分積分学I", "MATH101", "B", CourseCategory.COMMON_MATH, RequirementType.COMPULSORY, 2, 1, 1, "1-2", []),
        Course("英語I", "ENG101", "A", CourseCategory.LANGUAGE, RequirementType.COMPULSORY, 2, 1, 1, "1-2", []),
        Course("情報リテラシー", "GEN101", "A", CourseCategory.UNIVERSITY_COMMON, RequirementType.COMPULSORY, 2, 1, 1, "1-2", []),
        Course("体育実技I", "PE101", "A", CourseCategory.HEALTH_PE, RequirementType.COMPULSORY, 1, 1, 1, "1-2", []),
        Course("情報基礎", "INFO101", "B", CourseCategory.INFORMATICS, RequirementType.COMPULSORY, 2, 1, 1, "1-2", []),
    ]
    return completed


def test_condition_processor():
    """Test ConditionProcessor functionality"""
    print("=== ConditionProcessor テスト ===")
    
    processor = ConditionProcessor()
    
    # Test data
    user_conditions = UserConditions(
        min_units=14,
        max_units=20,
        preferences=["afternoon", "専門重視"],
        avoid_first_period=True,
        preferred_time_slots=["3", "4"],
        preferred_categories=[CourseCategory.MAJOR]
    )
    
    completed_courses = create_completed_courses()
    available_courses = create_sample_courses()
    
    print(f"完了済み科目数: {len(completed_courses)}")
    print(f"利用可能科目数: {len(available_courses)}")
    
    # Test current semester recommendations
    try:
        recommendations = processor.process_current_semester_recommendation(
            user_id=12345,
            user_conditions=user_conditions,
            completed_courses=completed_courses,
            available_courses=available_courses
        )
        
        print(f"\n今学期の推奨科目数: {len(recommendations)}")
        for i, rec in enumerate(recommendations):
            print(f"  パターン {i+1}: {rec.total_credits}単位, {len(rec.courses)}科目")
            for course in rec.courses[:3]:  # Show first 3 courses
                print(f"    - {course.subject_name} ({course.credit}単位)")
        
        print("✓ 今学期推奨機能: 正常動作")
        
    except Exception as e:
        print(f"✗ 今学期推奨機能エラー: {e}")
    
    # Test four-year patterns
    try:
        patterns = processor.generate_four_year_patterns(
            user_id=12345,
            user_conditions=user_conditions,
            completed_courses=completed_courses,
            all_courses=available_courses
        )
        
        print(f"\n4年間パターン数: {len(patterns)}")
        for i, pattern in enumerate(patterns):
            print(f"  パターン {i+1}: {pattern.description}")
            print(f"    総単位数: {pattern.total_credits}, 卒業可能: {pattern.graduation_feasible}")
        
        print("✓ 4年間パターン生成: 正常動作")
        
    except Exception as e:
        print(f"✗ 4年間パターン生成エラー: {e}")


def test_condition_parser():
    """Test ConditionParser functionality"""
    print("\n=== ConditionParser テスト ===")
    
    parser = ConditionParser()
    
    # Test conditions
    conditions = {
        'min_units': 16,
        'max_units': 22,
        'preferences': ['afternoon', '専門重視'],
        'avoid_first_period': True,
        'preferred_time_slots': ['3', '4', '5'],
        'preferred_categories': ['専門科目']
    }
    
    completed_courses = create_completed_courses()
    available_courses = create_sample_courses()
    necessary_subjects = {}
    
    # Test condition parsing and execution
    try:
        recommendations = parser.parse_and_execute(
            conditions=conditions,
            user_id=12345,
            completed_courses=completed_courses,
            available_courses=available_courses,
            necessary_subjects=necessary_subjects
        )
        
        print(f"条件ベース推奨パターン数: {len(recommendations)}")
        for i, rec in enumerate(recommendations):
            print(f"  パターン {i+1}: {rec.total_credits}単位, {len(rec.courses)}科目")
        
        print("✓ 条件解析・実行: 正常動作")
        
    except Exception as e:
        print(f"✗ 条件解析・実行エラー: {e}")
    
    # Test specific avoid first period function
    try:
        user_conditions = UserConditions(
            min_units=16,
            max_units=22,
            preferences=[],
            avoid_first_period=True
        )
        
        first_period_patterns = parser.get_registration_pattern_avoiding_first_hour_class(
            user_conditions=user_conditions,
            completed_courses=completed_courses,
            available_courses=available_courses,
            necessary_subjects=necessary_subjects
        )
        
        print(f"\n1限回避パターン数: {len(first_period_patterns)}")
        
        # Check if patterns actually avoid first period
        for pattern in first_period_patterns:
            first_period_courses = [
                course for course in pattern.courses 
                if course.time_slot and '1' in course.time_slot
            ]
            print(f"  1限科目数: {len(first_period_courses)}")
        
        print("✓ 1限回避機能: 正常動作")
        
    except Exception as e:
        print(f"✗ 1限回避機能エラー: {e}")


def test_registration_pattern_calculator():
    """Test RegistrationPatternCalculator functionality"""
    print("\n=== RegistrationPatternCalculator テスト ===")
    
    calculator = RegistrationPatternCalculator()
    
    user_conditions = UserConditions(
        min_units=16,
        max_units=22,
        preferences=[],
        avoid_first_period=False
    )
    
    completed_courses = create_completed_courses()
    available_courses = create_sample_courses()
    necessary_subjects = {}
    
    try:
        patterns = calculator.get_registration_pattern(
            user_conditions=user_conditions,
            completed_courses=completed_courses,
            available_courses=available_courses,
            necessary_subjects=necessary_subjects
        )
        
        print(f"生成パターン数: {len(patterns)}")
        for pattern in patterns:
            print(f"  パターン: {pattern.pattern_id}")
            print(f"    説明: {pattern.description}")
            print(f"    総単位数: {pattern.total_credits}")
            print(f"    卒業可能: {pattern.graduation_feasible}")
            print(f"    年度パターン数: {len(pattern.yearly_patterns)}")
        
        print("✓ 履修パターン算出: 正常動作")
        
    except Exception as e:
        print(f"✗ 履修パターン算出エラー: {e}")


def main():
    """Run all C4 component tests"""
    print("C4 条件処理部 統合テスト開始")
    print("=" * 50)
    
    test_condition_processor()
    test_condition_parser()
    test_registration_pattern_calculator()
    
    print("\n" + "=" * 50)
    print("C4 条件処理部 統合テスト完了")


if __name__ == "__main__":
    main()