import { Alert, Badge, Card, Table } from "react-bootstrap";

const PrescriptionList = ({ prescriptions }) => {
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
        <h4 className="mb-0 text-primary">Đơn thuốc</h4>
      </Card.Header>

      <Card.Body className="p-4">
        {prescriptions.length === 0 ? (
          <Alert variant="info" className="mb-0">
            Chưa có đơn thuốc.
          </Alert>
        ) : (
          prescriptions.map((prescription) => (
            <div
              key={prescription.prescriptionId}
              className="border rounded p-3 mb-3"
            >
              <div className="d-flex justify-content-between align-items-center mb-3">
                <div>
                  <strong>Đơn thuốc #{prescription.prescriptionId}</strong>

                  <div className="text-secondary small">
                    Ngày kê: {formatDateTime(prescription.createdDate)}
                  </div>
                </div>

                <Badge bg="primary">
                  {prescription.details?.length || 0} thuốc
                </Badge>
              </div>

              {prescription.details?.length > 0 ? (
                <Table striped bordered hover responsive className="mb-0">
                  <thead>
                    <tr>
                      <th>Thuốc</th>
                      <th>Số lượng</th>
                      <th>Đơn vị</th>
                      <th>Liều dùng</th>
                    </tr>
                  </thead>

                  <tbody>
                    {prescription.details.map((detail) => (
                      <tr key={detail.id}>
                        <td>{detail.drugId?.name}</td>
                        <td>{detail.quantity}</td>
                        <td>{detail.drugId?.unit}</td>
                        <td>{detail.dosage}</td>
                      </tr>
                    ))}
                  </tbody>
                </Table>
              ) : (
                <Alert variant="warning" className="mb-0">
                  Đơn thuốc chưa có chi tiết.
                </Alert>
              )}
            </div>
          ))
        )}
      </Card.Body>
    </Card>
  );
};

export default PrescriptionList;
