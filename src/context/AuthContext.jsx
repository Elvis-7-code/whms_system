import {
  createContext,
  useContext,
  useEffect,
  useState,
  useCallback,
} from 'react';

import { authService } from '../services/authService';

const AuthContext = createContext(null);

const USER_KEY = 'authUser';
const TOKEN_KEY = 'authToken';

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem(TOKEN_KEY);

    if (!token) {
      setLoading(false);
      return;
    }

    authService
      .getCurrentUser()
      .then((res) => {
        setUser(res.data);
      })
      .catch(() => {
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
        setUser(null);
      })
      .finally(() => {
        setLoading(false);
      });
  }, []);

  const login = useCallback(async (email, password) => {
    const res = await authService.login(email, password);

    localStorage.setItem(TOKEN_KEY, res.token);
    localStorage.setItem(USER_KEY, JSON.stringify(res.user));

    setUser(res.user);

    return res.user;
  }, []);

  const signup = useCallback(async (payload) => {
    const res = await authService.signup(payload);

    localStorage.setItem(TOKEN_KEY, res.token);
    localStorage.setItem(USER_KEY, JSON.stringify(res.user));

    setUser(res.user);

    return res.user;
  }, []);

  const logout = useCallback(async () => {
    await authService.logout();

    setUser(null);
  }, []);

  const value = {
    user,
    isAuthenticated: Boolean(user),
    loading,
    login,
    signup,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      'useAuth must be used within an AuthProvider'
    );
  }

  return context;
}