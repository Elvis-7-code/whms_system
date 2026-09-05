function AnimalStatusBadge({ status = 'Active' }) {
  const normalizedStatus = status.toLowerCase();

  return (
    <span
      className={`animal-status-badge animal-status-${normalizedStatus}`}
    >
      {status}
    </span>
  );
}

export default AnimalStatusBadge;