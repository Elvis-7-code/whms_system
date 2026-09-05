import StatCard from './StatCard.jsx';
import RecentActivity from './RecentActivity.jsx';
import QuickActions from './QuickActions.jsx';

function WorkerDashboard() {
  const activities = [
    {
      id: 1,
      icon: '🌾',
      title: 'Feeding updated',
      description: 'Morning feeding was recorded.',
      time: 'Today',
    },
    {
      id: 2,
      icon: '💉',
      title: 'Vaccination completed',
      description: 'Vaccination was marked as completed.',
      time: 'Today',
    },
  ];

  const actions = [
    {
      id: 1,
      label: 'View Animals',
      icon: '🐄',
    },
    {
      id: 2,
      label: 'Update Feeding',
      icon: '🌾',
    },
    {
      id: 3,
      label: 'Mark Vaccination',
      icon: '💉',
    },
    {
      id: 4,
      label: 'View Alerts',
      icon: '🔔',
    },
  ];

  return (
    <div className="role-dashboard worker-dashboard">
      <div className="dashboard-heading">
        <h1>Worker Dashboard</h1>
        <p>View animals and update assigned farm activities.</p>
      </div>

      <div className="stats-grid">
        <StatCard
          title="Total Animals"
          value="42"
          icon="🐄"
          description="Animals available to view"
        />

        <StatCard
          title="Feeding Tasks"
          value="6"
          icon="🌾"
          description="Tasks for today"
        />

        <StatCard
          title="Vaccinations"
          value="3"
          icon="💉"
          description="Vaccinations due"
        />

        <StatCard
          title="Alerts"
          value="2"
          icon="🔔"
          description="Alerts to review"
        />
      </div>

      <div className="dashboard-grid">
        <RecentActivity activities={activities} />

        <QuickActions actions={actions} />
      </div>
    </div>
  );
}

export default WorkerDashboard;