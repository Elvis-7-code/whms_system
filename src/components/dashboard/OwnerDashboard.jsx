import StatCard from './StatCard.jsx';
import RecentActivity from './RecentActivity.jsx';
import QuickActions from './QuickActions.jsx';

function OwnerDashboard() {
  const activities = [
    {
      id: 1,
      icon: '🐄',
      title: 'New animal registered',
      description: 'COW-001 was added to the herd.',
      time: 'Today',
    },
    {
      id: 2,
      icon: '💉',
      title: 'Vaccination completed',
      description: 'BULL-001 vaccination was marked complete.',
      time: 'Today',
    },
    {
      id: 3,
      icon: '🌾',
      title: 'Feed stock updated',
      description: 'Dairy feed inventory was updated.',
      time: 'Yesterday',
    },
  ];

  const actions = [
    {
      id: 1,
      label: 'Add Animal',
      icon: '🐄',
    },
    {
      id: 2,
      label: 'Add User',
      icon: '👤',
    },
    {
      id: 3,
      label: 'Record Breeding',
      icon: '❤️',
    },
    {
      id: 4,
      label: 'View Reports',
      icon: '📊',
    },
  ];

  return (
    <div className="role-dashboard owner-dashboard">
      <div className="dashboard-heading">
        <h1>Owner Dashboard</h1>
        <p>Complete overview and control of the farm.</p>
      </div>

      <div className="stats-grid">
        <StatCard
          title="Total Animals"
          value="42"
          icon="🐄"
          description="Animals currently registered"
        />

        <StatCard
          title="Breeding Records"
          value="12"
          icon="❤️"
          description="Active breeding records"
        />

        <StatCard
          title="Low Feed Alerts"
          value="3"
          icon="🌾"
          description="Items requiring attention"
        />

        <StatCard
          title="Active Users"
          value="8"
          icon="👥"
          description="Registered system users"
        />
      </div>

      <div className="dashboard-grid">
        <RecentActivity activities={activities} />

        <QuickActions actions={actions} />
      </div>
    </div>
  );
}

export default OwnerDashboard;