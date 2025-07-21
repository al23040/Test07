#/backend/c7/RequireInfo
from c4.condition_processor import ConditionProcessor, UserConditions
from typing import Optional, Dict, List
from c4.condition_processor import CourseCategory, DayOfWeek

class RequireInfo:

    def __init__(self, condition_processor: ConditionProcessor, all_user_conditions: Dict[int, UserConditions]):
        self.condition_processor = condition_processor
        self.all_user_conditions = all_user_conditions

    def get_user_conditions(self, user_id: int) -> Optional[UserConditions]:
        if not isinstance(user_id, int) or not (20000 <= user_id <= 99999):
            print(f"警告: 不正な学籍番号が入力されました。5桁の整数を入力してください：{user_id}")
            return None

        retrieved_conditions = self.all_user_conditions.get(user_id)

        if retrieved_conditions is None:
            print(f"学籍番号AL{user_id}の希望条件は見つかりませんでした。")
            return None
        else:
            return retrieved_conditions

    def save_user_conditions(self, user_id: int, conditions: UserConditions) -> bool:
        """ユーザー条件を保存"""
        if isinstance(user_id, int) and 20000 <= user_id <= 99999:
            self.all_user_conditions[user_id] = conditions
            return True
        else:
            print(f"保存失敗：不正な学籍番号 {user_id}")
            return False

    def create_user_conditions_from_form(self, form_data: Dict) -> UserConditions:
        """フォームデータから UserConditions オブジェクトを作成"""
        user_id = form_data.get('user_id')
        
        # 基本設定
        min_units = form_data.get('min_units', 0)
        max_units = form_data.get('max_units', 20)
        avoid_first_period = form_data.get('avoid_first_period', False)

        # 希望授業
        preferences = []
        if 'priority' in form_data and form_data['priority']:
            preferences.append(form_data['priority'])
        if 'plus' in form_data and form_data['plus']:
            preferences.extend([p.strip() for p in form_data['plus'].split(',') if p.strip()])

        # 時間帯
        preferred_time_slots = form_data.get('preferred_time_slots', [])
        if isinstance(preferred_time_slots, str):
            preferred_time_slots = [slot.strip() for slot in preferred_time_slots.split(',') if slot.strip()]

        # カテゴリ
        preferred_categories = []
        category_names = form_data.get('preferred_categories', [])
        if isinstance(category_names, str):
            category_names = [cat.strip() for cat in category_names.split(',') if cat.strip()]
        for cat_name in category_names:
            for category in CourseCategory:
                if category.value == cat_name:
                    preferred_categories.append(category)
                    break

        # 曜日希望と回避
        preferred_days = []
        avoided_days = []

        preferred_day_names = form_data.get('preferred_days', [])
        if isinstance(preferred_day_names, str):
            preferred_day_names = [day.strip() for day in preferred_day_names.split(',') if day.strip()]
        for day_name in preferred_day_names:
            for day in DayOfWeek:
                if day.value == day_name:
                    preferred_days.append(day)
                    break

        avoided_day_names = form_data.get('avoided_days', [])
        if isinstance(avoided_day_names, str):
            avoided_day_names = [day.strip() for day in avoided_day_names.split(',') if day.strip()]
        for day_name in avoided_day_names:
            for day in DayOfWeek:
                if day.value == day_name:
                    avoided_days.append(day)
                    break

        return UserConditions(
            user_id=user_id,
            min_units=min_units,
            max_units=max_units,
            preferences=preferences,
            avoid_first_period=avoid_first_period,
            preferred_time_slots=preferred_time_slots,
            preferred_categories=preferred_categories,
            preferred_days=preferred_days,
            avoided_days=avoided_days
        )
