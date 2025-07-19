// W6_PreferenceInput.js
import React, { useState, useEffect } from 'react';
import './W6_PreferenceInput.css';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useConditions } from '../context/ConditionsContext';

function W6_PreferenceInput() {
  const navigate = useNavigate();
  const userId = parseInt(localStorage.getItem('user_id'), 10) || null;
  const { setConditions } = useConditions();

  const [minUnits, setMinUnits] = useState('');
  const [maxUnits, setMaxUnits] = useState('');
  const [preferredCategories, setPreferredCategories] = useState([]);
  const [showPriority, setShowPriority] = useState(false);
  const [avoidFirstPeriod, setAvoidFirstPeriod] = useState(false);
  const [preferredDays, setPreferredDays] = useState([]);
  const [avoidedDays, setAvoidedDays] = useState([]);
  const [preferredTimeSlots, setPreferredTimeSlots] = useState([]);
  const [preferences, setPreferences] = useState([]);
  const [availableCourses, setAvailableCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!userId) {
      setLoading(false);
      return;
    }

    const storedAvailable = localStorage.getItem('availableCourses');
    if (storedAvailable) {
      try {
        setAvailableCourses(JSON.parse(storedAvailable));
      } catch {
        setAvailableCourses([]);
      } finally {
        setLoading(false);
      }
    } else {
      setLoading(false);
    }
  }, [userId]);

  const handleCheckboxChange = (value, listSetter, currentList) => {
    if (currentList.includes(value)) {
      listSetter(currentList.filter((item) => item !== value));
    } else {
      listSetter([...currentList, value]);
    }
  };

  const handleNext = async () => {
    if (!userId) {
      alert("ユーザーIDが見つかりません。ログインしてください。");
      navigate('/login');
      return;
    }

    if (!minUnits || !maxUnits) {
      alert("単位数を入力してください。");
      return;
    }
    if (parseInt(minUnits, 10) > parseInt(maxUnits, 10)) {
      alert("最小単位数は最大単位数より小さくしてください。");
      return;
    }

  const dataToSend = {
      user_id: userId,
      min_units: parseInt(minUnits, 10),
      max_units: parseInt(maxUnits, 10),
      preferences: preferences,
      avoid_first_period: avoidFirstPeriod,
      preferred_time_slots: preferredTimeSlots.map(time => time.replace('限', '')),
      preferred_categories: preferredCategories,
      preferred_days: preferredDays,
      avoided_days: avoidedDays
    };

    setConditions({
      min_units: parseInt(minUnits, 10),
      max_units: parseInt(maxUnits, 10),
      preferences: preferences,
      avoid_first_period: avoidFirstPeriod,
      preferred_time_slots: preferredTimeSlots.map(time => time.replace('限', '')),
      preferred_categories: preferredCategories,
      preferred_days: preferredDays,
      avoided_days: avoidedDays
    });

    try {
      const resCond = await axios.post(`/api/c7/user_conditions/${userId}`, dataToSend);

      if (resCond.status === 200 && resCond.data.status === 'ok') {
        if (resCond.data.four_year_patterns) {
          localStorage.setItem('four_year_patterns', JSON.stringify(resCond.data.four_year_patterns));
        }

        navigate('/current-semester-recommendation');
      } else {
        alert(`条件の送信に失敗しました: ${resCond.data.error || '不明なエラー'}`);
      }
    } catch (err) {
      console.error("送信中にエラー:", err);
      alert("送信中にエラーが発生しました。");
    }
  };


  if (loading) {
    return <div className="container">データを読み込み中...</div>;
  }

  if (error) {
    return <div className="container">エラー: {error}</div>;
  }

  return (
    <div className="container">
      <h1>希望条件の入力</h1>

            <div className="input-group">
        <label>単位数</label>
        最少
        <input
          type="number"
          className="half-width"
          value={minUnits}
          onChange={e => setMinUnits(e.target.value)}
          min="0"
        /> 単位 〜 最大
        <input
          type="number"
          className="half-width"
          value={maxUnits}
          onChange={e => setMaxUnits(e.target.value)}
          min="0"
        /> 単位
      </div>

      <div className="input-group">
        <label htmlFor="priority-toggle">
          <input
            type="checkbox"
            id="priority-toggle"
            checked={showPriority}
            onChange={() => setShowPriority(!showPriority)}
          />
          優先科目を指定する
        </label>

        {showPriority && (
          <div className="details-box">
            {["専門科目", "共通数理科目", "人文社会系教養科目", "言語科目", "共通健康科目", "全学共通科目","共通工学系教養科目"].map((cat) => (
              <label key={cat}>
                <input
                  type="checkbox"
                  value={cat}
                  checked={preferredCategories.includes(cat)}
                  onChange={() => handleCheckboxChange(cat, setPreferredCategories, preferredCategories)}
                />
                {cat}
              </label>
            ))}
          </div>
        )}
      </div>

      <div className="input-group vertical">
        <label>希望授業名</label>
        <div className="checkbox-list details-box" style={{ maxHeight: '200px', overflowY: 'auto' }}>
          {availableCourses.length > 0 ? (
            availableCourses.map((course) => (
              <label key={course.code || course.subject_name} className="checkbox-label">
                <input
                  type="checkbox"
                  checked={preferences.includes(course.subject_name)}
                  onChange={() =>
                    handleCheckboxChange(course.subject_name, setPreferences, preferences)
                  }
                />
                {course.subject_name} ({course.credit}単位)
              </label>
            ))
          ) : (
            <p>履修可能科目データがありません。</p>
          )}
        </div>
      </div>

      <div className="input-group vertical">
        <label>希望時間帯</label>
        <div className="checkbox-list details-box">
          {["1限", "2限", "3限", "4限", "5限"].map((time) => (
            <label key={time}>
              <input
                type="checkbox"
                value={time}
                checked={preferredTimeSlots.includes(time)}
                onChange={() => handleCheckboxChange(time, setPreferredTimeSlots, preferredTimeSlots)}
              />
              {time}
            </label>
          ))}
        </div>
      </div>

      <div className="input-group">
        <label>
          <input
            type="checkbox"
            checked={avoidFirstPeriod}
            onChange={() => setAvoidFirstPeriod(!avoidFirstPeriod)}
          />
          1限を避けたい
        </label>
      </div>

      <div className="input-group day-preference-group">
        <label>曜日の希望</label>
        <div>
          <span>避けたい曜日:</span>
          <div className="day-selection-group">
            {["月", "火", "水", "木", "金", "土"].map((day) => (
              <label key={day}>
                <input
                  type="checkbox"
                  value={day}
                  checked={avoidedDays.includes(day)}
                  onChange={() => handleCheckboxChange(day, setAvoidedDays, avoidedDays)}
                />
                {day}
              </label>
            ))}
          </div>
        </div>
        <div>
          <span>出たい曜日:</span>
          <div className="day-selection-group">
            {["月", "火", "水", "木", "金", "土"].map((day) => (
              <label key={day}>
                <input
                  type="checkbox"
                  value={day}
                  checked={preferredDays.includes(day)}
                  onChange={() => handleCheckboxChange(day, setPreferredDays, preferredDays)}
                />
                {day}
              </label>
            ))}
          </div>
        </div>
      </div>

      <button id="next-button" onClick={handleNext}>次へ</button>
    </div>
  );
}

export default W6_PreferenceInput;
