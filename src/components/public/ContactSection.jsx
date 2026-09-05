import { Phone, Mail, MapPin } from 'lucide-react';
import ContactForm from './ContactForm.jsx';

function ContactSection() {
  return (
    <section id="contact" className="section">
      <div className="section-header">
        <span className="section-eyebrow">Get in touch</span>
        <h2>Want to buy milk or cattle?</h2>
        <p>Reach out directly and the farm owner will respond personally.</p>
      </div>

      <div className="contact-grid">
        <div className="contact-info">
          <div className="contact-info-item">
            <Phone size={20} />
            <div>
              <div className="contact-info-label">Call or WhatsApp</div>
              <div className="contact-info-value">+254 745 172 465</div>
            </div>
          </div>
          <div className="contact-info-item">
            <Mail size={20} />
            <div>
              <div className="contact-info-label">Email</div>
              <div className="contact-info-value">elviswachira800@gmail.com</div>
            </div>
          </div>
          <div className="contact-info-item">
            <MapPin size={20} />
            <div>
              <div className="contact-info-label">Location</div>
              <div className="contact-info-value">Nyeri County, Kenya</div>
            </div>
          </div>
        </div>

        <ContactForm />
      </div>
    </section>
  );
}

export default ContactSection;