import { useContext, useEffect, useState } from "react";
import { Alert } from "react-bootstrap";
import { MyUserContext } from "../../configs/Contexts";
import { authApis, endpoints } from "../../configs/Apis";
import MySpinner from "../../components/MySpinner";
import AppointmentTable from "../../components/AppointmentTable";
import { useNavigate } from "react-router-dom";

const DoctorAppointment = () => {
  const [user] = useContext(MyUserContext);
  const [doctor, setDoctor] = useState(null);
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");
  const nav = useNavigate();

  const isDoctor = user !== null && user.role === "doctor";

  const loadDoctor = async () => {
    let res = await authApis().get(endpoints.doctorByUser(user.id));
    setDoctor(res.data);
    return res.data;
  };

  const loadAppointments = async () => {
    let d = await loadDoctor();
    let res = await authApis().get(endpoints.appointmentsByDoctor(d.doctorId));
    setAppointments(res.data);
  };
  const viewMedicalRecords = (appointment) => {
    nav(`/doctor-medical-record?appointmentId=${appointment.appointmentId}`);
  };
  const examine = (appointment) => {
    nav(`/doctor-examination?appointmentId=${appointment.appointmentId}`);
  };
  useEffect(() => {
    if (user !== null && isDoctor) {
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
      <div className="main-content" style={{ paddingTop: "40px" }}>
        <div className="container">
          <Alert variant="warning">
            Vui lòng đăng nhập để xem lịch hẹn bệnh nhân.
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
    <div className="main-content">
      <div className="container">
        <div className="section-box">
          <h2>Lịch hẹn bệnh nhân</h2>

          {doctor && (
            <p>
              Bác sĩ: <strong>{doctor.fullName}</strong> - Chuyên khoa:{" "}
              <strong>{doctor.specialtyId?.name}</strong>
            </p>
          )}
        </div>

        {msg && <Alert variant="info">{msg}</Alert>}

        <div className="feature-card">
          <AppointmentTable
            appointments={appointments}
            showPatient={true}
            showDoctor={false}
            showActions={false}
            showMedicalRecordAction={true}
            onViewMedicalRecords={viewMedicalRecords}
            onExamine={examine}
          />

          {appointments.length === 0 && !loading && (
            <Alert variant="info">Chưa có lịch hẹn nào.</Alert>
          )}
        </div>

        {loading && <MySpinner />}
      </div>
    </div>
  );
};

export default DoctorAppointment;
