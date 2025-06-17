from backend.UserInfo import UserInfo

class CoursesInfo:

    def __init__(self, courses: dict):
        self.courses = courses

    def send_courses(self, user_id: int) -> list[str]:
        if user_id in self.courses:
            return self.courses[user_id]
        else:
            print(f"学籍番号{user_id}の学生は見つかりませんでした。")
            return []