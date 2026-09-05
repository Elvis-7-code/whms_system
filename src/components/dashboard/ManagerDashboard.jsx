import StatCard from './StatCard.jsx';
import RecentActivity from './RecentActivity.jsx';
import QuickActions from './QuickActions.jsx';

function ManagerDashboard() {
  const activities = [
    {
      id: 1,
      icon: '🐄',
      title: 'Animal record updated',
      description: 'COW-001 details were updated.',
      time: 'Today',
    },
    {
      id: 2,
      icon: '❤️',
      title: 'Breeding record added',
      description: 'A new breeding record was created.',
      time: 'Today',
    },
    {
      id: 3,
      icon: '💉',
      title: 'Vaccination due',
      description: '3 animals have upcoming vaccinations.',
      time: 'Yesterday',
    },
  ];

  const actions = [
    {
      id: 1,
      label: 'Record Breeding',
      icon: '❤️',
    },
    {
      id: 2,
      label: 'Update Feed',
      icon: '🌾',
    },
    {
      id: 3,
      label: 'Update Vaccination',
      icon: '💉',
    },
    {
      id: 4,
      label: 'View Alerts',
      icon: '🔔',
    },
  ];

  return (
    <div className="role-dashboard manager-dashboard">
      <div className="dashboard-heading">
        <h1>Manager Dashboard</h1>
        <p>Monitor and manage daily farm operations.</p>
      </div>

      <div className="stats-grid">
        <StatCard
          title="Total Animals"
          value="42"
          icon="🐄"
          description="Animals in the herd"
        />

        <StatCard
          title="Breeding"
          value="12"
          icon="❤️"
          description="Active breeding records"
        />

        <StatCard
          title="Vaccinations Due"
          value="5"
          icon="💉"
          description="Upcoming vaccinations"
        />

        <StatCard
          title="Alerts"
          value="4"
          icon="🔔"
          description="Alerts requiring attention"
        />
      </div>

      <div className="dashboard-grid">
        <RecentActivity activities={activities} />

        <QuickActions actions={actions} />
      </div>
    </div>
  );
}

export default ManagerDashboard;