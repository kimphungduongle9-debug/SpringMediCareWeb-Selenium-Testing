import { useContext, useEffect, useState } from "react";
import { Alert } from "react-bootstrap";
import { MyUserContext } from "../../configs/Contexts";
import { authApis, endpoints } from "../../configs/Apis";
import MySpinner from "../../components/MySpinner";
import DoctorScheduleTable from "../../components/DoctorScheduleTable";

const DoctorWorkSchedule = () => {
  const [user] = useContext(MyUserContext);
  const [doctor, setDoctor] = useState(null);
  const [schedules, setSchedules] = useState([]);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const isDoctor = user !== null && user.role === "doctor";

  const loadDoctor = async () => {
    let res = await authApis().get(endpoints.doctorByUser(user.id));
    setDoctor(res.data);
    return res.data;
  };

  const loadSchedules = async () => {
    let d = await loadDoctor();

    let res = await authApis().get(
      endpoints.doctorSchedulesByDoctor(d.doctorId),
    );

    setSchedules(res.data);
  };

  useEffect(() => {
    if (user !== null && isDoctor) {
      setLoading(true);

      loadSchedules()
        .catch((err) => {
          console.error(err);
          setMsg("Không tải được lịch làm việc.");
        })
        .finally(() => setLoading(false));
    }
  }, [user]);

  if (user === null) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="warning">
            Vui lòng đăng nhập để xem lịch làm việc.
          </Alert>
        </div>
      </div>
    );
  }

  if (!isDoctor) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="danger">
            Chỉ tài khoản bác sĩ mới được xem trang này.
          </Alert>
        </div>
      </div>
    );
  }

  return (
    <div className="main-content" style={{ paddingTop: "60px" }}>
      <div className="container">
        <div className="section-box">
          <h2>Lịch làm việc của tôi</h2>

          {doctor && (
            <p>
              Bác sĩ: <strong>{doctor.fullName}</strong> - Chuyên khoa:{" "}
              <strong>{doctor.specialtyId?.name}</strong>
            </p>
          )}
        </div>

        {msg && <Alert variant="info">{msg}</Alert>}

        <div className="feature-card">
          <DoctorScheduleTable schedules={schedules} showActions={false} />

          {schedules.length === 0 && !loading && (
            <Alert variant="info">Chưa có lịch làm việc.</Alert>
          )}
        </div>

        {loading && <MySpinner />}
      </div>
    </div>
  );
};

export default DoctorWorkSchedule;
