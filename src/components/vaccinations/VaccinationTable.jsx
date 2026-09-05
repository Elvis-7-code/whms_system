function VaccinationTable({ vaccinations = [] }) {
  return (
    <div className="table-container">
      <table className="data-table">
        <thead>
          <tr>
            <th>Animal</th>
            <th>Vaccine</th>
            <th>Date</th>
            <th>Next Due</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {vaccinations.map((vaccination) => (
            <tr key={vaccination.id}>
              <td>
                {vaccination.animalTag || 'N/A'}
              </td>

              <td>
                {vaccination.vaccineName || 'N/A'}
              </td>

              <td>
                {vaccination.date || 'N/A'}
              </td>

              <td>
                {vaccination.nextDueDate || 'N/A'}
              </td>

              <td>
                <span className="status">
                  {vaccination.status || 'Pending'}
                </span>
              </td>
            </tr>
          ))}

          {vaccinations.length === 0 && (
            <tr>
              <td colSpan="5">
                No vaccination records found.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default VaccinationTable;