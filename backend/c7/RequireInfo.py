from c4.condition_processor import ConditionProcessor, UserConditions
from typing import Optional, Dict, List

class RequireInfo:

    def __init__(self, condition_processor: ConditionProcessor, all_user_conditions: Dict[int, UserConditions]):
        self.condition_processor = condition_processor
        self.all_user_conditions = all_user_conditions

    def get_user_conditions(self, user_id: int) -> Optional[UserConditions]:

        if not isinstance(user_id, int) or not(20000 <= user_id <= 99999):
            print(f"警告: 不正な学籍番号が入力されました。5桁の整数を入力してください：{user_id}")
            return None
        retrieved_conditions = self.all_user_conditions.get(user_id)

        if retrieved_conditions is None:
            print(f"学籍番号AL{user_id}の希望条件は見つかりませんでした。")
            return None
        else:
            return retrieved_conditions
