import React, { useState } from 'react';
import './W1_Login.css';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [userId, setUserId] = useState('');
  const [stuPass, setStuPass] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleLogin = () => {
    if (!/^\d{5}$/.test(userId)) {
      setError('学籍番号は5桁の半角数字です');
      return;
    }

    if (!/^[0-9A-Za-z]{8,64}$/.test(stuPass)) {
      setError('パスワードは8文字以上64文字以下の半角英数字です');
      return;
    }

    navigate('/grade-upload');
  };

  return (
    <div className="screen">
      <div className="form-container">
        <h2>ログイン画面</h2>

        <div>
          <label htmlFor="user-id">学籍番号</label>
          <input
            id="user-id"
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="12345"
          />
        </div>

        <div>
          <label htmlFor="stu-pass">パスワード</label>
          <input
            id="stu-pass"
            type="password"
            value={stuPass}
            onChange={(e) => setStuPass(e.target.value)}
          />
        </div>

        <button onClick={handleLogin}>ログイン</button>
        <a href="/register">新規登録へ</a>
        <p className="error">{error}</p>
      </div>
    </div>
  );
}

export default Login;
