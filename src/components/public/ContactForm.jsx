import { useState } from 'react';
import { Send, CheckCircle2 } from 'lucide-react';
import { sendContactMessage } from '../../services/contactService.js';

const INITIAL_FORM = {
  name: '',
  contact: '',
  interest: 'Milk',
  message: '',
};

function ContactForm() {
  const [form, setForm] = useState(INITIAL_FORM);
  const [status, setStatus] = useState('idle'); // idle | submitting | success | error

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('submitting');
    try {
      // Backend endpoint isn't built yet — this will fail gracefully until
      // POST /api/public/contact exists. Swap for a real handler then.
      await sendContactMessage(form);
      setStatus('success');
      setForm(INITIAL_FORM);
    } catch (err) {
      setStatus('error');
    }
  };

  if (status === 'success') {
    return (
      <div className="contact-success">
        <CheckCircle2 size={40} />
        <h3>Thanks, {form.name || 'friend'}!</h3>
        <p>Your message has been sent. We'll get back to you shortly.</p>
      </div>
    );
  }

  return (
    <form className="contact-form" onSubmit={handleSubmit}>
      <div className="form-row">
        <label>
          Full name
          <input
            type="text"
            name="name"
            value={form.name}
            onChange={handleChange}
            placeholder="Jane Wanjiru"
            required
          />
        </label>
        <label>
          Phone or email
          <input
            type="text"
            name="contact"
            value={form.contact}
            onChange={handleChange}
            placeholder="+254 7xx xxx xxx or you@example.com"
            required
          />
        </label>
      </div>

      <label>
        I'm interested in
        <select name="interest" value={form.interest} onChange={handleChange}>
          <option value="Milk">Milk</option>
          <option value="Cattle">Cattle</option>
          <option value="Goats/Sheep">Goats / Sheep</option>
          <option value="General">General inquiry</option>
        </select>
      </label>

      <label>
        Message
        <textarea
          name="message"
          value={form.message}
          onChange={handleChange}
          rows={4}
          placeholder="Tell us what you're looking for..."
          required
        />
      </label>

      {status === 'error' && (
        <p className="form-error">
          Couldn't send your message right now — the contact endpoint isn't
          connected yet. Try again once the backend is live.
        </p>
      )}

      <button type="submit" className="btn btn-primary btn-lg" disabled={status === 'submitting'}>
        <Send size={16} />
        {status === 'submitting' ? 'Sending...' : 'Send Message'}
      </button>
    </form>
  );
}

export default ContactForm;