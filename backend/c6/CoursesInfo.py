from c5.models import TakenCourse
from c5.account_manager import AccountManager
from typing import List

class CoursesInfo:

    def __init__(self, account_manager: AccountManager):
        self.account_manager = account_manager

    def get_user_courses(self, user_id: int) -> List[TakenCourse]:
        try:
            passed_courses: List[TakenCourse] = self.account_manager.get_user_passed_courses(user_id)

            if not passed_courses:
                print(f"学籍番号AL{user_id} の合格科目は見つかりませんでした。")
                return []

            course_data_list = []
            for course in passed_courses:
                course_data = {
                    'subject_id': course.subject_id,
                    'subject_name': course.subject_name,
                    'evaluation': course.evaluation,
                    'credits': course.credits,
                    'passed': course.passed,
                    'semester': course.semester,
                    'year': course.year,
                    'category': course.category
                }
                course_data_list.append(course_data)
            print(f"学籍番号AL{user_id} の合格科目 {len(course_data_list)} 件を取得しました。")
            return course_data_list

        except Exception as e:
            print(f"合格科目の取得中にエラーが発生しました: {e}")
            return []