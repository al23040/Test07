from flask import Flask, request, jsonify
from flask_cors import CORS
from c2.Authorization import Authorization
from c5.account_manager import AccountManager
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # CORSを有効にしてフロントエンドからのアクセスを許可

# AccountManagerとAuthorizationの初期化
account_manager = AccountManager()
auth = Authorization(account_manager)


@app.route('/api/register', methods=['POST'])
def register():
    """新規登録API"""
    try:
        # JSONデータを取得
        data = request.get_json(force=True)
        print(f"リクエスト送信:{data}")

        if not data or 'user_id' not in data or 'user_pw' not in data:
            return jsonify({
                'success': False,
                'message': 'リクエストデータが無効です'
            }), 400

        user_id = data.get('user_id')
        user_pw = data.get('user_pw')

        # 入力値の検証
        if not user_id or not user_pw:
            return jsonify({
                'success': False,
                'message': '学籍番号とパスワードは必須です'
            }), 400

        # 型の検証
        if not isinstance(user_id, int):
            try:
                user_id = int(data.get("user_id"))
            except(ValueError, TypeError):
                return jsonify({
                    'success': False,
                    'message': '学籍番号は数値である必要があります'
                }), 400

        # バリデーション（フロントエンドと同じチェックをバックエンドでも実施）
        if not (10000 <= user_id <= 99999):  # 5桁チェック
            return jsonify({
                'success': False,
                'message': '学籍番号は5桁の数字である必要があります'
            }), 400

        if len(user_pw) < 8 or len(user_pw) > 64:
            return jsonify({
                'success': False,
                'message': 'パスワードは8文字以上64文字以下である必要があります'
            }), 400

        # 英数字チェック
        if not user_pw.isalnum():
            return jsonify({
                'success': False,
                'message': 'パスワードは半角英数字のみ使用可能です'
            }), 400

        # Authorizationクラスを使用して登録処理
        logger.info(f"登録処理開始: user_id={user_id}")
        result = auth.register_user(user_id, user_pw)

        if result:
            logger.info(f"登録成功: user_id={user_id}")
            return jsonify({
                'success': True,
                'message': '登録が完了しました'
            }), 201
        else:
            logger.warning(f"登録失敗: user_id={user_id}")
            return jsonify({
                'success': False,
                'message': '登録に失敗しました（既に存在する学籍番号の可能性があります）'
            }), 409

    except ValueError as e:
        logger.error(f"バリデーションエラー: {str(e)}")
        return jsonify({
            'success': False,
            'message': '入力データが無効です'
        }), 400
    except Exception as e:
        logger.error(f"予期しないエラー: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'システムエラーが発生しました'
        }), 500


@app.route('/api/login', methods=['POST'])
def login():
    """ログインAPI（将来的に使用）"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'リクエストデータが無効です'
            }), 400

        user_id = data.get('user_id')
        user_pw = data.get('user_pw')

        if not user_id or not user_pw:
            return jsonify({
                'success': False,
                'message': '学籍番号とパスワードは必須です'
            }), 400

        # Authorizationクラスを使用して認証
        result = auth.check_auth(int(user_id), user_pw)

        if result:
            return jsonify({
                'success': True,
                'message': 'ログイン成功'
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': '学籍番号またはパスワードが間違っています'
            }), 401

    except Exception as e:
        logger.error(f"ログインエラー: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'システムエラーが発生しました'
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """ヘルスチェックAPI"""
    return jsonify({
        'status': 'OK',
        'message': 'サーバーは正常に動作しています'
    }), 200


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'APIエンドポイントが見つかりません'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'message': '許可されていないHTTPメソッドです'
    }), 405


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
