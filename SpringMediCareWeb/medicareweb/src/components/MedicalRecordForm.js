import { Button, Card, Form } from "react-bootstrap";

const MedicalRecordForm = ({
  title,
  diagnosis,
  treatment,
  setDiagnosis,
  setTreatment,
  onSubmit,
  saving = false,
  submitLabel,
  onCancel,
}) => {
  return (
    <Card className="shadow-sm border-0 mt-4">
      <Card.Header className="bg-info-subtle py-3">
        <h4 className="mb-0 text-primary">{title}</h4>
      </Card.Header>

      <Card.Body className="p-4">
        <Form onSubmit={onSubmit}>
          <Form.Group className="mb-4">
            <Form.Label className="fw-semibold">Chẩn đoán</Form.Label>

            <Form.Control
              as="textarea"
              rows={3}
              value={diagnosis}
              onChange={(e) => setDiagnosis(e.target.value)}
              placeholder="Nhập kết quả chẩn đoán"
            />
          </Form.Group>

          <Form.Group className="mb-4">
            <Form.Label className="fw-semibold">Hướng điều trị</Form.Label>

            <Form.Control
              as="textarea"
              rows={4}
              value={treatment}
              onChange={(e) => setTreatment(e.target.value)}
              placeholder="Nhập hướng điều trị"
            />
          </Form.Group>

          <Button variant="primary" type="submit" disabled={saving}>
            {saving ? "Đang lưu..." : submitLabel}
          </Button>

          {onCancel && (
            <Button
              variant="secondary"
              type="button"
              className="ms-2"
              onClick={onCancel}
              disabled={saving}
            >
              Hủy
            </Button>
          )}
        </Form>
      </Card.Body>
    </Card>
  );
};

export default MedicalRecordForm;
