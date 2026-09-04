import DashboardLayout from './DashboardLayout.jsx';

function PageLayout({ children }) {
  return (
    <DashboardLayout>
      {children}
    </DashboardLayout>
  );
}

export default PageLayout;
