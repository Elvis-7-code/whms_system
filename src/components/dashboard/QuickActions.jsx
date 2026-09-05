function QuickActions({ actions = [] }) {
  return (
    <div className="quick-actions">
      <div className="section-header">
        <h2>Quick Actions</h2>
      </div>

      <div className="quick-actions-grid">
        {actions.map((action, index) => (
          <button
            key={action.id || index}
            type="button"
            className="quick-action"
            onClick={action.onClick}
            disabled={action.disabled}
          >
            <span className="quick-action-icon">
              {action.icon || '＋'}
            </span>

            <span className="quick-action-label">
              {action.label}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}

export default QuickActions;