from backend.TakenCourse import TakenCourse

class UserInfo:
    def __init__(self, user_id: int, taken_course: TakenCourse):
        self.user_id = user_id
        self.taken_course = taken_course
