function ReportTable({
  columns = [],
  data = [],
}) {
  return (
    <div className="table-container">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.key}>
                {column.label}
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {data.map((row, index) => (
            <tr key={row.id || index}>
              {columns.map((column) => (
                <td key={column.key}>
                  {column.render
                    ? column.render(row)
                    : row[column.key] ?? 'N/A'}
                </td>
              ))}
            </tr>
          ))}

          {data.length === 0 && (
            <tr>
              <td colSpan={columns.length || 1}>
                No report data available.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default ReportTable;