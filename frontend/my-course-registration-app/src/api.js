// src/api.js

// バックエンドのベースURL
const BASE_URL = 'http://127.0.0.1:5000/api'; // Flaskサーバーのアドレスとポートに合わせる

/**
 * 今学期のおすすめ履修データをバックエンドから取得する。
 * @param {number} currentYear - 現在の学年 (例: 1, 2, 3, 4)
 * @returns {Promise<Object>} 今学期のおすすめデータ
 */
export const fetchCurrentSemesterRecommendation = async (currentYear = 1) => {
  console.log(`API: 今学期のおすすめデータ (学年: ${currentYear}) を取得中...`);
  try {
    const response = await fetch(`${BASE_URL}/recommendation?currentYear=${currentYear}`);
    if (!response.ok) {
      // HTTPステータスが2xx以外の場合
      const errorData = await response.json(); // エラーレスポンスのJSONを取得
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching current semester recommendation:", error);
    throw error; // エラーを呼び出し元に再スロー
  }
};

/**
 * 4年間の履修パターンデータをバックエンドから取得する。
 * patternIdが指定された場合、そのIDのパターン詳細を返す。
 * 指定されない場合、全パターンの概要リストを返す。
 * @param {string|null} patternId - 取得したい履修パターンのID。全パターン取得の場合はnull。
 * @returns {Promise<Object|Array<Object>>} 履修パターンデータまたはそのリスト
 */
export const fetchFourYearPatterns = async (patternId = null) => {
  console.log(`API: 4年間の履修パターン (ID: ${patternId || '全パターン'}) データを取得中...`);
  let url = `${BASE_URL}/patterns`;
  if (patternId) {
    url += `?patternId=${patternId}`;
  }

  try {
    const response = await fetch(url);
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching four year patterns:", error);
    throw error;
  }
};