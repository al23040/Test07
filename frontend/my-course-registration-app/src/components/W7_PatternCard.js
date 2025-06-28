// src/components/PatternCard.js
import React from 'react';
import './W7_PatternCard.css';

function PatternCard({ pattern, onViewDetails }) {
  return (
    <div className="pattern-card">
      <h3>パターン {pattern.id}</h3>
      <p><strong>総単位数:</strong> {pattern.totalUnits}</p>
      <p><strong>残単位数:</strong> {pattern.remainingUnits}</p>
      <p><strong>基本情報技術者試験内容習得率:</strong> {pattern.itSkillAcquisitionRate}%</p>
      <p><strong>概要:</strong> {pattern.description}</p>
      <div className="course-lists">
        <h4>主要科目:</h4>
        <ul>
          {pattern.coreCourses.map((course, index) => (
            <li key={`core-${index}`}>{course}</li>
          ))}
        </ul>
        <h4>選択科目例:</h4>
        <ul>
          {pattern.electiveCourses.map((course, index) => (
            <li key={`elective-${index}`}>{course}</li>
          ))}
        </ul>
      </div>
      {pattern.remarks && <p className="remarks">備考: {pattern.remarks}</p>}
      <button onClick={() => onViewDetails(pattern.id)} className="detail-button">
        詳細を見る
      </button>
    </div>
  );
}

export default PatternCard;