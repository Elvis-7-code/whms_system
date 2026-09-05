import { useEffect, useState } from 'react';
import { userService } from '../../services/userService.js';
import Loader from '../../components/common/Loader.jsx';

/**
 * TODO: replicate the fetch -> loading -> error -> render pattern
 * from src/pages/animals/AnimalsList.jsx once the backend is ready.
 *
 * BACKEND CALL: GET /users
 */
export default function Users() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    // Uncomment once the backend exists:
    // setLoading(true);
    // userService.getAll()
    //   .then((res) => { /* setData(res.data) */ })
    //   .catch(() => setError('Could not load Users.'))
    //   .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loader label="Loading Users..." />;

  return (
    <div className="flex-col gap-16">
      <h1 style={{ fontSize: 20 }}>Users</h1>
      <div className="card">
        <p className="text-secondary" style={{ fontSize: 13 }}>
          This page is scaffolded and ready to wire up. It will call
          <code> GET /users</code> once your backend exists.
        </p>
        {error && <p style={{ color: 'var(--color-danger)', fontSize: 13, marginTop: 8 }}>{error}</p>}
      </div>
    </div>
  );
}