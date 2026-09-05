function PublicFooter() {
  return (
    <footer className="public-footer">
      <div className="public-footer-inner">
        <div>
          <div className="public-brand-name" style={{ color: '#fff' }}>
            Wahome Herd Management System
          </div>
          <p>Practical farm management for real farms.</p>
        </div>
        <div className="public-footer-links">
          <a href="#features">Features</a>
          <a href="#products">Milk &amp; Cattle</a>
          <a href="#contact">Contact</a>
        </div>
        <p className="public-footer-copy">
          © {new Date().getFullYear()} Wahome Herd Management System. All rights reserved.
        </p>
      </div>
    </footer>
  );
}

export default PublicFooter;