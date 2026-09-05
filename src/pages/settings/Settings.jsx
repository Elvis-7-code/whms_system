import { useAuth } from '../../context/AuthContext.jsx';

export default function Settings() {
  const { user, isDevBypass } = useAuth();

  return (
    <div className="flex-col gap-16">
      <h1 style={{ fontSize: 20 }}>Settings</h1>

      <div className="card" style={{ maxWidth: 520 }}>
        <h3 className="card-title" style={{ marginBottom: 12 }}>Account</h3>
        <p className="text-secondary" style={{ fontSize: 13 }}>Signed in as {user?.name} ({user?.role})</p>
      </div>

      {isDevBypass && (
        <div className="card" style={{ maxWidth: 520, borderColor: 'var(--color-accent-gold)' }}>
          <h3 className="card-title" style={{ marginBottom: 8 }}>Dev preview mode is on</h3>
          <p className="text-secondary" style={{ fontSize: 13 }}>
            VITE_SKIP_AUTH is true in your .env, so login is bypassed and you
            can switch roles from the top bar. Set it to false and connect a
            real backend before shipping this to real users.
          </p>
        </div>
      )}
    </div>
  );
}