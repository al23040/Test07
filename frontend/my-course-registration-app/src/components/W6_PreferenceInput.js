// src/components/W6_PreferenceInput.js

import React, { useState } from 'react';
import './W6_PreferenceInput.css';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';         // 認証Context
import { useConditions } from '../context/ConditionsContext'; // 希望条件Context

function W6_PreferenceInput() {
  const navigate = useNavigate();
  
  // --- Contextから必要なデータを取得 ---
  const { userId } = useAuth();
  const { conditions, setConditions } = useConditions(); // グローバルな希望条件

  // --- この画面だけで使う、入力フォーム用の状態 ---
  const [minUnits, setMinUnits] = useState(conditions.min_units || '');
  const [maxUnits, setMaxUnits] = useState(conditions.max_units || '');
  const [preferredCategories, setPreferredCategories] = useState(conditions.preferred_categories || []);
  const [avoidFirstPeriod, setAvoidFirstPeriod] = useState(conditions.avoid_first_period || false);
  // ... 他の入力項目のためのuseState ...

  const handleNext = async () => {
    if (!userId) {
      alert("ログインしていません。");
      navigate('/login');
      return;
    }
    
    // --- ユーザーが入力した内容をオブジェクトにまとめる ---
    const newConditions = {
      min_units: parseInt(minUnits, 10),
      max_units: parseInt(maxUnits, 10),
      preferred_categories: preferredCategories,
      avoid_first_period: avoidFirstPeriod,
      // ... 他の条件もここに追加 ...
    };

    try {
      // 1. グローバルな希望条件 (Context) を更新する
      setConditions(newConditions);

      // 2. APIに送信する
      await axios.post(`/api/c7/user_conditions/${userId}`, {
        user_id: userId,
        ...newConditions //まとめた条件を送信
      });
      
      alert("希望条件を保存しました。");
      navigate('/current-semester-recommendation'); // 次の画面へ

    } catch (err) {
      console.error("条件の保存に失敗しました:", err);
      alert("エラーが発生しました。");
    }
  };

  const handleCheckboxChange = (value, listSetter, currentList) => {
    // ... (この部分は変更なし) ...
  };
  
  if (isLoading) {
    return <div className="container">科目データを読み込み中...</div>;
  }
  
  return (
    <div className="container">
      <h1>希望条件の入力</h1>
      {/* ... (入力フォームのJSX部分は、allCoursesを使って表示) ... */}
      <div className="input-group vertical">
        <label>希望授業名</label>
        <div className="checkbox-list details-box">
          {allCourses.length > 0 ? (
            allCourses.map((course) => (
              <label key={course.id}>
                {/* ... checkbox ... */}
              </label>
            ))
          ) : (
            <p>履修可能な科目がありません。</p>
          )}
        </div>
      </div>
      {/* ... 他の入力フォーム ... */}
      <button id="next-button" onClick={handleNext}>次へ</button>
    </div>
  );
}

export default W6_PreferenceInput;