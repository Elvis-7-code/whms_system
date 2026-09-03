import React from 'react'

export default function Signup() {
    const {} = useAuth();
    const navigate = useNavigate();
    const [form, setForm] = useState({ name: "", email: "", password: "" });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            //BACKEND CALL: POST {baseURL}/auth/signup
            await signup(form.name, form.email, form.password);
            navigate(PATHS.LOGIN);
        } catch (err) {
            setError(err?.response?.data?.message || 'Signup failed. Please check your details and try again.');
        } finally {
            setLoading(false);
        }
    };

     return (
    <div className="flex items-center justify-center" style={{ minHeight: '100vh', background: 'var(--color-bg)' }}>
      <form onSubmit={handleSubmit} className="card" style={{ width: 380, padding: 32 }}>
        <h1 style={{ fontSize: 20, marginBottom: 4 }}>Create your account</h1>
        <p className="text-secondary" style={{ fontSize: 13, marginBottom: 24 }}>
          Set up Wahome Herd Management for your farm
        </p>

        {error && (
          <div style={{ background: 'var(--color-danger-light)', color: 'var(--color-danger)', padding: 10, borderRadius: 8, fontSize: 13, marginBottom: 16 }}>
            {error}
          </div>
        )}

        {[
          { name: 'name', label: 'Full name', type: 'text' },
          { name: 'farmName', label: 'Farm name', type: 'text' },
          { name: 'email', label: 'Email', type: 'email' },
          { name: 'password', label: 'Password', type: 'password' },
        ].map((field) => (
          <div key={field.name} style={{ marginBottom: 16 }}>
            <label style={{ fontSize: 13, fontWeight: 600, display: 'block', marginBottom: 6 }}>{field.label}</label>
            <input
              name={field.name}
              type={field.type}
              required
              value={form[field.name]}
              onChange={handleChange}
              style={{ width: '100%', padding: '9px 12px', borderRadius: 8, border: '1px solid var(--color-border)' }}
            />
          </div>
        ))}

        <Button type="submit" fullWidth disabled={loading} style={{ marginTop: 6 }}>
          {loading ? 'Creating account...' : 'Create account'}
        </Button>

        <p className="text-secondary" style={{ fontSize: 13, marginTop: 18, textAlign: 'center' }}>
          Already have an account? <Link to={PATHS.login} style={{ color: 'var(--color-accent-green)', fontWeight: 600 }}>Log in</Link>
        </p>
      </form>
    </div>
  );
}