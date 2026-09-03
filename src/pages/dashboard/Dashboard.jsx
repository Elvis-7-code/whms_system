import { useAuth } from '../../context/AuthContext.jsx';
import OwnerDashboard from '../../components/dashboard/OwnerDashboard.jsx';
import ManagerDashboard from '../../components/dashboard/ManagerDashboard.jsx';
import WorkerDashboard from '../../components/dashboard/WorkerDashboard.jsx';

/**
 * ================================================================
 *  BACKEND INTEGRATION POINT
 * ================================================================
 * Right now each role dashboard renders with mock data (imported
 * inside OwnerDashboard.jsx / ManagerDashboard.jsx / WorkerDashboard.jsx).
 *
 * To wire this to a real backend, replace the mock-data defaults with
 * a fetch here, e.g.:
 *
 *   const [data, setData] = useState(null);
 *   useEffect(() => {
 *     Promise.all([
 *       animalService.getAll(),
 *       breedingService.getUpcomingBirths(),
 *       feedService.getLevels(),
 *       alertService.getAll(),
 *     ]).then(([animals, births, feed, alerts]) => {
 *       setData({ ...shape it to match mockDashboard.js... });
 *     });
 *   }, []);
 *
 * Then pass `data={data}` into <OwnerDashboard data={data} />, etc.
 * The child components already expect exactly that shape, so no
 * further changes are needed once the backend responds correctly.
 * ================================================================
 */
export default function Dashboard() {
  const { user } = useAuth();
  const role = user?.role || 'owner';

  if (role === 'manager') return <ManagerDashboard />;
  if (role === 'worker') return <WorkerDashboard />;
  return <OwnerDashboard />;
}