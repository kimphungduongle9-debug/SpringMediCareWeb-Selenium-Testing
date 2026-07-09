import { Alert, Card, Table } from "react-bootstrap";

const TestResultList = ({ testResults }) => {
  const formatDateTime = (value) => {
    if (!value) return "";

    return new Date(value).toLocaleString("vi-VN", {
      hour: "2-digit",
      minute: "2-digit",
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };

  return (
    <Card className="shadow-sm border-0 mt-4">
      <Card.Header className="bg-info-subtle py-3">
        <h4 className="mb-0 text-primary">Kết quả xét nghiệm</h4>
      </Card.Header>

      <Card.Body className="p-4">
        {testResults.length === 0 ? (
          <Alert variant="info" className="mb-0">
            Chưa có kết quả xét nghiệm.
          </Alert>
        ) : (
          <Table striped bordered hover responsive className="mb-0">
            <thead>
              <tr>
                <th>ID</th>
                <th>Tên xét nghiệm</th>
                <th>Kết quả</th>
                <th>Ngày tạo</th>
              </tr>
            </thead>

            <tbody>
              {testResults.map((testResult) => (
                <tr key={testResult.testId}>
                  <td>{testResult.testId}</td>
                  <td>{testResult.testName}</td>
                  <td>{testResult.result}</td>
                  <td>{formatDateTime(testResult.createdDate)}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        )}
      </Card.Body>
    </Card>
  );
};

export default TestResultList;
