import unittest
from unittest.mock import Mock, MagicMock
import sys
import os
from typing import List, Dict, Any

# プロジェクトのルートディレクトリをsys.pathに追加
current_test_dir = os.path.dirname(os.path.abspath(__file__))
module_root_dir = os.path.abspath(os.path.join(current_test_dir, '..', '..'))

if module_root_dir not in sys.path:
    sys.path.insert(0, module_root_dir)

from c6.CoursesInfo import CoursesInfo # ファイル名に合わせて修正

# AccountManagerクラスとTakenCourseモデルは backend/c5/ からインポート
from c5.account_manager import AccountManager
from c5.models import TakenCourse


class TestCoursesInfo(unittest.TestCase):
    # ... (以降のコードは変更なしでOK) ...

    def setUp(self):
        self.mock_account_manager = Mock(spec=AccountManager)
        self.courses_info = CoursesInfo(account_manager=self.mock_account_manager)

        self.dummy_passed_course_1 = TakenCourse(
            subject_id="MATH101", subject_name="微積第一", evaluation="A",
            credits=2, passed=True, semester=1, year=2023, category="必修"
        )
        self.dummy_passed_course_2 = TakenCourse(
            subject_id="MATH201", subject_name="微積第二", evaluation="S",
            credits=3, passed=True, semester=2, year=2024, category="選択"
        )
        self.dummy_passed_course_data_1 = {
            'subject_id': "MATH101", 'subject_name': "微積第一", 'evaluation': "A",
            'credits': 2, 'passed': True, 'semester': 1, 'year': 2023, 'category': "必修"
        }
        self.dummy_passed_course_data_2 = {
            'subject_id': "MATH201", 'subject_name': "微積第二", 'evaluation': "S",
            'credits': 3, 'passed': True, 'semester': 2, 'year': 2024, 'category': "選択"
        }

    def test_get_user_courses_success(self):
        user_id = 23089
        self.mock_account_manager.get_user_passed_courses.return_value = [
            self.dummy_passed_course_1,
            self.dummy_passed_course_2
        ]

        result = self.courses_info.get_user_courses(user_id)

        expected_result = [self.dummy_passed_course_data_1, self.dummy_passed_course_data_2]
        self.assertEqual(result, expected_result)
        self.assertEqual(len(result), 2)
        self.mock_account_manager.get_user_passed_courses.assert_called_once_with(user_id)

    def test_get_user_courses_no_courses_found(self):
        user_id = 23089
        self.mock_account_manager.get_user_passed_courses.return_value = []

        result = self.courses_info.get_user_courses(user_id)

        self.assertEqual(result, [])
        self.mock_account_manager.get_user_passed_courses.assert_called_once_with(user_id)

    def test_get_user_courses_exception_handling(self):
        user_id = 23089
        self.mock_account_manager.get_user_passed_courses.side_effect = Exception("データベースエラー")

        result = self.courses_info.get_user_courses(user_id)

        self.assertEqual(result, [])
        self.mock_account_manager.get_user_passed_courses.assert_called_once_with(user_id)


if __name__ == '__main__':
    unittest.main(verbosity=2)