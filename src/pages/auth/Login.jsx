import {} from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/authContext";
import Button from "../../components/Button.jsx";
import {PATHS} from "../../routes/paths";

export default function Login() {
    const { login } = useAuth();
    const navigate = useNavigate();
    const [form, setForm] = useState({ email: "", password: "" });
    const [error, setError] = useState(false);

    const handleChange = (e) => setForm({ ...form, [e.target.name]:e.target.value});

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);
        try {
            //BACKEND CALL: POST {baseURL}/auth/login
            await login(form.email, form.password);
            navigate(PATHS.ANIMALS_LIST);
        } catch (err) {
            setError(err?.response?.data?.message || 'Login failed. Please check your details and try again.');
        } finally {
            setLoading(false);
        }
    };

   return (
    <div className="flex items-center justify-center" style={{ minHeight: '100vh', background: 'var(--color-bg)' }}>
      <form onSubmit={handleSubmit} className="card" style={{ width: 360, padding: 32 }}>
        <h1 style={{ fontSize: 20, marginBottom: 4 }}>Welcome back</h1>
        <p className="text-secondary" style={{ fontSize: 13, marginBottom: 24 }}>
          Log in to Wahome Herd Management System
        </p>

        {error && (
          <div style={{ background: 'var(--color-danger-light)', color: 'var(--color-danger)', padding: 10, borderRadius: 8, fontSize: 13, marginBottom: 16 }}>
            {error}
          </div>
        )}

        <label style={{ fontSize: 13, fontWeight: 600, display: 'block', marginBottom: 6 }}>Email</label>
        <input
          name="email"
          type="email"
          required
          value={form.email}
          onChange={handleChange}
          style={{ width: '100%', padding: '9px 12px', borderRadius: 8, border: '1px solid var(--color-border)', marginBottom: 16 }}
        />

        <label style={{ fontSize: 13, fontWeight: 600, display: 'block', marginBottom: 6 }}>Password</label>
        <input
          name="password"
          type="password"
          required
          value={form.password}
          onChange={handleChange}
          style={{ width: '100%', padding: '9px 12px', borderRadius: 8, border: '1px solid var(--color-border)', marginBottom: 22 }}
        />

        <Button type="submit" fullWidth disabled={loading}>
          {loading ? 'Logging in...' : 'Log in'}
        </Button>

        <p className="text-secondary" style={{ fontSize: 13, marginTop: 18, textAlign: 'center' }}>
          Don't have an account? <Link to={PATHS.signup} style={{ color: 'var(--color-accent-green)', fontWeight: 600 }}>Sign up</Link>
        </p>
      </form>
    </div>
  );
}