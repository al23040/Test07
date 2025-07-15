// src/api.js

const BASE_URL = '/api';

/**
 * ユーザーログイン (C5 API)
 */
export const loginUser = async (userId, password) => {
  try {
    const response = await fetch(`${BASE_URL}/c5/users/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, password }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || 'Login failed');
    }
    return data;
  } catch (error) {
    console.error("Error logging in user:", error);
    throw error;
  }
};

/**
 * ユーザー登録 (C5 API)
 */
export const registerUser = async (userId, password) => {
  try {
    const response = await fetch(`${BASE_URL}/c5/users/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: userId, password }),
    });
    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.message || 'Registration failed');
    }
    return data;
  } catch (error) {
    console.error("Error registering user:", error);
    throw error;
  }
};


// ===============================================================
// C4のAPI
// ===============================================================

/**
 * 4年間の履修パターンリストを取得します。
 */
export const fetchFourYearPatterns = async (userId, conditions, completedCourses, allCourses) => {
  try {
    const response = await fetch(`${BASE_URL}/c4/four-year-patterns`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        user_id: userId,
        conditions,
        completed_courses: completedCourses,
        all_courses: allCourses }),
    });
    if (!response.ok) throw new Error(`サーバーエラー (status: ${response.status})`);
    return await response.json();
  } catch (error) {
    console.error("4年間履修パターンの取得に失敗:", error);
    throw error;
  }
};

/**
 * 4年間の履修パターンの詳細を取得します。
 */
export const fetchFourYearPatternDetail = async (patternId) => {
  try {
    // 詳細取得なのでGETメソッドを使用します
    const response = await fetch(`${BASE_URL}/c4/patterns/${patternId}`, { 
      method: 'GET' 
    });
    if (!response.ok) throw new Error(`サーバーエラー (status: ${response.status})`);
    return await response.json();
  } catch (error) {
    console.error("履修パターン詳細の取得に失敗しました:", error);
    throw error;
  }
};

/**
 * 今学期のおすすめ履修データを取得します。
 */
export const fetchCurrentSemesterRecommendation = async (userId, conditions, completedCourses, availableCourses) => {
  try {
    const response = await fetch(`${BASE_URL}/c4/current-semester-recommendation`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        user_id: userId,
        conditions,
        completed_courses: completedCourses,
        available_courses: availableCourses }),
    });
    if (!response.ok) throw new Error(`サーバーエラー (status: ${response.status})`);
    return await response.json();
  } catch (error) {
    console.error("今学期のおすすめ履修の取得に失敗しました:", error);
    throw error;
  }
};


// ===============================================================
// C5のAPI
// ===============================================================

/**
 * 全科目のリストを取得します。
 */
export const fetchAllSubjects = async () => {
  try {
    const response = await fetch(`${BASE_URL}/c5/subjects`);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    return data.subjects || [];
  } catch (error) {
    console.error("全科目リストの取得に失敗しました:", error);
    throw error;
  }
};

/**
 * ユーザーの履修済み科目リストを取得します。
 */
export const fetchUserTakenCourses = async (userId) => {
  try {
    const response = await fetch(`${BASE_URL}/c5/users/${userId}/courses`);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    const data = await response.json();
    return data.completed_courses || [];
  } catch (error) {
    console.error(`履修済み科目リストの取得に失敗しました:`, error);
    throw error;
  }
};