// src/components/W5_SubjectEditPage.js
import React, { useState, useEffect } from 'react';
import './W5_SubjectEditPage.css';
import { useNavigate } from 'react-router-dom';

function SubjectEditPage() {
  const navigate = useNavigate();
  const [subjects, setSubjects] = useState([]);
  const [newSubject, setNewSubject] = useState({
    subject_name: '',
    code: '',
    category: '',
    requirement: '',
    credit: ''
  });

  useEffect(() => {
    const stored = localStorage.getItem('parsedCourses');
    if (stored) {
      setSubjects(JSON.parse(stored));
    }
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewSubject(prev => ({ ...prev, [name]: value }));
  };

  const handleAdd = () => {
    const { subject_name, credit } = newSubject;
    if (subject_name.trim() === '' || credit === '') {
      alert('科目名と単位数は必須です。');
      return;
    }

    const updatedSubjects = [...subjects, { ...newSubject, credit: Number(credit) }];
    setSubjects(updatedSubjects);
    setNewSubject({
      subject_name: '',
      code: '',
      category: '',
      requirement: '',
      credit: ''
    });
  };

  const handleDelete = (index) => {
    const updated = [...subjects];
    updated.splice(index, 1);
    setSubjects(updated);
  };

  const toKey = (req) => {
    switch (req) {
      case '必修': return 'compulsory';
      case '選択必修': return 'elective_compulsory';
      case '選択': return 'elective';
      default: return 'elective';
    }
  };

  const computeCreditData = (subjects) => {
    const creditData = {
      university_common_credits: 0,
      informatics_credits: 0,
      common_math_credits: { compulsory: 0, elective_compulsory: 0, elective: 0 },
      language_credits: { compulsory: 0, elective_compulsory: 0, elective: 0 },
      social_sciences_credits: { compulsory: 0, elective_compulsory: 0, elective: 0 },
      PE_health_credits: { compulsory: 0, elective_compulsory: 0, elective: 0 },
      major_credits: { compulsory: 0, elective_compulsory: 0, elective: 0 }
    };

    subjects.forEach(sub => {
      const cat = sub.category;
      const req = toKey(sub.requirement);
      const credit = Number(sub.credit);

      switch (cat) {
        case '全学共通科目':
          creditData.university_common_credits += credit;
          break;
        case '情報科目':
          creditData.informatics_credits += credit;
          break;
        case '共通数理科目':
          creditData.common_math_credits[req] += credit;
          break;
        case '言語科目':
          creditData.language_credits[req] += credit;
          break;
        case '人文社会系教養科目':
          creditData.social_sciences_credits[req] += credit;
          break;
        case '共通健康科目':
          creditData.PE_health_credits[req] += credit;
          break;
        case '専門科目':
          creditData.major_credits[req] += credit;
          break;
        default:
          break;
      }
    });

    return creditData;
  };

  const handleNext = () => {
    localStorage.setItem('parsedCourses', JSON.stringify(subjects));
    const updatedCreditData = computeCreditData(subjects);
    localStorage.setItem('creditData', JSON.stringify(updatedCreditData));
    navigate('/subject-confirmation');
  };

  return (
    <div className="subject-edit-container">
      <h2>履修科目の編集</h2>

      <div className="subject-list-section">
        <h3>登録済み科目</h3>
        <table className="subjects-edit-table">
          <thead>
            <tr>
              <th>科目名</th>
              <th>コード</th>
              <th>区分</th>
              <th>必修/選択</th>
              <th>単位</th>
              <th>操作</th>
            </tr>
          </thead>
          <tbody>
            {subjects.map((sub, idx) => (
              <tr key={idx}>
                <td>{sub.subject_name}</td>
                <td>{sub.code}</td>
                <td>{sub.category}</td>
                <td>{sub.requirement}</td>
                <td>{sub.credit}</td>
                <td>
                  <button onClick={() => handleDelete(idx)} className="delete-button">削除</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="add-subject-form">
        <input
          type="text"
          name="subject_name"
          placeholder="科目名"
          value={newSubject.subject_name}
          onChange={handleInputChange}
        />
        <input
          type="text"
          name="code"
          placeholder="コード"
          value={newSubject.code}
          onChange={handleInputChange}
        />
        <select
          name="category"
          value={newSubject.category}
          onChange={handleInputChange}
        >
          <option value="">区分を選択</option>
          <option value="全学共通科目">全学共通科目</option>
          <option value="共通数理科目">共通数理科目</option>
          <option value="言語科目">言語科目</option>
          <option value="人文社会系教養科目">人文社会系教養科目</option>
          <option value="共通健康科目">共通健康科目</option>
          <option value="専門科目">専門科目</option>
          <option value='共通工学系教養科目'>共通工学系教養科目</option>
        </select>
        <select
          name="requirement"
          value={newSubject.requirement}
          onChange={handleInputChange}
        >
          <option value="">必修/選択</option>
          <option value="必修">必修</option>
          <option value="選択必修">選択必修</option>
          <option value="選択">選択</option>
        </select>
        <input
          type="number"
          name="credit"
          placeholder="単位数"
          value={newSubject.credit}
          onChange={handleInputChange}
          min="1"
          max="4"
        />
        <button onClick={handleAdd} className="add-button">追加</button>
      </div>

      <div className="button-group">
        <button onClick={handleNext} className="next-button">次へ</button>
      </div>
    </div>
  );
}

export default SubjectEditPage;

