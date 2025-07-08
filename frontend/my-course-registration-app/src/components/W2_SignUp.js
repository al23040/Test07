// src/components/W2_SignUp.js
import React, { useState } from 'react';
import './W2_SignUp.css';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function SignUp() {
  const [userId, setUserId] = useState('');
  const [stuPass, setStuPass] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = async () => {
    setError('');

    if (!/^\d{5}$/.test(userId)) {
      setError('学籍番号は5桁の半角数字です');
      return;
    }

    if (!/^[0-9A-Za-z]{8,64}$/.test(stuPass)) {
      setError('パスワードは8文字以上64文字以下の半角英数字です');
      return;
    }

    if (stuPass !== confirm) {
      setError('パスワードが一致しません');
      return;
    }

    try {
      const response = await axios.post('http://localhost:8000/api/register', {
        user_id: parseInt(userId),
        user_pw: stuPass,
      });

      if (response.data.success) {
        navigate('/login');
      } else {
        setError(response.data.message);
      }
    } catch (err) {
      setError('登録に失敗しました');
    }
  };

  return (
    <div className="screen">
      <div className="form-container">
        <h2>新規登録</h2>
        <label>学籍番号</label>
        <input type="text" value={userId} onChange={(e) => setUserId(e.target.value)} />
        <label>パスワード</label>
        <input type="password" value={stuPass} onChange={(e) => setStuPass(e.target.value)} />
        <label>確認用</label>
        <input type="password" value={confirm} onChange={(e) => setConfirm(e.target.value)} />
        <button onClick={handleRegister}>登録</button>
        <p className="error">{error}</p>
      </div>
    </div>
  );
}

export default SignUp;
