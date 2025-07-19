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

      <div className="semesters-grid">
        {patternDetail.semesters.map((semester, index) => (
          <section key={index} className="semester-card">
            <h3>{semester.year}年次 {semester.semester}</h3>
            <ul className="course-list-detail">
              {semester.courses && semester.courses.map((course, courseIndex) => (
                <li key={courseIndex}>
                  <span className="course-name">{course.name}</span>
                  <span className="course-credits">{course.credits}単位</span>
                </li>
              ))}
            </ul>
          </section>
        ))}
      </div>

      <footer className="pattern-detail-footer">
        <Link to="/patterns" className="back-link">← パターン一覧へ戻る</Link>
      </footer>
    </div>
  );
};

export default W7_FourYearPatternDetail;