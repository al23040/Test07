from c5.account_manager import AccountManager
class Authorization:

    def __init__(self, account_manager: AccountManager):
        self.account_manager = account_manager

    def check_auth(self, user_id: int, user_pw: str) -> bool:
        flag = self.account_manager.authenticate_user(user_id, user_pw)
        if flag:
            return True
        else:
            return False

    def register_user(self, user_id: int, user_pw: str) -> bool:
        flag = self.account_manager.create_user_account(user_id, user_pw)
        if flag:
            return True
        else:
            return False