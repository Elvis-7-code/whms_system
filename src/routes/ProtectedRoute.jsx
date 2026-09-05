import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';

import PageLayout from '../components/layout/PageLayout.jsx';
import Loader from '../components/common/Loader.jsx';

import { PATHS } from './paths';

export default function ProtectedRoute({
  allowedRoles = [],
}) {
  const {
    user,
    isAuthenticated,
    loading,
  } = useAuth();

  if (loading) {
    return (
      <Loader
        fullScreen
        label="Checking your session..."
      />
    );
  }

  if (!isAuthenticated) {
    return (
      <Navigate
        to={PATHS.login}
        replace
      />
    );
  }

  /*
   * If no roles are specified, any authenticated
   * user can access the route.
   */
  if (
    allowedRoles.length > 0 &&
    !allowedRoles.includes(user.role)
  ) {
    return (
      <Navigate
        to={PATHS.dashboard}
        replace
      />
    );
  }

  return (
    <PageLayout>
      <Outlet />
    </PageLayout>
  );
}