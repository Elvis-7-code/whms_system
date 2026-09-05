import { Link } from 'react-router-dom';

function Hero() {
  return (
    <section className="hero">
      <div className="hero-overlay" />
      <div className="hero-content">
        <span className="hero-eyebrow">Trusted by farms across Kenya</span>
        <h1>
          Run your farm with clarity,
          <br />
          not guesswork.
        </h1>
        <p>
          Wahome Herd Management System keeps your animals, breeding records,
          feed, vaccinations, and sales in one place — so you always know
          exactly what's happening on your farm, wherever you are.
        </p>
        <div className="hero-actions">
          <Link to="/signup" className="btn btn-primary btn-lg">
            Get Started Free
          </Link>
          <a href="#products" className="btn btn-outline btn-lg">
            See Our Produce
          </a>
        </div>
      </div>
    </section>
  );
}

export default Hero;