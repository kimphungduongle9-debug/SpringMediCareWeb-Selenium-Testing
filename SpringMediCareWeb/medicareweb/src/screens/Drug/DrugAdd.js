import { useEffect, useState } from "react";
import { Alert, Container } from "react-bootstrap";
import { Link, useNavigate } from "react-router-dom";
import DrugForm from "../../components/DrugForm";
import MySpinner from "../../components/MySpinner";
import { authApis, endpoints } from "../../configs/Apis";

const DrugAdd = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");
  const nav = useNavigate();

  const loadCategories = async () => {
    let res = await authApis().get(endpoints.categories);
    setCategories(Array.isArray(res.data) ? res.data : []);
  };

  const addDrug = async (drug) => {
    setLoading(true);

    try {
      await authApis().post(endpoints.drugs, drug);
      nav("/admin-drugs");
    } catch (err) {
      console.error(err);
      setMsg("Không thể thêm thuốc.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setLoading(true);

    loadCategories()
      .catch((err) => {
        console.error(err);
        setMsg("Không thể tải danh mục thuốc.");
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="main-content">
      <Container>
        <div className="section-box">
          <h2>Thêm thuốc</h2>
          <p>Nhập thông tin thuốc mới vào kho dược phẩm.</p>
        </div>

        {msg && <Alert variant="danger">{msg}</Alert>}

        <div className="feature-card">
          <DrugForm
            categories={categories}
            loading={loading}
            submitLabel="Thêm thuốc"
            onSubmit={addDrug}
          />

          <Link to="/admin-drugs" className="btn btn-secondary mt-3">
            Quay lại
          </Link>
        </div>

        {loading && <MySpinner />}
      </Container>
    </div>
  );
};

export default DrugAdd;
