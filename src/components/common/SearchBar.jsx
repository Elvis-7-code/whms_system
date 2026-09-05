function SearchBar({
  value,
  onChange,
  placeholder = 'Search...',
}) {
  return (
    <div className="search-bar">
      <span className="search-icon">🔍</span>

      <input
        type="search"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        aria-label={placeholder}
      />
    </div>
  );
}

export default SearchBar;