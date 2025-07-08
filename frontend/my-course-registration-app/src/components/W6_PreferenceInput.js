// W6_PreferenceInput.js
import React, { useState } from 'react';
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

export default W6_PreferenceInput;
