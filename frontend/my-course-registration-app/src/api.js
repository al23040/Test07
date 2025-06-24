// src/api.js

const BASE_URL = 'http://127.0.0.1:5000/api'; // Flaskサーバーのアドレスとポートに合わせる

/**
 * ユーザーログイン (C5 API)
 * @param {string} userId - ユーザーID
 * @param {string} password - パスワード
 * @returns {Promise<Object>} ログイン成功時のデータ（例: { message: "Login successful", user: { id: "12345" } }）
 * @throws {Error} ログイン失敗時のエラー
 */
export const loginUser = async (userId, password) => {
  try {
    const response = await fetch(`${BASE_URL}/c5/users/login`, { // C5のAPIエンドポイントに修正
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
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
 * @param {string} userId - ユーザーID
 * @param {string} password - パスワード
 * @returns {Promise<Object>} 登録成功時のデータ（例: { message: "User registered successfully", user: { id: "new_user" } }）
 * @throws {Error} 登録失敗時のエラー
 */
export const registerUser = async (userId, password) => {
  try {
    const response = await fetch(`${BASE_URL}/c5/users/register`, { // C5のAPIエンドポイントに修正
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
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


// C4 APIエンドポイント

/**
 * 現在の学年に応じた今学期のおすすめ履修データを取得する。(C4 API)
 * @param {number} userId - ユーザーID
 * @param {Object} conditions - ユーザーが設定した条件
 * @returns {Promise<Object>} 今学期のおすすめデータ
 */
export const fetchCurrentSemesterRecommendation = async (userId, conditions) => {
  try {
    console.log(`API: C4から今学期のおすすめ履修 (ユーザー: ${userId}) データを取得中...`);
    const response = await fetch(`${BASE_URL}/c4/current-semester-recommendation`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      // バックエンドの期待する形式に合わせて調整
      // test_c4.pyのapi_requestを見ると、user_idとconditions以外に
      // completed_coursesとavailable_coursesも必要そうなので追加
      body: JSON.stringify({
        user_id: userId,
        conditions: conditions,
        // 仮のデータ。実際にはC5から取得する必要がある
        completed_courses: [], // ここにユーザーが履修済みの科目をC5から取得して渡す
        available_courses: []  // ここに利用可能な全科目をC5から取得して渡す
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching current semester recommendation from C4:", error);
    throw error;
  }
};

/**
 * 4年間の履修パターンリストを取得する。(C4 API)
 * @param {number} userId - ユーザーID
 * @param {Object} conditions - ユーザーが設定した条件
 * @returns {Promise<Array<Object>>} 4年間の履修パターンデータの配列
 */
export const fetchFourYearPatterns = async (userId, conditions) => {
  try {
    console.log(`API: C4から4年間の履修パターン (ユーザー: ${userId}) データを取得中...`);
    const response = await fetch(`${BASE_URL}/c4/four-year-patterns`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      // バックエンドの期待する形式に合わせて調整
      // test_c4.pyのapi_requestを見ると、user_idとconditions以外に
      // completed_coursesとavailable_coursesも必要そうなので追加
      body: JSON.stringify({
        user_id: userId,
        conditions: conditions,
        // 仮のデータ。実際にはC5から取得する必要がある
        completed_courses: [], // ここにユーザーが履修済みの科目をC5から取得して渡す
        available_courses: []  // ここに利用可能な全科目をC5から取得して渡す
      }),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching four year patterns from C4:", error);
    throw error;
  }
};

// C5のREADMEに記載されているその他のAPIエンドポイント (必要に応じて追加)
// これらの関数は、C5から科目やユーザーの履修履歴を取得するために使用されます。
// 現状のC4 API呼び出しではダミーデータで済ませていますが、最終的にはここから取得したデータを使うべきです。

/**
 * 全科目のリストを取得する (C5 API)
 * @returns {Promise<Array<Object>>} 全科目のリスト
 */
export const fetchAllSubjects = async () => {
    try {
        console.log("API: C5から全科目データを取得中...");
        const response = await fetch(`${BASE_URL}/c5/subjects`); // C5のAPIエンドポイントに修正
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data.subjects; // subjectsリストを直接返す
    } catch (error) {
        console.error("Error fetching all subjects from C5:", error);
        throw error;
    }
};

/**
 * ユーザーの履修済み科目リストを取得する (C5 API)
 * @param {string} userId - ユーザーID
 * @returns {Promise<Array<Object>>} ユーザーの履修済み科目リスト
 */
export const fetchUserTakenCourses = async (userId) => {
    try {
        console.log(`API: C5からユーザー ${userId} の履修済み科目データを取得中...`);
        const response = await fetch(`${BASE_URL}/c5/users/${userId}/courses`); // C5のAPIエンドポイントに修正
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data.completed_courses; // completed_coursesリストを直接返す
    } catch (error) {
        console.error(`Error fetching user ${userId} taken courses from C5:`, error);
        throw error;
    }
};