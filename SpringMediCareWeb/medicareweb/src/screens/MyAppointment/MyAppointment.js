import { useContext, useEffect, useState } from "react";
import { Alert } from "react-bootstrap";
import Apis, { endpoints } from "../../configs/Apis";
import MySpinner from "../../components/MySpinner";
import { MyUserContext } from "../../configs/Contexts";
import AppointmentTable from "../../components/AppointmentTable";
const MyAppointment = () => {
  const [user] = useContext(MyUserContext);
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const isPatient = user !== null && user.role === "patient";

  const loadAppointments = async () => {
    let patientId = user.patientId || user.id || user.userId;

    let res = await Apis.get(`/appointments/patient/${patientId}`);
    setAppointments(res.data);
  };

  useEffect(() => {
    if (user !== null && isPatient) {
      setLoading(true);

      loadAppointments()
        .catch((err) => {
          console.error(err);
          setMsg("Không tải được danh sách lịch hẹn.");
        })
        .finally(() => setLoading(false));
    }
  }, [user]);

  if (user === null) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="warning">Vui lòng đăng nhập để xem lịch hẹn.</Alert>
        </div>
      </div>
    );
  }

  if (!isPatient) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="danger">
            Chỉ tài khoản bệnh nhân mới được xem trang này.
          </Alert>
        </div>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="container">
        <div className="section-box">
          <h2>Lịch hẹn của tôi</h2>
          <p>Danh sách các lịch hẹn khám bệnh bạn đã đặt.</p>
        </div>

        {msg && <Alert variant="info">{msg}</Alert>}

        <div className="feature-card">
          <AppointmentTable appointments={appointments} showDoctor={true} />

          {appointments.length === 0 && !loading && (
            <Alert variant="info">Bạn chưa có lịch hẹn nào.</Alert>
          )}
        </div>

        {loading && <MySpinner />}
      </div>
    </div>
  );
};

export default MyAppointment;
