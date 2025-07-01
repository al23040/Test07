import unittest
from unittest.mock import Mock, MagicMock
import sys
import os
from typing import Dict, List, Optional

# プロジェクトのルートディレクトリをsys.pathに追加
# テストファイル (c7/test/test_c7.py) から見て、
# 2つ上のディレクトリ (c7/test -> c7 -> backend) がモジュールのルートと仮定
current_test_dir = os.path.dirname(os.path.abspath(__file__))
module_root_dir = os.path.abspath(os.path.join(current_test_dir, '..', '..'))

if module_root_dir not in sys.path:
    sys.path.insert(0, module_root_dir)

# テスト対象のクラスと、それが依存するクラスをインポート
# RequireInfoクラスが backend/c7/RequireInfo.py にあると仮定
from c7.RequireInfo import RequireInfo

# c4/condition_processor.py から ConditionProcessor と UserConditions をインポート
from c4.condition_processor import ConditionProcessor, UserConditions, DayOfWeek, CourseCategory


class TestRequireInfo(unittest.TestCase):
    """
    RequireInfoクラスの単体テスト
    """

    def setUp(self):
        """
        各テストメソッド実行前の初期化処理
        """
        # ConditionProcessorのモックを作成 (RequireInfoが依存しているため)
        self.mock_condition_processor = Mock(spec=ConditionProcessor)

        # テスト用のダミーUserConditionsオブジェクトを作成
        # UserConditionsはdataclassなので、実際のオブジェクトとして作成できます。
        self.dummy_user_cond_23089 = UserConditions(
            min_units=10, max_units=20, preferences=["AI"],
            avoid_first_period=True, preferred_days=[DayOfWeek.MONDAY]
        )
        self.dummy_user_cond_10002 = UserConditions(
            min_units=15, max_units=25, preferences=["Robotics"],
            avoided_days=[DayOfWeek.TUESDAY]
        )

        # 全ユーザーの条件データをシミュレートする辞書
        self.all_user_conditions_mock_data = {
            23089: self.dummy_user_cond_23089,
            10002: self.dummy_user_cond_10002,
        }

        # RequireInfoのインスタンスを作成し、モックとダミーデータを注入
        self.require_info = RequireInfo(
            condition_processor=self.mock_condition_processor,
            all_user_conditions=self.all_user_conditions_mock_data
        )

    def test_get_user_conditions_success(self):
        """
        存在するユーザーIDで希望条件が正常に取得できる場合のテスト
        """
        user_id = 23089
        # get_user_conditionsを呼び出すと、内部でall_user_conditionsから取得される
        result = self.require_info.get_user_conditions(user_id)

        # 結果が期待通りのUserConditionsオブジェクトであることをアサート
        self.assertIsNotNone(result)
        self.assertEqual(result, self.dummy_user_cond_23089)

    def test_get_user_conditions_not_found(self):
        """
        希望条件が見つからないユーザーIDの場合のテスト
        """
        user_id = 99999  # 辞書に存在しないID

        result = self.require_info.get_user_conditions(user_id)

        # 結果がNoneであることをアサート
        self.assertIsNone(result)

    def test_get_user_conditions_invalid_id_negative(self):
        """
        不正なユーザーID（負の値）の場合のテスト
        """
        user_id = -100

        result = self.require_info.get_user_conditions(user_id)

        # 結果がNoneであることをアサート
        self.assertIsNone(result)

    def test_get_user_conditions_invalid_id_short_digits(self):
        """
        不正なユーザーID（5桁未満）の場合のテスト
        """
        user_id = 1234

        result = self.require_info.get_user_conditions(user_id)

        self.assertIsNone(result)

    def test_get_user_conditions_invalid_id_long_digits(self):
        """
        不正なユーザーID（5桁より多い）の場合のテスト
        """
        user_id = 123456

        result = self.require_info.get_user_conditions(user_id)

        self.assertIsNone(result)

    def test_get_user_conditions_invalid_id_type(self):
        """
        不正なユーザーID（int型以外）の場合のテスト
        """
        user_id = "abcde"  # 文字列

        result = self.require_info.get_user_conditions(user_id)

        self.assertIsNone(result)

    def test_get_user_conditions_edge_case_min_id(self):
        """
        学籍番号の最小値エッジケース (10000) のテスト
        """
        user_id = 20000
        # 辞書にIDを追加してテスト
        self.all_user_conditions_mock_data[user_id] = self.dummy_user_cond_23089
        result = self.require_info.get_user_conditions(user_id)
        self.assertIsNotNone(result)
        self.assertEqual(result, self.dummy_user_cond_23089)

    def test_get_user_conditions_edge_case_max_id(self):
        """
        学籍番号の最大値エッジケース (99999) のテスト
        """
        user_id = 99999
        # 辞書にIDを追加してテスト
        self.all_user_conditions_mock_data[user_id] = self.dummy_user_cond_10002
        result = self.require_info.get_user_conditions(user_id)
        self.assertIsNotNone(result)
        self.assertEqual(result, self.dummy_user_cond_10002)


if __name__ == '__main__':
    unittest.main(verbosity=2)  # verbosity=2 でより詳細なテスト結果を表示