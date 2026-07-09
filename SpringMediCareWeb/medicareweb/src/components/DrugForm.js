import { useEffect, useState } from "react";
import { Button, Form } from "react-bootstrap";

const DrugForm = ({
  initialDrug,
  categories,
  loading,
  submitLabel,
  onSubmit,
}) => {
  const [drug, setDrug] = useState({
    categoryId: "",
    name: "",
    description: "",
    price: "",
    quantity: "",
    minQuantity: "",
    productionDate: "",
    expiryDate: "",
    dosageForm: "",
    unit: "",
    strength: "",
    manufacturer: "",
    status: "available",
    image: "",
  });

  const formatDateInput = (date) => {
    if (!date) return "";

    const value = new Date(date);
    const year = value.getFullYear();
    const month = String(value.getMonth() + 1).padStart(2, "0");
    const day = String(value.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
  };

  useEffect(() => {
    if (initialDrug) {
      setDrug({
        categoryId: initialDrug.categoryId?.categoryId || "",
        name: initialDrug.name || "",
        description: initialDrug.description || "",
        price: initialDrug.price || "",
        quantity: initialDrug.quantity ?? "",
        minQuantity: initialDrug.minQuantity ?? "",
        productionDate: formatDateInput(initialDrug.productionDate),
        expiryDate: formatDateInput(initialDrug.expiryDate),
        dosageForm: initialDrug.dosageForm || "",
        unit: initialDrug.unit || "",
        strength: initialDrug.strength || "",
        manufacturer: initialDrug.manufacturer || "",
        status: initialDrug.status || "available",
        image: initialDrug.image || "",
      });
    }
  }, [initialDrug]);

  const change = (event) => {
    setDrug({
      ...drug,
      [event.target.name]: event.target.value,
    });
  };

  const submit = (event) => {
    event.preventDefault();

    onSubmit({
      ...drug,
      categoryId: {
        categoryId: Number(drug.categoryId),
      },
      price: Number(drug.price),
      quantity: Number(drug.quantity),
      minQuantity: Number(drug.minQuantity),
    });
  };

  return (
    <Form onSubmit={submit}>
      <Form.Group className="mb-3">
        <Form.Label>Danh mục thuốc</Form.Label>
        <Form.Select
          name="categoryId"
          value={drug.categoryId}
          onChange={change}
          required
        >
          <option value="">Chọn danh mục thuốc</option>

          {categories.map((category) => (
            <option key={category.categoryId} value={category.categoryId}>
              {category.categoryName}
            </option>
          ))}
        </Form.Select>
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Tên thuốc</Form.Label>
        <Form.Control
          name="name"
          value={drug.name}
          onChange={change}
          required
        />
      </Form.Group>

      <Form.Group className="mb-3">
        <Form.Label>Mô tả</Form.Label>
        <Form.Control
          as="textarea"
          rows={3}
          name="description"
          value={drug.description}
          onChange={change}
        />
      </Form.Group>

      <div className="row">
        <div className="col-md-4">
          <Form.Group className="mb-3">
            <Form.Label>Giá</Form.Label>
            <Form.Control
              type="number"
              name="price"
              value={drug.price}
              onChange={change}
              min="0"
              required
            />
          </Form.Group>
        </div>

        <div className="col-md-4">
          <Form.Group className="mb-3">
            <Form.Label>Số lượng tồn kho</Form.Label>
            <Form.Control
              type="number"
              name="quantity"
              value={drug.quantity}
              onChange={change}
              min="0"
              required
            />
          </Form.Group>
        </div>

        <div className="col-md-4">
          <Form.Group className="mb-3">
            <Form.Label>Số lượng tối thiểu</Form.Label>
            <Form.Control
              type="number"
              name="minQuantity"
              value={drug.minQuantity}
              onChange={change}
              min="0"
              required
            />
          </Form.Group>
        </div>
      </div>

      <div className="row">
        <div className="col-md-6">
          <Form.Group className="mb-3">
            <Form.Label>Ngày sản xuất</Form.Label>
            <Form.Control
              type="date"
              name="productionDate"
              value={drug.productionDate}
              onChange={change}
              required
            />
          </Form.Group>
        </div>

        <div className="col-md-6">
          <Form.Group className="mb-3">
            <Form.Label>Hạn sử dụng</Form.Label>
            <Form.Control
              type="date"
              name="expiryDate"
              value={drug.expiryDate}
              onChange={change}
              required
            />
          </Form.Group>
        </div>
      </div>

      <div className="row">
        <div className="col-md-4">
          <Form.Group className="mb-3">
            <Form.Label>Dạng bào chế</Form.Label>
            <Form.Control
              name="dosageForm"
              value={drug.dosageForm}
              onChange={change}
            />
          </Form.Group>
        </div>

        <div className="col-md-4">
          <Form.Group className="mb-3">
            <Form.Label>Đơn vị</Form.Label>
            <Form.Control name="unit" value={drug.unit} onChange={change} />
          </Form.Group>
        </div>

        <div className="col-md-4">
          <Form.Group className="mb-3">
            <Form.Label>Hàm lượng</Form.Label>
            <Form.Control
              name="strength"
              value={drug.strength}
              onChange={change}
            />
          </Form.Group>
        </div>
      </div>

      <Form.Group className="mb-3">
        <Form.Label>Nhà sản xuất</Form.Label>
        <Form.Control
          name="manufacturer"
          value={drug.manufacturer}
          onChange={change}
        />
      </Form.Group>

      <Form.Select name="status" value={drug.status} onChange={change} required>
        <option value="available">Còn hàng</option>
        <option value="low_stock">Sắp hết hàng</option>
        <option value="expired">Hết hạn</option>
        <option value="inactive">Ngừng kinh doanh</option>
      </Form.Select>

      <Form.Group className="mb-3">
        <Form.Label>URL ảnh thuốc</Form.Label>
        <Form.Control
          type="text"
          name="image"
          value={drug.image}
          onChange={change}
          placeholder="Dán đường link ảnh vào đây"
        />
      </Form.Group>

      <Button type="submit" variant="primary" disabled={loading}>
        {submitLabel}
      </Button>
    </Form>
  );
};

export default DrugForm;
