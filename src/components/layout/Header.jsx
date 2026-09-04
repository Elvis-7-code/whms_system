import { useAuth } from '../../context/AuthContext.jsx';

function Header({ onMenuClick }) {
  const { user } = useAuth();

  return (
    <header className="app-header">
      <div className="header-left">
        <button
          type="button"
          className="menu-button"
          onClick={onMenuClick}
          aria-label="Open navigation"
        >
          ☰
        </button>

        <div className="header-title">
          <span>Wahome Herd Management System</span>
        </div>
      </div>

      <div className="header-right">
        <button
          type="button"
          className="notification-button"
          aria-label="Notifications"
        >
          🔔
        </button>

        <div className="header-user">
          <div className="user-avatar">
            {user?.name
              ? user.name.charAt(0).toUpperCase()
              : 'U'}
          </div>

          <div className="user-info">
            <strong>{user?.name || 'User'}</strong>

            <span>{user?.role || 'Worker'}</span>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Header;
