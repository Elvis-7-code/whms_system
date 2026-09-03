import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext.jsx';
import PageLayout from '../components/layout/PageLayout.jsx';
import Loader from '../components/common/Loader.jsx';
import { PATHS } from './paths';

/**
 * Gate for any route that needs a logged-in user.
 * In dev-bypass mode (VITE_SKIP_AUTH=true) this always lets you
 * through so you can preview the UI without a backend - see
 * src/context/AuthContext.jsx for details.
 */
export default function ProtectedRoute() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <Loader fullScreen label="Checking your session..." />;
  }

  if (!isAuthenticated) {
    return <Navigate to={PATHS.login} replace />;
  }

  return (
    <PageLayout>
      <Outlet />
    </PageLayout>
  );
}