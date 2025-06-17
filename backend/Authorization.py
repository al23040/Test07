from backend.UserInfo import UserInfo

class Authorization:

    def __init__(self, users: list[UserInfo]):
        self.users = users

    def check_auth(self, user_id: int, user_pw: str) -> bool:
        for user in self.users:
            if user.user_id == user_id and user.user_pw == user_pw:
                return True
        return False

    def register_user(self, user_id: int, user_pw: str) -> bool:
        for user in self.users:
            if user.user_id == user_id:
                print(f"ユーザーID:｛user_id｝は既に存在します。")
                return False
        new_user = UserInfo(user_id, user_pw)
        self.users.append(new_user)
        print(f"新しくユーザーを登録しました: ID:{user_id}")
        return True