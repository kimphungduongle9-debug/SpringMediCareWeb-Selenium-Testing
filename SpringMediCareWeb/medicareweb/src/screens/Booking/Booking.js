import { useContext, useEffect, useState } from "react";
import { Alert, Button, Form } from "react-bootstrap";
import { useNavigate, useSearchParams } from "react-router-dom";
import Apis, { endpoints } from "../../configs/Apis";
import MySpinner from "../../components/MySpinner";
import { MyUserContext } from "../../configs/Contexts";

const Booking = () => {
  const [user] = useContext(MyUserContext);
  const [q] = useSearchParams();
  const nav = useNavigate();

  const doctorId = q.get("doctorId");

  const [doctor, setDoctor] = useState(null);
  const [schedules, setSchedules] = useState([]);
  const [workDate, setWorkDate] = useState("");
  const [appointmentTime, setAppointmentTime] = useState("");
  const [notes, setNotes] = useState("");
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);

  const loadDoctor = async () => {
    if (doctorId !== null) {
      let res = await Apis.get(`${endpoints.doctors}/${doctorId}`);
      setDoctor(res.data);
    }
  };
  const loadSchedules = async () => {
    if (doctorId !== null) {
      let res = await Apis.get(endpoints.doctorSchedulesByDoctor(doctorId));

      setSchedules(res.data);
    }
  };
  useEffect(() => {
    Promise.all([loadDoctor(), loadSchedules()]).catch((err) => {
      console.error(err);
      setMsg("Không tải được thông tin hoặc lịch làm việc của bác sĩ.");
    });
  }, [doctorId]);

  const bookAppointment = async (e) => {
    e.preventDefault();

    if (user === null) {
      setMsg("Vui lòng đăng nhập trước khi đặt lịch.");
      return;
    }

    if (!user.patientId && !user.id && !user.userId) {
      setMsg("Không tìm thấy thông tin bệnh nhân trong tài khoản.");
      return;
    }

    let patientId = user.patientId || user.id || user.userId;

    let data = {
      patientId: patientId.toString(),
      doctorId: doctorId.toString(),
      appointmentDate: `${workDate}T${appointmentTime}:00`,
      notes: notes,
    };

    setLoading(true);

    try {
      let res = await Apis.post(endpoints.appointments, data);
      setMsg(res.data || "Đặt lịch thành công. Vui lòng chờ xác nhận.");
    } catch (err) {
      console.error(err);
      setMsg(
        "Đặt lịch thất bại. Bác sĩ có thể không làm giờ này hoặc giờ đã có người đặt.",
      );
    } finally {
      setLoading(false);
    }
  };

  if (doctorId === null) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="danger">Thiếu thông tin bác sĩ để đặt lịch.</Alert>
        </div>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="container">
        <div className="section-box">
          <h2>Đặt lịch hẹn khám</h2>
          <p>
            Chọn ngày khám và nhập giờ khám phù hợp với lịch làm việc của bác
            sĩ.
          </p>
        </div>

        {msg && <Alert variant="info">{msg}</Alert>}

        <div className="feature-card">
          {doctor && (
            <div style={{ marginBottom: "20px" }}>
              <h3>{doctor.fullName}</h3>
              <p>
                <strong>Chuyên khoa:</strong>{" "}
                {doctor.specialtyId?.name || "Chưa rõ"}
              </p>
            </div>
          )}
          <div style={{ marginBottom: "20px" }}>
            <h4>Lịch làm việc của bác sĩ</h4>

            {schedules.length === 0 ? (
              <Alert variant="warning">
                Bác sĩ hiện chưa có lịch làm việc.
              </Alert>
            ) : (
              schedules.map((s) => (
                <div key={s.scheduleId}>
                  {new Date(s.workDate).toLocaleDateString("vi-VN")} -{" "}
                  {s.startTime.substring(0, 5)} đến {s.endTime.substring(0, 5)}{" "}
                  -{" "}
                  {s.status === "available" ? "Có làm việc" : "Không làm việc"}
                </div>
              ))
            )}
          </div>
          <Form onSubmit={bookAppointment}>
            <Form.Group className="mb-3">
              <Form.Label>Ngày khám</Form.Label>
              <Form.Control
                type="date"
                value={workDate}
                onChange={(e) => setWorkDate(e.target.value)}
                required
              />
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Giờ khám</Form.Label>
              <Form.Control
                type="time"
                value={appointmentTime}
                onChange={(e) => setAppointmentTime(e.target.value)}
                required
              />
              <Form.Text>
                Vui lòng nhập giờ nằm trong lịch làm việc của bác sĩ. Ca sáng:
                07:00 - 11:30, ca chiều: 13:00 - 17:00, ca tối: 17:30 - 21:00.
              </Form.Text>
            </Form.Group>

            <Form.Group className="mb-3">
              <Form.Label>Ghi chú</Form.Label>
              <Form.Control
                as="textarea"
                rows={3}
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
                placeholder="Nhập triệu chứng hoặc yêu cầu nếu có..."
              />
            </Form.Group>

            <Button type="submit" variant="primary">
              Đặt lịch
            </Button>

            <Button
              type="button"
              variant="secondary"
              className="ms-2"
              onClick={() => nav("/doctor")}
            >
              Quay lại
            </Button>
          </Form>
        </div>

        {loading && <MySpinner />}
      </div>
    </div>
  );
};

export default Booking;
