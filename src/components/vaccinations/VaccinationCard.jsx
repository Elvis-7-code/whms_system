function VaccinationCard({ vaccination }) {
  if (!vaccination) {
    return null;
  }

  return (
    <article className="vaccination-card">
      <div className="vaccination-card-header">
        <h3>
          {vaccination.vaccineName ||
            'Vaccination'}
        </h3>

        <span className="vaccination-status">
          {vaccination.status || 'Pending'}
        </span>
      </div>

      <div className="vaccination-details">
        <p>
          <strong>Animal:</strong>{' '}
          {vaccination.animalTag || 'N/A'}
        </p>

        <p>
          <strong>Date:</strong>{' '}
          {vaccination.date || 'N/A'}
        </p>

        <p>
          <strong>Next Due:</strong>{' '}
          {vaccination.nextDueDate || 'N/A'}
        </p>

        {vaccination.notes && (
          <p>
            <strong>Notes:</strong>{' '}
            {vaccination.notes}
          </p>
        )}
      </div>
    </article>
  );
}

export default VaccinationCard;