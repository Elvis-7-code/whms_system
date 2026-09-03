function ReportCard({
  title,
  value,
  description,
  icon,
}) {
  return (
    <article className="report-card">
      {icon && (
        <div className="report-card-icon">
          {icon}
        </div>
      )}

      <div className="report-card-content">
        <h3>{title}</h3>

        <strong>{value}</strong>

        {description && (
          <p>{description}</p>
        )}
      </div>
    </article>
  );
}

export default ReportCard;