from models import Registration
from sqlalchemy.orm import Session

class SaveCourseData:

    def submit_course_data(self, courses: list, user_id: int):
        for course in courses:
            code = course.get("code")
            if not code:
                continue

            registration = Registration(
                user_id=user_id,
                code=code
            )
            self.session.add(registration)

        self.session.commit()

