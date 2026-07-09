import { Badge, Button, Card, Col, Image, Row } from "react-bootstrap";

const MedicalRecordDetail = ({ medicalRecord, onEdit, showEdit = false }) => {
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
    <Card className="shadow-sm border-0">
      <Card.Header className="bg-info-subtle py-3">
        <div className="d-flex justify-content-between align-items-center">
          <h4 className="mb-0 text-primary">Thông tin khám bệnh</h4>

          <div className="d-flex align-items-center gap-2">
            <Badge bg="primary">Hồ sơ #{medicalRecord.recordId}</Badge>

            {showEdit && (
              <Button variant="outline-primary" size="sm" onClick={onEdit}>
                Cập nhật hồ sơ
              </Button>
            )}
          </div>
        </div>
      </Card.Header>

      <Card.Body className="p-4">
        <Row className="g-4 align-items-stretch">
          <Col md={3}>
            <div className="border rounded p-3 h-100 text-center fs-5">
              <Image
                src={medicalRecord.patientId?.image}
                roundedCircle
                width={140}
                height={140}
                className="object-fit-cover mb-3"
              />

              <h5 className="mb-1">{medicalRecord.patientId?.fullName}</h5>

              <p className="text-secondary mb-0">Bệnh nhân</p>
            </div>
          </Col>

          <Col md={4}>
            <div className="border rounded p-4 h-100 fs-5">
              <h5 className="text-primary mb-4">Thông tin chung</h5>

              <p className="mb-3">
                <strong>Bác sĩ phụ trách:</strong>
                <br />
                {medicalRecord.doctorId?.fullName}
              </p>

              <p className="mb-0">
                <strong>Ngày tạo:</strong>
                <br />
                {formatDateTime(medicalRecord.createdDate)}
              </p>
            </div>
          </Col>

          <Col md={5}>
            <div className="border rounded p-4 h-100 fs-5">
              <h5 className="text-primary mb-4">Kết quả thăm khám</h5>

              <p className="mb-3">
                <strong>Chẩn đoán:</strong>
                <br />
                {medicalRecord.diagnosis}
              </p>

              <p className="mb-0">
                <strong>Hướng điều trị:</strong>
                <br />
                {medicalRecord.treatment}
              </p>
            </div>
          </Col>
        </Row>
      </Card.Body>
    </Card>
  );
};

export default MedicalRecordDetail;
