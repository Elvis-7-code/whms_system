function FeedStatusBadge({ status = 'Available' }) {
  const normalizedStatus = status.toLowerCase();

  return (
    <span
      className={`feed-status-badge feed-status-${normalizedStatus}`}
    >
      {status}
    </span>
  );
}

export default FeedStatusBadge;