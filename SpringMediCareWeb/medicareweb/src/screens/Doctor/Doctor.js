import { useEffect, useState } from "react";
import MySpinner from "../../components/MySpinner";
import Apis, { endpoints } from "../../configs/Apis";
import { Alert } from "react-bootstrap";
import { useNavigate, useSearchParams } from "react-router-dom";

const Doctor = () => {
  const [doctors, setDoctors] = useState([]);
  const [allDoctors, setAllDoctors] = useState([]);
  const [loading, setLoading] = useState(false);
  const [kw, setKw] = useState("");
  const [q] = useSearchParams();
  const nav = useNavigate();

  const loadDoctors = async () => {
    try {
      setLoading(true);

      let res = await Apis.get(endpoints.allDoctors);

      setAllDoctors(res.data);
      setDoctors(res.data);
    } catch (ex) {
      console.error("Lỗi khi tải danh sách bác sĩ:", ex);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDoctors();
  }, []);

  useEffect(() => {
    const searchKw = q.get("kw") || "";
    setKw(searchKw);

    if (searchKw.trim() === "") {
      setDoctors(allDoctors);
    } else {
      setDoctors(
        allDoctors.filter((d) =>
          d.fullName.toLowerCase().includes(searchKw.trim().toLowerCase()),
        ),
      );
    }
  }, [q, allDoctors]);

  const handleBooking = (doctorId) => {
    nav(`/booking?doctorId=${doctorId}`);
  };

  const handleSearch = (e) => {
    e.preventDefault();
    if (kw.trim()) {
      nav(`/doctor?kw=${kw.trim()}`);
    } else {
      nav("/doctor");
    }
  };

  return (
    <div className="main-content">
      <div className="container">
        <div className="search-container-shared">
          <form onSubmit={handleSearch} className="search-form-shared">
            <input
              type="text"
              className="search-input-shared"
              placeholder="Nhập tên bác sĩ cần tìm..."
              value={kw}
              onChange={(e) => setKw(e.target.value)}
            />
            <button type="submit" className="btn-main-shared">
              Tìm kiếm
            </button>
          </form>
        </div>

        <div className="section-box">
          <h2>Danh sách bác sĩ</h2>
          <p style={{ color: "red", fontWeight: "bold", marginBottom: "14px" }}>
            Số lượng bác sĩ: <span>{doctors.length}</span>
          </p>
        </div>

        {doctors.length === 0 && !loading && (
          <Alert variant="info" className="mt-2">
            KHÔNG có kết quả phù hợp!
          </Alert>
        )}

        <div className="feature-grid">
          {doctors.map((d) => (
            <div
              className="feature-card"
              key={d.doctorId}
              style={{ display: "flex", flexDirection: "column" }}
            >
              <img
                className="doctor-img"
                src={d.image || "https://via.placeholder.com/150"}
                alt={d.fullName}
              />

              <h3 className="card-title-shared">{d.fullName}</h3>

              <p className="card-text-shared">
                <strong>Chuyên khoa:</strong>{" "}
                <span className="card-value-highlight">
                  {d.specialtyId?.name || "Chưa rõ"}
                </span>
              </p>

              <p className="card-text-shared" style={{ marginBottom: "20px" }}>
                <strong>Kinh nghiệm:</strong>{" "}
                <span className="card-value-highlight">
                  {d.experienceYears} năm
                </span>
              </p>

              <div className="card-actions-shared">
                <button
                  onClick={() => handleBooking(d.doctorId)}
                  className="btn-action-shared"
                >
                  Đặt lịch hẹn
                </button>
              </div>
            </div>
          ))}
        </div>

        {loading && <MySpinner />}
      </div>
    </div>
  );
};

export default Doctor;
