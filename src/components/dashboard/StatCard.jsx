function StatCard({
  title,
  value,
  icon,
  description,
  trend,
  trendType = 'neutral',
}) {
  return (
    <div className="stat-card">
      <div className="stat-card-header">
        <div>
          <p className="stat-card-title">
            {title}
          </p>

          <h2 className="stat-card-value">
            {value}
          </h2>
        </div>

        {icon && (
          <div className="stat-card-icon">
            {icon}
          </div>
        )}
      </div>

      {description && (
        <p className="stat-card-description">
          {description}
        </p>
      )}

      {trend && (
        <div className={`stat-card-trend trend-${trendType}`}>
          {trend}
        </div>
      )}
    </div>
  );
}

export default StatCard;