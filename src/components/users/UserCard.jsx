function UserCard({ user }) {
  if (!user) {
    return null;
  }

  const initials = user.name
    ? user.name
        .split(' ')
        .map((name) => name.charAt(0))
        .join('')
        .slice(0, 2)
        .toUpperCase()
    : 'U';

  return (
    <article className="user-card">
      <div className="user-card-avatar">
        {user.avatar ? (
          <img
            src={user.avatar}
            alt={user.name}
          />
        ) : (
          initials
        )}
      </div>

      <div className="user-card-content">
        <h3>{user.name || 'Unknown User'}</h3>

        <p>
          {user.email || 'No email provided'}
        </p>

        <span className="user-role">
          {user.role || 'Worker'}
        </span>
      </div>
    </article>
  );
}

export default UserCard;