function BreedingTable({ records = [] }) {
  return (
    <div className="table-container">
      <table className="data-table">
        <thead>
          <tr>
            <th>Animal</th>
            <th>Bull</th>
            <th>Breeding Date</th>
            <th>Expected Birth</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {records.map((record) => (
            <tr key={record.id}>
              <td>
                {record.animalTag ||
                  record.animalName ||
                  'N/A'}
              </td>

              <td>
                {record.bullTag || 'N/A'}
              </td>

              <td>
                {record.breedingDate || 'N/A'}
              </td>

              <td>
                {record.expectedBirthDate || 'N/A'}
              </td>

              <td>
                <span className="status">
                  {record.status || 'Pending'}
                </span>
              </td>
            </tr>
          ))}

          {records.length === 0 && (
            <tr>
              <td colSpan="5">
                No breeding records found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default BreedingTable;