import { useEffect, useState } from 'react';
import { reportService } from '../../services/reportService.js';
import Loader from '../../components/common/Loader.jsx';

/**
 * TODO: replicate the fetch -> loading -> error -> render pattern
 * from src/pages/animals/AnimalsList.jsx once the backend is ready.
 *
 * BACKEND CALL: GET /reports/sales-summary
 */
export default function Reports() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    // Uncomment once the backend exists:
    // setLoading(true);
    // reportService.getAll()
    //   .then((res) => { /* setData(res.data) */ })
    //   .catch(() => setError('Could not load Reports.'))
    //   .finally(() => setLoading(false));
  }, []);

  if (loading) return <Loader label="Loading Reports..." />;

  return (
    <div className="flex-col gap-16">
      <h1 style={{ fontSize: 20 }}>Reports</h1>
      <div className="card">
        <p className="text-secondary" style={{ fontSize: 13 }}>
          This page is scaffolded and ready to wire up. It will call
          <code> GET /reports/sales-summary</code> once your backend exists.
        </p>
        {error && <p style={{ color: 'var(--color-danger)', fontSize: 13, marginTop: 8 }}>{error}</p>}
      </div>
    </div>
  );
}