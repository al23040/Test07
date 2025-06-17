from backend.UserInfo import UserInfo

class RequireInfo:

    def __init__(self, conditions: dict = None):
        self.conditions = conditions

    def send_req(self, user_id: int, conditions: dict) -> dict:
        if user_id in conditions:
            return conditions[user_id]
        else:
            print(f"ユーザーID{user_id}の希望条件は見つかりませんでした。")
            return {}
