import { Button, Card, Form } from "react-bootstrap";

const TestResultForm = ({
  testName,
  result,
  setTestName,
  setResult,
  onSubmit,
  saving,
}) => {
  return (
    <Card className="shadow-sm border-0 mt-4">
      <Card.Header className="bg-info-subtle py-3">
        <h4 className="mb-0 text-primary">Thêm kết quả xét nghiệm</h4>
      </Card.Header>

      <Card.Body className="p-4">
        <Form onSubmit={onSubmit}>
          <Form.Group className="mb-3">
            <Form.Label>Tên xét nghiệm</Form.Label>

            <Form.Control
              type="text"
              value={testName}
              onChange={(e) => setTestName(e.target.value)}
              placeholder="Ví dụ: Điện tâm đồ ECG"
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Kết quả</Form.Label>

            <Form.Control
              as="textarea"
              rows={4}
              value={result}
              onChange={(e) => setResult(e.target.value)}
              placeholder="Nhập nội dung kết quả xét nghiệm"
            />
          </Form.Group>

          <Button type="submit" variant="primary" disabled={saving}>
            {saving ? "Đang lưu..." : "Lưu kết quả"}
          </Button>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default TestResultForm;
