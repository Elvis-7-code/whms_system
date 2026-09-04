import { Routes, Route } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute.jsx';
import PublicRoute from './PublicRoute.jsx';
import { PATHS } from './paths';

import LandingPage from '../pages/public/LandingPage.jsx';
import Login from '../pages/auth/Login.jsx';
import Signup from '../pages/auth/Signup.jsx';
import Dashboard from '../pages/dashboard/Dashboard.jsx';
import AnimalsList from '../pages/animals/AnimalsList.jsx';
import AnimalDetail from '../pages/animals/AnimalDetail.jsx';
import Breeding from '../pages/breeding/Breeding.jsx';
import Feed from '../pages/feed/Feed.jsx';
import Vaccinations from '../pages/vaccinations/Vaccinations.jsx';
import Alerts from '../pages/alerts/Alerts.jsx';
import Reports from '../pages/reports/Reports.jsx';
import Users from '../pages/users/Users.jsx';
import Settings from '../pages/settings/Settings.jsx';

export default function AppRoutes() {
  return (
    <Routes>
      {/* Public marketing page — redirects to dashboard if already logged in */}
      <Route element={<PublicRoute />}>
        <Route path={PATHS.landing} element={<LandingPage />} />
      </Route>

      {/* Public auth routes */}
      <Route path={PATHS.login} element={<Login />} />
      <Route path={PATHS.signup} element={<Signup />} />

      {/* ============================= */}
      {/* AUTHENTICATED ROUTES           */}
      {/* ============================= */}
      <Route element={<ProtectedRoute />}>
        <Route path={PATHS.dashboard} element={<Dashboard />} />
        <Route path={PATHS.animals} element={<AnimalsList />} />
        <Route path={PATHS.animalDetail()} element={<AnimalDetail />} />
        <Route path={PATHS.feed} element={<Feed />} />
        <Route path={PATHS.vaccinations} element={<Vaccinations />} />
        <Route path={PATHS.alerts} element={<Alerts />} />
      </Route>

      {/* MANAGER + ADMIN + OWNER */}
      <Route element={<ProtectedRoute allowedRoles={['owner', 'admin', 'manager']} />}>
        <Route path={PATHS.breeding} element={<Breeding />} />
      </Route>

      {/* REPORTS */}
      <Route element={<ProtectedRoute allowedRoles={['owner', 'admin', 'manager']} />}>
        <Route path={PATHS.reports} element={<Reports />} />
      </Route>

      {/* ADMIN + OWNER */}
      <Route element={<ProtectedRoute allowedRoles={['owner', 'admin']} />}>
        <Route path={PATHS.users} element={<Users />} />
        <Route path={PATHS.settings} element={<Settings />} />
      </Route>
    </Routes>
  );
}