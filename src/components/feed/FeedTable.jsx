function FeedTable({ feeds = [] }) {
  return (
    <div className="table-container">
      <table className="data-table">
        <thead>
          <tr>
            <th>Feed</th>
            <th>Type</th>
            <th>Quantity</th>
            <th>Minimum Stock</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {feeds.map((feed) => (
            <tr key={feed.id}>
              <td>{feed.name || 'N/A'}</td>

              <td>{feed.type || 'N/A'}</td>

              <td>
                {feed.quantity ?? 0}{' '}
                {feed.unit || 'kg'}
              </td>

              <td>
                {feed.minimumStock ?? 0}{' '}
                {feed.unit || 'kg'}
              </td>

              <td>
                <span
                  className={`status status-${(
                    feed.status || 'available'
                  ).toLowerCase()}`}
                >
                  {feed.status || 'Available'}
                </span>
              </td>
            </tr>
          ))}

          {feeds.length === 0 && (
            <tr>
              <td colSpan="5">
                No feed records found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default FeedTable;