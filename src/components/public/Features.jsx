import {
  PawPrint,
  HeartPulse,
  Utensils,
  Syringe,
  Bell,
  ShoppingCart,
  FileBarChart,
  Users,
} from 'lucide-react';

const FEATURES = [
  {
    icon: PawPrint,
    title: 'Animal Records',
    description: 'Track every cow, goat, and sheep — tag, breed, status, and full history in one place.',
  },
  {
    icon: HeartPulse,
    title: 'Breeding Tracking',
    description: 'Know exactly when each animal is due, with pregnancy and birth records kept up to date.',
  },
  {
    icon: Utensils,
    title: 'Feed Management',
    description: 'Monitor stock levels and get warned before you run low on maize bran, hay, or minerals.',
  },
  {
    icon: Syringe,
    title: 'Vaccination Schedules',
    description: 'Never miss a vaccination window with reminders tied to each animal.',
  },
  {
    icon: Bell,
    title: 'Real-time Alerts',
    description: 'Low feed, upcoming births, and vaccination due dates — sent to you the moment they happen.',
  },
  {
    icon: ShoppingCart,
    title: 'Sales Tracking',
    description: 'Record milk and livestock sales, and see your revenue at a glance.',
  },
  {
    icon: FileBarChart,
    title: 'Reports',
    description: 'Herd growth, sales performance, and feed usage — summarized, not buried in spreadsheets.',
  },
  {
    icon: Users,
    title: 'Role-based Access',
    description: 'Owners, managers, and workers each see exactly what they need — nothing more, nothing less.',
  },
];

function Features() {
  return (
    <section id="features" className="section">
      <div className="section-header">
        <span className="section-eyebrow">What you get</span>
        <h2>Everything your farm needs, in one system</h2>
      </div>

      <div className="feature-grid">
        {FEATURES.map(({ icon: Icon, title, description }) => (
          <div className="feature-card" key={title}>
            <div className="feature-icon">
              <Icon size={22} />
            </div>
            <h3>{title}</h3>
            <p>{description}</p>
          </div>
        ))}
      </div>
    </section>
  );
}

export default Features;