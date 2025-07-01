import unittest
import sys
import os
from unittest.mock import Mock
# --- パス調整を修正 ---
# 現在のファイル（test_authorization.py）のディレクトリパス
current_test_dir = os.path.dirname(os.path.abspath(__file__))
# backendディレクトリのパスを計算 (c2/test から 2つ上)
# C:\...\backend\c2\test -> C:\...\backend\c2 -> C:\...\backend
backend_root_path = os.path.abspath(os.path.join(current_test_dir, '..', '..'))

# backendディレクトリをsys.pathの先頭に追加
if backend_root_path not in sys.path:
    sys.path.insert(0, backend_root_path)
from c2.Authorization import Authorization


class TestAuthorization(unittest.TestCase):
    """
    Authorizationクラスの単体テスト
    """

    def setUp(self):
        """
        各テストケース実行前の初期化
        """
        # AccountManagerのモックを作成
        self.mock_account_manager = Mock()
        self.auth = Authorization(self.mock_account_manager)

    def test_check_auth_success(self):
        """
        認証成功のテスト
        """
        # AccountManagerのmockが認証成功を返すように設定
        self.mock_account_manager.authenticate_user.return_value = True

        result = self.auth.check_auth(12345, "password123")

        # 結果の検証
        self.assertTrue(result)
        self.mock_account_manager.authenticate_user.assert_called_once_with(12345, "password123")

    def test_check_auth_failure(self):
        """
        認証失敗のテスト
        """
        # AccountManagerのmockが認証失敗を返すように設定
        self.mock_account_manager.authenticate_user.return_value = False

        result = self.auth.check_auth(12345, "wrong_password")

        # 結果の検証
        self.assertFalse(result)
        self.mock_account_manager.authenticate_user.assert_called_once_with(12345, "wrong_password")

    def test_check_auth_multiple_calls(self):
        """
        複数回の認証テスト
        """
        self.mock_account_manager.authenticate_user.return_value = True

        # 複数回呼び出し
        result1 = self.auth.check_auth(111, "pass1")
        result2 = self.auth.check_auth(222, "pass2")

        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertEqual(self.mock_account_manager.authenticate_user.call_count, 2)

    def test_register_user_success(self):
        """
        ユーザー登録成功のテスト
        """
        # AccountManagerのmockが登録成功を返すように設定
        self.mock_account_manager.create_user_account.return_value = True

        result = self.auth.register_user(12345, "password123")

        # 結果の検証
        self.assertTrue(result)
        self.mock_account_manager.create_user_account.assert_called_once_with(12345, "password123")

    def test_register_user_failure(self):
        """
        ユーザー登録失敗のテスト（既存ユーザーなど）
        """
        # AccountManagerのmockが登録失敗を返すように設定
        self.mock_account_manager.create_user_account.return_value = False

        result = self.auth.register_user(12345, "password123")

        # 結果の検証
        self.assertFalse(result)
        self.mock_account_manager.create_user_account.assert_called_once_with(12345, "password123")

    def test_register_user_multiple_calls(self):
        """
        複数回のユーザー登録テスト
        """
        self.mock_account_manager.create_user_account.return_value = True

        # 複数回呼び出し
        result1 = self.auth.register_user(111, "pass1")
        result2 = self.auth.register_user(222, "pass2")

        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertEqual(self.mock_account_manager.create_user_account.call_count, 2)

    def test_auth_and_register_workflow(self):
        """
        認証と登録のワークフローテスト
        """
        user_id = 12345
        password = "test_password"

        # 1. 最初は認証失敗（ユーザーが存在しない）
        self.mock_account_manager.authenticate_user.return_value = False
        auth_result_before = self.auth.check_auth(user_id, password)
        self.assertFalse(auth_result_before)

        # 2. ユーザー登録成功
        self.mock_account_manager.create_user_account.return_value = True
        register_result = self.auth.register_user(user_id, password)
        self.assertTrue(register_result)

        # 3. 登録後は認証成功
        self.mock_account_manager.authenticate_user.return_value = True
        auth_result_after = self.auth.check_auth(user_id, password)
        self.assertTrue(auth_result_after)

    def test_different_user_ids(self):
        """
        異なるユーザーIDでのテスト
        """
        # 様々なユーザーIDで認証テスト
        test_cases = [
            (1, "pass1"),
            (99999, "pass2"),
            (12345, "pass3")
        ]

        self.mock_account_manager.authenticate_user.return_value = True

        for user_id, password in test_cases:
            with self.subTest(user_id=user_id):
                result = self.auth.check_auth(user_id, password)
                self.assertTrue(result)

    def test_different_passwords(self):
        """
        異なるパスワードでのテスト
        """
        user_id = 12345
        passwords = ["short", "very_long_password_123", "パスワード", "!@#$%^&*()"]

        self.mock_account_manager.authenticate_user.return_value = True

        for password in passwords:
            with self.subTest(password=password):
                result = self.auth.check_auth(user_id, password)
                self.assertTrue(result)

    def test_mock_not_called_on_failure(self):
        """
        適切にモックが呼ばれているかのテスト
        """
        # 認証テスト
        self.mock_account_manager.authenticate_user.return_value = False
        self.auth.check_auth(111, "pass")

        # 登録テスト
        self.mock_account_manager.create_user_account.return_value = False
        self.auth.register_user(222, "pass")

        # 呼び出し回数の確認
        self.assertEqual(self.mock_account_manager.authenticate_user.call_count, 1)
        self.assertEqual(self.mock_account_manager.create_user_account.call_count, 1)

    def test_return_value_consistency(self):
        """
        戻り値の一貫性テスト
        """
        # Trueの場合
        self.mock_account_manager.authenticate_user.return_value = True
        self.mock_account_manager.create_user_account.return_value = True

        self.assertTrue(self.auth.check_auth(1, "pass"))
        self.assertTrue(self.auth.register_user(1, "pass"))

        # Falseの場合
        self.mock_account_manager.authenticate_user.return_value = False
        self.mock_account_manager.create_user_account.return_value = False

        self.assertFalse(self.auth.check_auth(1, "pass"))
        self.assertFalse(self.auth.register_user(1, "pass"))


if __name__ == '__main__':
    # テストの実行
    unittest.main(verbosity=2)
