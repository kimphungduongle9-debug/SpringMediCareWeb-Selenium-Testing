import { useContext, useEffect, useState } from "react";
import { Alert } from "react-bootstrap";
import { MyUserContext } from "../../configs/Contexts";
import { authApis, endpoints } from "../../configs/Apis";
import MySpinner from "../../components/MySpinner";
import AppointmentTable from "../../components/AppointmentTable";

const AdminAppointment = () => {
  const [user] = useContext(MyUserContext);
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const isAdminOrStaff =
    user !== null && (user.role === "admin" || user.role === "staff");

  const loadAppointments = async () => {
    let res = await authApis().get(endpoints.appointments);
    setAppointments(res.data);
  };

  const confirmAppointment = async (id) => {
    setLoading(true);

    try {
      await authApis().put(`${endpoints.appointments}/${id}/confirm`);
      setMsg("Xác nhận lịch hẹn thành công.");
      await loadAppointments();
    } catch (err) {
      console.error(err);
      setMsg("Không xác nhận được lịch hẹn.");
    } finally {
      setLoading(false);
    }
  };

  const cancelAppointment = async (id) => {
    if (window.confirm("Bạn chắc chắn muốn hủy lịch hẹn này không?") === false)
      return;

    setLoading(true);

    try {
      await authApis().put(`${endpoints.appointments}/${id}/cancel`);
      setMsg("Hủy lịch hẹn thành công.");
      await loadAppointments();
    } catch (err) {
      console.error(err);
      setMsg("Không hủy được lịch hẹn.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user !== null && isAdminOrStaff) {
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
          <Alert variant="warning">
            Vui lòng đăng nhập để sử dụng chức năng này.
          </Alert>
        </div>
      </div>
    );
  }

  if (!isAdminOrStaff) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="danger">
            Bạn không có quyền truy cập trang quản lý lịch hẹn.
          </Alert>
        </div>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="container">
        <div className="section-box">
          <h2>Quản lý lịch hẹn</h2>
          <p>Xem, xác nhận hoặc hủy lịch hẹn của bệnh nhân.</p>
        </div>

        {msg && <Alert variant="info">{msg}</Alert>}

        <div className="feature-card">
          <AppointmentTable
            appointments={appointments}
            showPatient={true}
            showDoctor={true}
            showActions={true}
            onConfirm={confirmAppointment}
            onCancel={cancelAppointment}
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

export default AdminAppointment;
