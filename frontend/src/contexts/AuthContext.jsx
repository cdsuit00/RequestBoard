import React, { createContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [token, setToken] = useState(localStorage.getItem('rb_token'));
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('rb_user') || 'null'));

  useEffect(() => {
    if (token) localStorage.setItem('rb_token', token); else localStorage.removeItem('rb_token');
    if (user) localStorage.setItem('rb_user', JSON.stringify(user)); else localStorage.removeItem('rb_user');
  }, [token, user]);

  const logout = () => { setToken(null); setUser(null); };

  return (
    <AuthContext.Provider value={{ token, setToken, user, setUser, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export default AuthContext;
