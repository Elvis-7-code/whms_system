import { Link } from 'react-router-dom';

function PublicNavbar() {
  return (
    <header className="public-navbar">
      <div className="public-navbar-inner">
        <div className="public-brand">
          <div className="public-brand-logo" />
          <div>
            <div className="public-brand-name">Wahome Herd</div>
            <div className="public-brand-sub">MANAGEMENT SYSTEM</div>
          </div>
        </div>

        <nav className="public-nav-links">
          <a href="#features">Features</a>
          <a href="#products">Milk &amp; Cattle</a>
          <a href="#contact">Contact</a>
        </nav>

        <div className="public-nav-actions">
          {/* Update these to match your real routes/paths.js keys, e.g. PATHS.login */}
          <Link to="/login" className="btn btn-ghost">
            Log in
          </Link>
          <Link to="/signup" className="btn btn-primary">
            Get Started
          </Link>
        </div>
      </div>
    </header>
  );
}

export default PublicNavbar;