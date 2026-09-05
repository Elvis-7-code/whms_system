import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext.jsx';
import { PATHS } from '../../routes/paths';

function Sidebar({ isOpen, onClose }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const role = user?.role;

  const links = [
    {
      label: 'Dashboard',
      path: PATHS.dashboard,
      roles: ['owner', 'admin', 'manager', 'worker'],
    },
    {
      label: 'Animals',
      path: PATHS.animals,
      roles: ['owner', 'admin', 'manager', 'worker'],
    },
    {
      label: 'Feed',
      path: PATHS.feed,
      roles: ['owner', 'admin', 'manager', 'worker'],
    },
    {
      label: 'Vaccinations',
      path: PATHS.vaccinations,
      roles: ['owner', 'admin', 'manager', 'worker'],
    },
    {
      label: 'Breeding',
      path: PATHS.breeding,
      roles: ['owner', 'admin', 'manager'],
    },
    {
      label: 'Alerts',
      path: PATHS.alerts,
      roles: ['owner', 'admin', 'manager', 'worker'],
    },
    {
      label: 'Reports',
      path: PATHS.reports,
      roles: ['owner', 'admin', 'manager'],
    },
    {
      label: 'Users',
      path: PATHS.users,
      roles: ['owner', 'admin'],
    },
    {
      label: 'Settings',
      path: PATHS.settings,
      roles: ['owner', 'admin'],
    },
  ];

  const visibleLinks = links.filter((link) => link.roles.includes(role));

  const initials = user?.name
    ? user.name
        .split(' ')
        .map((part) => part[0])
        .slice(0, 2)
        .join('')
        .toUpperCase()
    : '?';

  const handleLogout = async () => {
    await logout();
    onClose?.(); // close mobile drawer if open
    navigate(PATHS.landing, { replace: true });
  };

  return (
    <>
      {isOpen && <div className="sidebar-overlay" onClick={onClose} />}
      <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <h2>WHMS</h2>
          <button
            type="button"
            onClick={onClose}
            className="sidebar-close"
            aria-label="Close navigation"
          >
            ×
          </button>
        </div>

        <nav className="sidebar-nav">
          {visibleLinks.map((link) => (
            <NavLink
              key={link.path}
              to={link.path}
              onClick={onClose}
              className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
            >
              {link.label}
            </NavLink>
          ))}
        </nav>

        <div className="sidebar-user">
          <div className="sidebar-user-avatar">{initials}</div>
          <div className="sidebar-user-info">
            <strong>{user?.name ?? 'Guest'}</strong>
            <span>{role ?? ''}</span>
          </div>
        </div>

        <button
          type="button"
          onClick={handleLogout}
          className="sidebar-link"
          style={{ width: '100%', border: 'none', background: 'transparent', marginTop: '4px' }}
        >
          Logout
        </button>
      </aside>
    </>
  );
}

export default Sidebar;