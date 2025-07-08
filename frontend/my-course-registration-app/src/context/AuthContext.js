// src/context/AuthContext.js
import React, { createContext, useContext, useState } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [userId, setUserId] = useState(localStorage.getItem('user_id') || null);

  const login = (id) => {
    setUserId(id);
    localStorage.setItem('user_id', id);
  };

  const logout = () => {
    setUserId(null);
    localStorage.removeItem('user_id');
  };

  return (
    <AuthContext.Provider value={{ userId, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
