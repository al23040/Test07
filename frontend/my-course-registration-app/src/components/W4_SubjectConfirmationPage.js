// src/components/W4_SubjectConfirmationPage.js
import React, { useState, useEffect } from 'react';
import './W4_SubjectConfirmationPage.css';
import { useNavigate } from 'react-router-dom';

function SubjectConfirmationPage() {
  const navigate = useNavigate();
  const [parsedCourses, setParsedCourses] = useState([]);
  const [availableCourses, setAvailableCourses] = useState([]);
  const [creditData, setCreditData] = useState(null);
  const [totalCredits, setTotalCredits] = useState(0);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const storedParsed = localStorage.getItem('parsedCourses');
    const storedAvailable = localStorage.getItem('availableCourses');
    const storedCredits = localStorage.getItem('creditData');

    if (storedParsed && storedAvailable && storedCredits) {
      const parsed = JSON.parse(storedParsed);
      const available = JSON.parse(storedAvailable);
      const credits = JSON.parse(storedCredits);

      setParsedCourses(parsed);
      setAvailableCourses(available);
      setCreditData(credits);

      const total = parsed.reduce((sum, sub) => sum + sub.credit, 0);
      setTotalCredits(total);
    }
  }, []);

  const handleEditSubjects = () => {
    navigate('/subject-edit');
  };

  const handleConfirm = async () => {
    const payload = {
      courses: parsedCourses,
      available_courses: availableCourses,
      credit_data: creditData
    };

    try {
      const response = await fetch('/api/c3/courses/submit', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) throw new Error('送信に失敗しました');

      setMessage('履修科目データを正常に送信しました。');
    } catch (err) {
      console.error('送信エラー:', err);
      setMessage('送信に失敗しました。data.json をダウンロードします。');

    }
  };

  return (
    <div className="subject-confirmation-container">
      <h2>履修登録状況の入力</h2>

      {parsedCourses.length === 0 ? (
        <p className="no-subjects-message">履修済み科目がありません。</p>
      ) : (
        <>
          <div className="category-section-container">
            <div className="category-section">
              <h3>履修済み科目</h3>
              <ul>
                {parsedCourses.map((course, idx) => (
                  <li key={idx}>
                    <span>{course.subject_name}</span>
                    <span>{course.credit}単位</span>
                    <span>{course.category}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="category-section">
              <h3>履修可能な科目</h3>
              <ul>
                {availableCourses.map((course, idx) => (
                  <li key={idx}>
                    <span>{course.subject_name}</span>
                    <span>{course.credit}単位</span>
                    <span>{course.category}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {creditData && (
            <div className="credit-summary">
              <h3>単位内訳</h3>
              <ul>
                {Object.entries(creditData).map(([categoryKey, value]) => {
                  if (typeof value === 'number') {
                    if (value === 0) return null;
                    const labelMap = {
                      university_common_credits: '全学共通科目',
                      informatics_credits: '情報科目'
                    };
                    return (
                      <li key={categoryKey}>
                        {labelMap[categoryKey] || categoryKey}: {value}単位
                      </li>
                    );
                  }

                  const categoryLabelMap = {
                    common_math_credits: '共通数理科目',
                    language_credits: '言語科目',
                    social_sciences_credits: '人文社会系教養科目',
                    major_credits: '専門科目',
                    PE_health_credits: '共通健康科目'
                  };

                  const requirementLabelMap = {
                    compulsory: '必修',
                    elective_compulsory: '選択必修',
                    elective: '選択'
                  };

                  return Object.entries(value).map(([reqKey, count]) => {
                    if (!count || count === 0) return null;
                    const categoryLabel = categoryLabelMap[categoryKey] || categoryKey;
                    const requirementLabel = requirementLabelMap[reqKey] || reqKey;
                    return (
                      <li key={`${categoryKey}-${reqKey}`}>
                        {categoryLabel}（{requirementLabel}）: {count}単位
                      </li>
                    );
                  });
                })}
              </ul>
              <p><strong>合計: {totalCredits}単位</strong></p>
            </div>
          )}
        </>
      )}

      <div className="button-group">
        <button onClick={handleEditSubjects} className="edit-button">編集</button>
        <button onClick={handleConfirm} className="confirm-button">確定</button>
      </div>
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default SubjectConfirmationPage;
