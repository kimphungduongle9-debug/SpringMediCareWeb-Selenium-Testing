import { useEffect, useState } from "react";
import { Alert, Badge, Button, Container, Form, Table } from "react-bootstrap";
import { Link } from "react-router-dom";
import MySpinner from "../../components/MySpinner";
import { authApis, endpoints } from "../../configs/Apis";

const Drug = () => {
    const [drugs, setDrugs] = useState([]);
    const [categories, setCategories] = useState([]);
    const [loading, setLoading] = useState(false);
    const [msg, setMsg] = useState("");
    const [kw, setKw] = useState("");
    const [selectedCat, setSelectedCat] = useState(null);

    const loadCategories = async () => {
        try {
            const res = await authApis().get(endpoints.categories);
            setCategories(Array.isArray(res.data) ? res.data : res.data?.data || []);
        } catch (err) {
            console.error(err);
        }
    };

    const loadDrugs = async (keyword = "", categoryId = null) => {
        try {
            setLoading(true);

            let url = endpoints.drugs;
            let params = [];

            if (keyword) params.push(`kw=${encodeURIComponent(keyword)}`);
            if (categoryId) params.push(`categoryId=${categoryId}`);

            if (params.length > 0)
                url += `?${params.join("&")}`;

            const res = await authApis().get(url);
            setDrugs(Array.isArray(res.data) ? res.data : []);
        } catch (err) {
            console.error(err);
            setMsg("Không thể tải danh sách thuốc.");
        } finally {
            setLoading(false);
        }
    };

    const deleteDrug = async (id) => {
        if (!window.confirm("Bạn chắc chắn muốn xóa thuốc này?"))
            return;

        try {
            await authApis().delete(`${endpoints.drugs}/${id}`);
            setMsg("Xóa thuốc thành công.");
            loadDrugs(kw, selectedCat);
        } catch (err) {
            console.error(err);
            setMsg("Không thể xóa thuốc.");
        }
    };

    const handleSearch = (e) => {
        e.preventDefault();
        loadDrugs(kw, selectedCat);
    };

    const getExpiryStatus = (expiryDate) => {
        const today = new Date();
        const expiry = new Date(expiryDate);
        const diffDays = (expiry - today) / (1000 * 60 * 60 * 24);

        if (diffDays < 0)
            return { text: "Hết hạn", bg: "danger" };

        if (diffDays <= 90)
            return { text: "Sắp hết hạn", bg: "warning" };

        return { text: "Còn hạn", bg: "success" };
    };

    useEffect(() => {
        loadCategories();
        loadDrugs();
    }, []);

    useEffect(() => {
        loadDrugs(kw, selectedCat);
    }, [selectedCat]);

    return (
        <div className="main-content">
            <Container>
                <div className="section-box">
                    <div className="d-flex justify-content-between align-items-center">
                        <div>
                            <h2>Quản lý kho dược phẩm</h2>
                            <p className="mb-0">Danh sách thuốc trong hệ thống</p>
                        </div>

                        <Link to="/drugs/add" className="btn btn-success">
                            + Thêm thuốc
                        </Link>
                    </div>
                </div>

                {msg && <Alert variant="info">{msg}</Alert>}

                <div className="mb-3">
                    <Button
                        variant={selectedCat === null ? "primary" : "outline-primary"}
                        className="me-2 mb-2"
                        onClick={() => setSelectedCat(null)}
                    >
                        Tất cả
                    </Button>

                    {categories.map((c) => (
                        <Button
                            key={c.categoryId}
                            variant={selectedCat === c.categoryId ? "primary" : "outline-primary"}
                            className="me-2 mb-2"
                            onClick={() => setSelectedCat(c.categoryId)}
                        >
                            {c.categoryName}
                        </Button>
                    ))}
                </div>

                <Form onSubmit={handleSearch} className="d-flex mb-4">
                    <Form.Control
                        placeholder="Nhập tên thuốc..."
                        value={kw}
                        onChange={(e) => setKw(e.target.value)}
                        className="me-2"
                    />

                    <Button type="submit" variant="primary">
                        Tìm kiếm
                    </Button>
                </Form>

                <div className="feature-card p-3">
                    {drugs.length === 0 && !loading ? (
                        <Alert variant="warning" className="text-center">
                            {kw
                                ? `Không tìm thấy thuốc với từ khóa "${kw}"`
                                : "Không có thuốc trong danh mục này"}
                        </Alert>
                    ) : (
                        <Table striped hover responsive>
                            <thead>
                                <tr>
                                    <th>STT</th>
                                    <th>Ảnh</th>
                                    <th>Tên thuốc</th>
                                    <th>Danh mục</th>
                                    <th>Giá</th>
                                    <th>Tồn kho</th>
                                    <th>NSX</th>
                                    <th>HSD</th>
                                    <th>Trạng thái</th>
                                    <th>Thao tác</th>
                                </tr>
                            </thead>

                            <tbody>
                                {drugs.map((d, index) => {
                                    const expiry = getExpiryStatus(d.expiryDate);

                                    return (
                                        <tr key={d.drugId}>
                                            <td>{index+1}</td>
                                            <td>
                                                <img
                                                    src={d.image}
                                                    alt={d.name}
                                                    width={70}
                                                    height={70}
                                                    style={{ objectFit: "cover", borderRadius: 8 }}
                                                />
                                            </td>

                                            <td>
                                                <strong>{d.name}</strong>
                                                <div className="text-muted small">
                                                    {d.dosageForm}
                                                </div>
                                            </td>

                                            <td>{d.categoryId?.categoryName}</td>

                                            <td>
                                                {Number(d.price).toLocaleString("vi-VN")}đ
                                            </td>

                                            <td>
                                                {d.quantity <= d.minQuantity ? (
                                                    <Badge bg="danger">
                                                        Sắp hết hàng ({d.quantity})
                                                    </Badge>
                                                ) : (
                                                    <Badge bg="success">
                                                        {d.quantity}
                                                    </Badge>
                                                )}
                                            </td>

                                            <td>
                                                {new Date(d.productionDate).toLocaleDateString("vi-VN")}
                                            </td>

                                            <td>
                                                {new Date(d.expiryDate).toLocaleDateString("vi-VN")}
                                            </td>

                                            <td>
                                                <Badge bg={expiry.bg}>
                                                    {expiry.text}
                                                </Badge>
                                            </td>

                                            <td>
                                                <Link
                                                    to={`/drugs/edit/${d.drugId}`}
                                                    className="btn btn-warning btn-sm me-2"
                                                >
                                                    Sửa
                                                </Link>

                                                <button
                                                    className="btn btn-danger btn-sm"
                                                    onClick={() => deleteDrug(d.drugId)}
                                                >
                                                    Xóa
                                                </button>
                                            </td>
                                        </tr>
                                    );
                                })}
                            </tbody>
                        </Table>
                    )}
                </div>

                {loading && <MySpinner />}
            </Container>
        </div>
    );
};

export default Drug;