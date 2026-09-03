import { useEffect, useState } from 'react';
import { vaccinationService } from '../../services/vaccinationService.js';
import Loader from '../../components/common/Loader.jsx';

/**
 * TODO: replicate the fetch -> loading -> error -> render pattern
 * from src/pages/animals/AnimalsList.jsx once the backend is ready.
 *
 * BACKEND CALL: GET /vaccinations
 */
export default function Vaccinations() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    // Uncomment once the backend exists:
    // setLoading(true);
    // vaccinationService.getAll()
    //   .then((res) => { /* setData(res.data) */ })
    //   .catch(() => setError('Could not load Vaccinations.'))
    //   .finally(() => setLoading(false));
  }, []);}