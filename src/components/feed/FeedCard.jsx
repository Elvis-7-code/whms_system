function FeedCard({ feed }) {
  if (!feed) {
    return null;
  }

  return (
    <article className="feed-card">
      <div className="feed-card-header">
        <h3>{feed.name || 'Feed Item'}</h3>

        <span className="feed-quantity">
          {feed.quantity ?? 0} {feed.unit || 'kg'}
        </span>
      </div>

      <div className="feed-card-content">
        <p>
          <strong>Type:</strong>{' '}
          {feed.type || 'N/A'}
        </p>

        <p>
          <strong>Minimum Stock:</strong>{' '}
          {feed.minimumStock ?? 0}{' '}
          {feed.unit || 'kg'}
        </p>

        <p>
          <strong>Status:</strong>{' '}
          {feed.status || 'Available'}
        </p>
      </div>
    </article>
  );
}

export default FeedCard;