import React, { createContext, useContext, useState } from 'react';

// 1. Context（データ置き場）を作成
const ConditionsContext = createContext();

// 2. 他のコンポーネントから簡単に使えるようにするためのカスタムフック
export const useConditions = () => {
  return useContext(ConditionsContext);
};

// 3. アプリ全体にデータを供給するためのコンポーネント
export const ConditionsProvider = ({ children }) => {
  
  // アプリケーション全体で共有したい「希望条件」のデータ
  const [conditions, setConditions] = useState({
    // ここに希望条件の初期値を設定します
    min_units: 0,
    max_units: 24,
    preferred_categories: [],
    avoid_first_period: false,
    preferred_days: [],
    avoided_days: [],
    preferred_time_slots: [],
    preferences: [], // 特に希望する科目のリストなど
  });

  // コンポーネントに渡す値（状態と、それを更新する関数）
  const value = {
    conditions,
    setConditions,
  };

  return (
    <ConditionsContext.Provider value={value}>
      {children}
    </ConditionsContext.Provider>
  );
};