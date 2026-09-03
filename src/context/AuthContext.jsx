import { createContext, useContext, useEffect, useState, useCallback } from 'react';
import { authService } from '../services/authService';

const AuthContext = createContext(null);

const SKIP_AUTH = import.meta.env.VITE_SKIP_AUTH === 'true';
const DEV_ROLE_DEFAULT = import.meta.env.VITE_DEV_ROLE || 'owner';

const DEV_USERS = {
  owner: { id: 'dev-owner', name: 'Victor Wahome', role: 'owner', avatar: '/images/avatars/owner.jpg' },
  manager: { id: 'dev-manager', name: 'Peter Mwangi', role: 'manager', avatar: '/images/avatars/manager.jpg' },
  worker: { id: 'dev-worker', name: 'John Kamau', role: 'worker', avatar: '/images/avatars/worker.jpg' },
};

/**
 * AuthProvider
 * ---------------------------------------------------------------
 * Real mode (VITE_SKIP_AUTH=false, the default for production):
 *   - isAuthenticated is only true once /auth/me confirms a valid
 *     token against your real backend.
 *
 * Dev preview mode (VITE_SKIP_AUTH=true):
 *   - No backend needed. ProtectedRoute lets you straight through.
 *   - `devRole` / `setDevRole` let you flip between Owner / Manager /
 *     Worker dashboards from the UI (see DevRoleSwitcher component).
 *   - This ONLY affects the frontend preview. No data is saved
 *     anywhere - it's purely for looking at the UI.
 * ---------------------------------------------------------------
 */
export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(!SKIP_AUTH);
  const [devRole, setDevRole] = useState(
    () => localStorage.getItem('devRole') || DEV_ROLE_DEFAULT
  );

  useEffect(() => {
    if (SKIP_AUTH) {
      setUser(DEV_USERS[devRole] || DEV_USERS.owner);
      setLoading(false);
      return;
    }

    const token = localStorage.getItem('authToken');
    if (!token) {
      setLoading(false);
      return;
    }

    authService
      .getCurrentUser()
      .then((res) => setUser(res.data))
      .catch(() => {
        localStorage.removeItem('authToken');
        setUser(null);
      })
      .finally(() => setLoading(false));
  }, [devRole]);

  const login = useCallback(async (credentials) => {
    const res = await authService.login(credentials);
    localStorage.setItem('authToken', res.data.token);
    setUser(res.data.user);
    return res.data.user;
  }, []);

  const signup = useCallback(async (payload) => {
    const res = await authService.signup(payload);
    localStorage.setItem('authToken', res.data.token);
    setUser(res.data.user);
    return res.data.user;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('authUser');
    setUser(null);
  }, []);

  const changeDevRole = useCallback((role) => {
    localStorage.setItem('devRole', role);
    setDevRole(role);
  }, []);

  const value = {
    user,
    isAuthenticated: SKIP_AUTH ? true : Boolean(user),
    loading,
    login,
    signup,
    logout,
    isDevBypass: SKIP_AUTH,
    devRole,
    setDevRole: changeDevRole,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within an AuthProvider');
  return ctx;
}