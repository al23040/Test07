import React, { useState } from 'react';
import './W2_SignUp.css';
import { useNavigate } from 'react-router-dom';

function SignUp() {
  const [userId, setUserId] = useState('');
  const [stuPass, setStuPass] = useState('');
  const [confirm, setConfirm] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleRegister = () => {
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

    navigate('/login');
  };

  return (
    <div className="screen">
      <div className="form-container">
        <h2>新規登録</h2>

        <div>
          <label htmlFor="reg-id">学籍番号</label>
          <input
            id="reg-id"
            type="text"
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            placeholder="例: 12345"
          />
          <small>※5桁の半角数字（MSゴシック）</small>
        </div>

        <div>
          <label htmlFor="reg-pass">パスワード</label>
          <input
            id="reg-pass"
            type="password"
            value={stuPass}
            onChange={(e) => setStuPass(e.target.value)}
          />
          <small>※半角英字+数字（MSゴシック）8文字以上64文字以下</small>
        </div>

        <div>
          <label htmlFor="reg-confirm">確認用</label>
          <input
            id="reg-confirm"
            type="password"
            value={confirm}
            onChange={(e) => setConfirm(e.target.value)}
          />
          <small>※8文字以上の半角の英数字を複合した物</small>
        </div>

        <button onClick={handleRegister}>登録</button>
        <p className="error">{error}</p>
      </div>
    </div>
  );
}

export default SignUp;

