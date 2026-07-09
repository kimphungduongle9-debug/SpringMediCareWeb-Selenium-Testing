import { Alert, Table } from "react-bootstrap";

const StatisticsTable = ({
  title,
  headers,
  data,
  emptyMessage,
  loading,
  renderRow,
  children,
  className = "",
}) => {
  return (
    <div className={`feature-card mt-4 ${className}`}>
      <h3>{title}</h3>

      {children}

      <Table bordered hover responsive>
        <thead>
          <tr>
            {headers.map((header, index) => (
              <th key={index}>{header}</th>
            ))}
          </tr>
        </thead>

        <tbody>
          {data.map((item, index) =>
            renderRow ? (
              renderRow(item, index)
            ) : (
              <tr key={index}>
                <td>{item[0]}</td>
                <td>{item[1]}</td>
              </tr>
            ),
          )}
        </tbody>
      </Table>

      {data.length === 0 && !loading && (
        <Alert variant="info">{emptyMessage}</Alert>
      )}
    </div>
  );
};

export default StatisticsTable;
