import { Button, Card, Form, Table } from "react-bootstrap";
import { useState } from "react";

const PrescriptionForm = ({ drugs, items, setItems, onSubmit, saving }) => {
  const [drugId, setDrugId] = useState("");
  const [quantity, setQuantity] = useState(1);
  const [dosage, setDosage] = useState("");

  const addItem = () => {
    const drug = drugs.find((d) => d.drugId === Number(drugId));

    if (!drug || Number(quantity) <= 0 || !dosage.trim()) {
      return;
    }

    setItems([
      ...items,
      {
        id: drug.drugId,
        name: drug.name,
        quantity: Number(quantity),
        dosage,
      },
    ]);

    setDrugId("");
    setQuantity(1);
    setDosage("");
  };

  const removeItem = (index) => {
    setItems(items.filter((_, i) => i !== index));
  };

  return (
    <Card className="shadow-sm border-0 mt-4">
      <Card.Header className="bg-info-subtle py-3">
        <h4 className="mb-0 text-primary">Kê đơn thuốc</h4>
      </Card.Header>

      <Card.Body className="p-4">
        <Form>
          <Form.Group className="mb-3">
            <Form.Label>Thuốc</Form.Label>

            <Form.Select
              value={drugId}
              onChange={(e) => setDrugId(e.target.value)}
            >
              <option value="">-- Chọn thuốc --</option>

              {drugs.map((drug) => (
                <option key={drug.drugId} value={drug.drugId}>
                  {drug.name} - tồn kho: {drug.quantity} {drug.unit}
                </option>
              ))}
            </Form.Select>
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Số lượng</Form.Label>

            <Form.Control
              type="number"
              min="1"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
            />
          </Form.Group>

          <Form.Group className="mb-3">
            <Form.Label>Liều dùng</Form.Label>

            <Form.Control
              type="text"
              value={dosage}
              onChange={(e) => setDosage(e.target.value)}
              placeholder="Ví dụ: Ngày uống 2 lần, mỗi lần 1 viên sau ăn"
            />
          </Form.Group>

          <Button type="button" variant="outline-primary" onClick={addItem}>
            Thêm vào đơn
          </Button>
        </Form>

        {items.length > 0 && (
          <Table striped bordered hover responsive className="mt-4">
            <thead>
              <tr>
                <th>Thuốc</th>
                <th>Số lượng</th>
                <th>Liều dùng</th>
                <th>Thao tác</th>
              </tr>
            </thead>

            <tbody>
              {items.map((item, index) => (
                <tr key={`${item.id}-${index}`}>
                  <td>{item.name}</td>
                  <td>{item.quantity}</td>
                  <td>{item.dosage}</td>
                  <td>
                    <Button
                      type="button"
                      variant="danger"
                      size="sm"
                      onClick={() => removeItem(index)}
                    >
                      Xóa
                    </Button>
                  </td>
                </tr>
              ))}
            </tbody>
          </Table>
        )}

        <Button
          type="button"
          variant="primary"
          className="mt-3"
          disabled={saving || items.length === 0}
          onClick={onSubmit}
        >
          {saving ? "Đang lưu..." : "Lưu đơn thuốc"}
        </Button>
      </Card.Body>
    </Card>
  );
};

export default PrescriptionForm;
