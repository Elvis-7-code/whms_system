import { useAuth } from '../../context/AuthContext.jsx';
import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Button from '../../components/common/Button.jsx';
import { PATHS } from '../../routes/paths';

export default function Signup() {
  const { signup } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: '',
    farmName: '',
    email: '',
    password: '',
  });

  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError('');
    setLoading(true);

    try {
      await signup({
        name: form.name,
        farmName: form.farmName,
        email: form.email,
        password: form.password,
      });

      navigate(PATHS.dashboard);
    } catch (err) {
      setError(
        err?.message ||
          'Signup failed. Please check your details and try again.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="auth-page"
      style={{
        background: 'var(--color-bg)',
      }}
    >
      <form
        onSubmit={handleSubmit}
        className="card auth-card"
        style={{
          padding: 32,
        }}
      >
        <h1
          style={{
            fontSize: 20,
            marginBottom: 4,
          }}
        >
          Create your account
        </h1>

        <p
          className="text-secondary"
          style={{
            fontSize: 13,
            marginBottom: 24,
          }}
        >
          Set up Wahome Herd Management for your farm
        </p>

        {error && (
          <div
            style={{
              background: 'var(--color-danger-light)',
              color: 'var(--color-danger)',
              padding: 10,
              borderRadius: 8,
              fontSize: 13,
              marginBottom: 16,
            }}
          >
            {error}
          </div>
        )}

        <div style={{ marginBottom: 16 }}>
          <label
            style={{
              fontSize: 13,
              fontWeight: 600,
              display: 'block',
              marginBottom: 6,
            }}
          >
            Full name
          </label>

          <input
            name="name"
            type="text"
            required
            value={form.name}
            onChange={handleChange}
            style={{
              width: '100%',
              padding: '9px 12px',
              borderRadius: 8,
              border: '1px solid var(--color-border)',
            }}
          />
        </div>

        <div style={{ marginBottom: 16 }}>
          <label
            style={{
              fontSize: 13,
              fontWeight: 600,
              display: 'block',
              marginBottom: 6,
            }}
          >
            Farm name
          </label>

          <input
            name="farmName"
            type="text"
            required
            value={form.farmName}
            onChange={handleChange}
            style={{
              width: '100%',
              padding: '9px 12px',
              borderRadius: 8,
              border: '1px solid var(--color-border)',
            }}
          />
        </div>

        <div style={{ marginBottom: 16 }}>
          <label
            style={{
              fontSize: 13,
              fontWeight: 600,
              display: 'block',
              marginBottom: 6,
            }}
          >
            Email
          </label>

          <input
            name="email"
            type="email"
            required
            value={form.email}
            onChange={handleChange}
            style={{
              width: '100%',
              padding: '9px 12px',
              borderRadius: 8,
              border: '1px solid var(--color-border)',
            }}
          />
        </div>

        <div style={{ marginBottom: 22 }}>
          <label
            style={{
              fontSize: 13,
              fontWeight: 600,
              display: 'block',
              marginBottom: 6,
            }}
          >
            Password
          </label>

          <input
            name="password"
            type="password"
            required
            minLength={6}
            value={form.password}
            onChange={handleChange}
            style={{
              width: '100%',
              padding: '9px 12px',
              borderRadius: 8,
              border: '1px solid var(--color-border)',
            }}
          />
        </div>

        <Button
          type="submit"
          disabled={loading}
          style={{
            width: '100%',
          }}
        >
          {loading ? 'Creating account...' : 'Create account'}
        </Button>

        <p
          className="text-secondary"
          style={{
            fontSize: 13,
            marginTop: 18,
            textAlign: 'center',
          }}
        >
          Already have an account?{' '}

          <Link
            to={PATHS.login}
            style={{
              color: 'var(--color-accent-green)',
              fontWeight: 600,
            }}
          >
            Log in
          </Link>
        </p>
      </form>
    </div>
  );
}