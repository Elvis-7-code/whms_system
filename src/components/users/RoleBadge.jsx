function RoleBadge({ role = 'worker' }) {
  const normalizedRole = role.toLowerCase();

  return (
    <span
      className={`role-badge role-${normalizedRole}`}
    >
      {role.charAt(0).toUpperCase() + role.slice(1)}
    </span>
  );
}

export default RoleBadge;