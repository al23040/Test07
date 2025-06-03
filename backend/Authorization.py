from backend.UserInfo import UserInfo

class Authorization:

    def __init__(self, users: list[UserInfo]):
        self.users = users

    def check_auth(self, user_id: int) -> bool:
        for user in self.users:
            if user.user_id == user_id:
                return True
            else:
                return False