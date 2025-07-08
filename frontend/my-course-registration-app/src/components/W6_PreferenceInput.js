// W6_PreferenceInput.js
/*import React, { useState } from 'react';
import './W6_PreferenceInput.css';
import { useNavigate } from 'react-router-dom';

function W6_PreferenceInput() {
  const navigate = useNavigate();
  const [showPriority, setShowPriority] = useState(false);
  const [showPlus, setShowPlus] = useState(false);
  const [showMinus, setShowMinus] = useState(false);

  const handleNext = () => {
    alert("入力完了");
    navigate('/next-page');
  };

  return (
    <div className="container">
      <h1>希望条件の入力</h1>

      <div className="input-group">
        <label>単位数</label>
        最少 <input type="number" min="0" max="49" /> 単位 〜 最大
        <input type="number" min="0" max="49" /> 単位
      </div>

      <div className="input-group">
        <input
          type="checkbox"
          id="priority-toggle"
          checked={showPriority}
          onChange={() => setShowPriority(!showPriority)}
        />
        <label htmlFor="priority-toggle">優先科目を指定する</label>

        {showPriority && (
          <div className="details-box">
            <div className="priority-item">
              <label><input type="checkbox" value="専門" /> 専門</label><br />
              <label><input type="checkbox" value="数理" /> 数理</label><br />
              <label><input type="checkbox" value="英語" /> 英語</label><br />
              <label><input type="checkbox" value="人文" /> 人文</label><br />
              <label><input type="checkbox" value="体育" /> 体育</label><br />
              <label><input type="checkbox" value="工学部共通科目" /> 工学部共通科目</label>
            </div>
          </div>
        )}
      </div>

      <div className="input-group">
        <input
          type="checkbox"
          id="plus-toggle"
          checked={showPlus}
          onChange={() => setShowPlus(!showPlus)}
        />
        <label htmlFor="plus-toggle">その他プラス要件を指定する</label>

        {showPlus && (
          <div className="details-box">
            <div className="plus-item">
              <label>週何日以下:</label>
              <input type="number" min="1" max="7" placeholder="例: 3" />
            </div>
            <div className="plus-item">
              <label>最低取得率(%):</label>
              <input type="number" min="0" max="100" placeholder="例: 80" />
            </div>
            <div className="plus-item">
              <label>希望研究室名:</label>
              <input type="text" placeholder="例: 井尻研究室" />
            </div>
          </div>
        )}
      </div>

      <div className="input-group">
        <input
          type="checkbox"
          id="minus-toggle"
          checked={showMinus}
          onChange={() => setShowMinus(!showMinus)}
        />
        <label htmlFor="minus-toggle">その他マイナス要件を指定する</label>

        {showMinus && (
          <div className="details-box">
            <div className="minus-item">
              <label>避けたい曜日:</label>
              <select>
                <option value="">選択してください</option>
                <option value="月">月曜</option>
                <option value="火">火曜</option>
                <option value="水">水曜</option>
                <option value="木">木曜</option>
                <option value="金">金曜</option>
                <option value="土">土曜</option>
              </select>
            </div>
            <div className="minus-item">
              <label>最大空きコマ数:</label>
              <input type="number" min="0" max="3" placeholder="例: 2" />
            </div>
          </div>
        )}
      </div>

      <button id="next-button" onClick={handleNext}>次へ</button>
    </div>
  );
}

export default W6_PreferenceInput;*/

import React, { useState } from 'react';
import './W6_PreferenceInput.css';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function W6_PreferenceInput() {
  const navigate = useNavigate();
  const user_id = parseInt(localStorage.getItem('user_id')) || 0;

  const [minUnits, setMinUnits] = useState('');
  const [maxUnits, setMaxUnits] = useState('');
  const [preferredCategories, setPreferredCategories] = useState([]);
  const [showPriority, setShowPriority] = useState(false);
  const [avoidFirst, setAvoidFirst] = useState(false);
  const [preferredDays, setPreferredDays] = useState([]);
  const [avoidedDays, setAvoidedDays] = useState([]);
  const [preferredTimeSlots, setPreferredTimeSlots] = useState([]);
  const [preferences, setPreferences] = useState([]);

  const handleCheckboxChange = (value, listSetter, currentList) => {
    if (currentList.includes(value)) {
      listSetter(currentList.filter((item) => item !== value));
    } else {
      listSetter([...currentList, value]);
    }
  };

  const handleNext = async () => {
    const data = {
      user_id,
      min_units: parseInt(minUnits),
      max_units: parseInt(maxUnits),
      preferences,
      avoid_first_period: avoidFirst,
      preferred_time_slots: preferredTimeSlots,
      preferred_categories: preferredCategories,
      preferred_days: preferredDays,
      avoided_days: avoidedDays
    };

    try {
      const res = await axios.post('/user_conditions', data);
      if (res.data.status === 'ok') {
        alert("入力完了");
        navigate('/next-page');
      }
    } catch (err) {
      console.error(err);
      alert("送信に失敗しました");
    }
  };

  return (
    <div className="container">
      <h1>希望条件の入力</h1>

      <div className="input-group">
        <label>単位数</label>
        最少 <input type="number" value={minUnits} onChange={e => setMinUnits(e.target.value)} /> 単位 〜 最大
        <input type="number" value={maxUnits} onChange={e => setMaxUnits(e.target.value)} /> 単位
      </div>

      <div className="input-group">
        <input
          type="checkbox"
          id="priority-toggle"
          checked={showPriority}
          onChange={() => setShowPriority(!showPriority)}
        />
        <label htmlFor="priority-toggle">優先科目を指定する</label>

        {showPriority && (
          <div className="details-box">
            {["専門科目", "数理科目", "英語", "人文", "体育", "工学部共通科目"].map((cat) => (
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

      <div className="input-group">
        <label>プラス条件</label>
        <div className="plus-item">
          <label>希望授業名（カンマ区切り）:</label>
          <input
            type="text"
            placeholder="プログラミング入門, 数理情報処理"
            onChange={(e) => setPreferences(e.target.value.split(',').map(s => s.trim()))}
          />
        </div>

        <div className="plus-item">
          <label>希望時間帯（例: 1限, 2限）:</label>
          <input
            type="text"
            placeholder="2限, 4限"
            onChange={(e) => setPreferredTimeSlots(e.target.value.split(',').map(s => s.trim()))}
          />
        </div>

        <div className="plus-item">
          <label>
            <input
              type="checkbox"
              checked={avoidFirst}
              onChange={() => setAvoidFirst(!avoidFirst)}
            />
            1限を避けたい
          </label>
        </div>
      </div>

      <div className="input-group">
        <label>曜日の希望</label>
        <div>
          避けたい曜日:
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

        <div>
          出たい曜日:
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

      <button id="next-button" onClick={handleNext}>次へ</button>
    </div>
  );
}

export default W6_PreferenceInput;

