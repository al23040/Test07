// src/components/W1_Login.js
import React, { useState } from 'react';
import './W1_Login.css';
import { useNavigate } from 'react-router-dom';
import { Link } from 'react-router-dom'
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

function Login() {
  const [userId, setUserId] = useState('');
  const [stuPass, setStuPass] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleLogin = async () => {
    setError('');

    if (!/^\d{5}$/.test(userId)) {
      setError('学籍番号は5桁の半角数字です');
      return;
    }

    if (!/^[0-9A-Za-z]{8,64}$/.test(stuPass)) {
      setError('パスワードは8文字以上64文字以下の半角英数字です');
      return;
    }

    try {
      const response = await axios.post('api/login', {
        user_id: parseInt(userId),
        user_pw: stuPass,
      });

      if (response.data.success) {
        login(userId); // コンテキスト保存
        localStorage.setItem('user_id', userId); // 必要なら保存
        navigate('/grade-upload'); // 次のページへ
      } else {
        setError(response.data.message);
      }
    } catch (err) {
      setError('ログインに失敗しました');
    }
  };

  return (
    <div className="screen">
      <div className="form-container">
        <h2>ログイン画面</h2>
        <label>学籍番号</label>
        <input type="text" value={userId} onChange={(e) => setUserId(e.target.value)} />
        <label>パスワード</label>
        <input type="password" value={stuPass} onChange={(e) => setStuPass(e.target.value)} />
        <button onClick={handleLogin}>ログイン</button>
        <Link to="/register">新規登録へ</Link>
        <p className="error">{error}</p>
      </div>
    </div>
  );
}

export default Login;
