import { useEffect, useState } from "react";
import { Alert, Container } from "react-bootstrap";
import { Link, useNavigate, useParams } from "react-router-dom";
import DrugForm from "../../components/DrugForm";
import MySpinner from "../../components/MySpinner";
import { authApis, endpoints } from "../../configs/Apis";

const DrugEdit = () => {
  const { drugId } = useParams();
  const [drug, setDrug] = useState(null);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");
  const nav = useNavigate();

  const loadDrug = async () => {
    let res = await authApis().get(`${endpoints.drugs}/${drugId}`);
    setDrug(res.data);
  };

  const loadCategories = async () => {
    let res = await authApis().get(endpoints.categories);
    setCategories(Array.isArray(res.data) ? res.data : []);
  };

  const updateDrug = async (updatedDrug) => {
    setLoading(true);

    try {
      await authApis().put(`${endpoints.drugs}/${drugId}`, updatedDrug);
      nav("/admin-drugs");
    } catch (err) {
      console.error(err);
      setMsg("Không thể cập nhật thuốc.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setLoading(true);

    Promise.all([loadDrug(), loadCategories()])
      .catch((err) => {
        console.error(err);
        setMsg("Không thể tải thông tin thuốc.");
      })
      .finally(() => setLoading(false));
  }, [drugId]);

  return (
    <div className="main-content">
      <Container>
        <div className="section-box">
          <h2>Cập nhật thuốc</h2>
          <p>Chỉnh sửa thông tin thuốc trong kho dược phẩm.</p>
        </div>

        {msg && <Alert variant="danger">{msg}</Alert>}

        {drug && (
          <div className="feature-card">
            <DrugForm
              initialDrug={drug}
              categories={categories}
              loading={loading}
              submitLabel="Cập nhật thuốc"
              onSubmit={updateDrug}
            />

            <Link to="/admin-drugs" className="btn btn-secondary mt-3">
              Quay lại
            </Link>
          </div>
        )}

        {loading && <MySpinner />}
      </Container>
    </div>
  );
};

export default DrugEdit;
