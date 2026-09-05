import { Link } from 'react-router-dom';

function AnimalTable({ animals = [] }) {
  return (
    <div className="table-container">
      <table className="data-table">
        <thead>
          <tr>
            <th>Tag ID</th>
            <th>Name</th>
            <th>Species</th>
            <th>Breed</th>
            <th>Gender</th>
            <th>Status</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          {animals.map((animal) => (
            <tr key={animal.id}>
              <td>{animal.tagId || 'N/A'}</td>

              <td>{animal.name || 'Unnamed'}</td>

              <td>{animal.species || 'N/A'}</td>

              <td>{animal.breed || 'N/A'}</td>

              <td>{animal.gender || 'N/A'}</td>

              <td>
                <span
                  className={`status status-${(
                    animal.status || 'active'
                  ).toLowerCase()}`}
                >
                  {animal.status || 'Active'}
                </span>
              </td>

              <td>
                <Link
                  to={`/animals/${animal.id}`}
                  className="table-action"
                >
                  View
                </Link>
              </td>
            </tr>
          ))}

          {animals.length === 0 && (
            <tr>
              <td colSpan="7">
                No animals recorded.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default AnimalTable;