function AlertCard({ alert, onDismiss }) {
  if (!alert) {
    return null;
  }

  const severity = (
    alert.severity || 'info'
  ).toLowerCase();

  return (
    <article
      className={`alert-card alert-${severity}`}
    >
      <div className="alert-card-icon">
        {severity === 'critical' && '🚨'}
        {severity === 'warning' && '⚠️'}
        {severity === 'info' && 'ℹ️'}
        {severity === 'success' && '✅'}
      </div>

      <div className="alert-card-content">
        <div className="alert-card-header">
          <h3>
            {alert.title || 'Alert'}
          </h3>

          {alert.createdAt && (
            <small>
              {alert.createdAt}
            </small>
          )}
        </div>

        <p>
          {alert.message || 'No alert message.'}
        </p>
      </div>

      {onDismiss && (
        <button
          type="button"
          className="alert-dismiss"
          onClick={() => onDismiss(alert)}
          aria-label="Dismiss alert"
        >
          ×
        </button>
      )}
    </article>
  );
}

export default AlertCard;