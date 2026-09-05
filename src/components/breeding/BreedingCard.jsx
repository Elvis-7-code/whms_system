function BreedingCard({ breeding }) {
  if (!breeding) {
    return null;
  }

  return (
    <article className="breeding-card">
      <div className="breeding-card-header">
        <h3>
          {breeding.animalName ||
            breeding.animalTag ||
            'Breeding Record'}
        </h3>

        <span className="breeding-status">
          {breeding.status || 'Pending'}
        </span>
      </div>

      <div className="breeding-details">
        <p>
          <strong>Animal:</strong>{' '}
          {breeding.animalTag || 'N/A'}
        </p>

        <p>
          <strong>Bull:</strong>{' '}
          {breeding.bullTag || 'N/A'}
        </p>

        <p>
          <strong>Breeding Date:</strong>{' '}
          {breeding.breedingDate || 'N/A'}
        </p>

        <p>
          <strong>Expected Birth:</strong>{' '}
          {breeding.expectedBirthDate || 'N/A'}
        </p>
      </div>
    </article>
  );
}

export default BreedingCard;