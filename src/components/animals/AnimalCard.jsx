import { Link } from 'react-router-dom';

function AnimalCard({ animal }) {
  if (!animal) {
    return null;
  }

  return (
    <article className="animal-card">
      <div className="animal-card-image">
        {animal.image ? (
          <img
            src={animal.image}
            alt={animal.name || animal.tagId}
          />
        ) : (
          <span>🐄</span>
        )}
      </div>

      <div className="animal-card-content">
        <div className="animal-card-header">
          <h3>
            {animal.name || 'Unnamed Animal'}
          </h3>

          <span className="animal-tag">
            {animal.tagId || 'No Tag'}
          </span>
        </div>

        <div className="animal-details">
          <p>
            <strong>Species:</strong>{' '}
            {animal.species || 'N/A'}
          </p>

          <p>
            <strong>Breed:</strong>{' '}
            {animal.breed || 'N/A'}
          </p>

          <p>
            <strong>Gender:</strong>{' '}
            {animal.gender || 'N/A'}
          </p>

          <p>
            <strong>Status:</strong>{' '}
            {animal.status || 'Active'}
          </p>
        </div>

        {animal.id && (
          <Link
            to={`/animals/${animal.id}`}
            className="card-link"
          >
            View Details
          </Link>
        )}
      </div>
    </article>
  );
}

export default AnimalCard;