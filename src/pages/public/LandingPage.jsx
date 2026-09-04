import PublicNavbar from '../../components/public/PublicNavbar.jsx';
import Hero from '../../components/public/Hero.jsx';
import Features from '../../components/public/Features.jsx';
import Products from '../../components/public/Products.jsx';
import ContactSection from '../../components/public/ContactSection.jsx';
import PublicFooter from '../../components/public/PublicFooter.jsx';
import '../../styles/public.css';

function LandingPage() {
  return (
    <div className="public-page">
      <PublicNavbar />
      <Hero />
      <Features />
      <Products />
      <ContactSection />
      <PublicFooter />
    </div>
  );
}

export default LandingPage;