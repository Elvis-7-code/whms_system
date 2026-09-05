function Loader({ label = 'Loading...' }) {
  return (
    <div className="loader-container" role="status" aria-live="polite">
      <div className="loader-spinner"></div>
      <p>{label}</p>
    </div>
  );
}

export default Loader;