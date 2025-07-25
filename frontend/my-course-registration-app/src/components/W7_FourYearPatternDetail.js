// frontend/my-course-registration-app/src/components/W7_FourYearPatternDetail.js
import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { fetchFourYearPatternDetail } from '../api';
import { useAuth } from '../context/AuthContext';
import { useConditions } from '../context/ConditionsContext';
import axios from 'axios';
import './W7_FourYearPatternDetail.css';

const W7_FourYearPatternDetail = () => {
  const { patternId } = useParams();
  const [patternDetail, setPatternDetail] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const { userId } = useAuth();
  const { conditions } = useConditions();
  const [completedCourses, setCompletedCourses] = useState(null);
  const [allCourses, setAllCourses] = useState(null);

  useEffect(() => {
    const getCourseData = async () => {
      if (!userId) return;
      setLoading(true);
      try {
        const dataToSend = { userId, conditions };
        const response = await axios.post(`/api/c7/user_allcourses/${userId}`, dataToSend);
        console.log('API Response:', response.data); 
        setCompletedCourses(response.data.completed_courses);
        setAllCourses(response.data.all_courses);
      } catch (err) {
        setError(err);
      }
    };
    getCourseData();
  }, [userId, conditions]);

  useEffect(() => {
    console.log('Dependencies for getDetail:', {
        patternId,
        userId,
        conditions,
        completedCourses,
        allCourses
    });
    if (!userId || !completedCourses || !allCourses) return;

    const getDetail = async () => {
      try {
        const data = await fetchFourYearPatternDetail(patternId, userId, conditions, completedCourses, allCourses);
        console.log('Pattern Detail Data:', data);
        setPatternDetail(data);
      } catch (err) {
        console.error('getDetail Error:', err);
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    getDetail();
  }, [patternId, userId, conditions, completedCourses, allCourses]);

  if (loading) {
    return <div className="loading-container"><div className="loader"></div><p>パターン詳細を読み込み中...</p></div>;
  }
  if (error) {
    return <div className="error-container"><p>エラー: {error.message}</p></div>;
  }
  if (!patternDetail) {
    return <p>パターンの詳細が見つかりません。</p>;
  }

  return (
    <div className="pattern-detail-container">
      <header className="pattern-detail-header">
        <h1>{patternDetail.name}</h1>
        <p className="pattern-description">{patternDetail.description}</p>
        <div className="pattern-meta">
          <span>総単位数: <strong>{patternDetail.totalUnits}</strong></span>
        </div>
      </header>

      <section className="course-section">
        <h2>推奨科目リスト</h2>
        {patternDetail.recommendedSubjects && patternDetail.recommendedSubjects.length > 0 ? (
          <ul className="course-list-detail">
            {patternDetail.recommendedSubjects.map((course) => (
              <li key={course.id}>
                <div className="course-info">
                  <span className="course-name">{course.name}</span>
                  <span className="course-details">
                    {course.year}年次 {course.semester} / {course.category} / {course.units}単位
                  </span>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p>推奨される科目は見つかりませんでした。</p>
        )}
      </section>

      <footer className="pattern-detail-footer">
        <Link to="/patterns" className="back-link">← パターン一覧へ戻る</Link>
      </footer>
    </div>
  );
};

export default W7_FourYearPatternDetail;