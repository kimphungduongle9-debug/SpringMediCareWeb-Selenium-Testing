import { useContext, useEffect, useState } from "react";
import { Alert, Button, Form } from "react-bootstrap";
import { useNavigate, useSearchParams } from "react-router-dom";
import Apis, { endpoints } from "../../configs/Apis";
import MySpinner from "../../components/MySpinner";
import { MyUserContext } from "../../configs/Contexts";
import DoctorBookedSlots from "../../components/DoctorBookedSlots";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const Booking = () => {
  const [user] = useContext(MyUserContext);
  const [q] = useSearchParams();
  const nav = useNavigate();

  const doctorId = q.get("doctorId");

  const [doctor, setDoctor] = useState(null);
  const [schedules, setSchedules] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [workDate, setWorkDate] = useState("");
  const [appointmentTime, setAppointmentTime] = useState("");
  const [notes, setNotes] = useState("");
  const [msg, setMsg] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedDate, setSelectedDate] = useState(null);

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

  const loadAppointments = async () => {
    if (doctorId !== null) {
      let res = await Apis.get(endpoints.appointmentsByDoctor(doctorId));

      setAppointments(res.data);
    }
  };

  useEffect(() => {
    Promise.all([loadDoctor(), loadSchedules(), loadAppointments()]).catch(
      (err) => {
        console.error(err);
        setMsg("Không tải được thông tin của bác sĩ.");
      },
    );
  }, [doctorId]);

  const formatDateValue = (dateValue) => {
    if (!dateValue) {
      return "";
    }

    const date = new Date(dateValue);

    if (Number.isNaN(date.getTime())) {
      return "";
    }

    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
  };

  const selectedSchedules = schedules.filter(
    (schedule) => formatDateValue(schedule.workDate) === workDate,
  );

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

    const patientId = user.patientId || user.id || user.userId;

    const data = {
      patientId: patientId.toString(),
      doctorId: doctorId.toString(),
      appointmentDate: `${workDate}T${appointmentTime}:00`,
      notes: notes,
    };

    setLoading(true);
    setMsg("");

    try {
      let res = await Apis.post(endpoints.appointments, data);

      setMsg(res.data || "Đặt lịch thành công. Vui lòng chờ xác nhận.");

      setAppointmentTime("");
      setNotes("");

      await loadAppointments();
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
        <div className="booking-heading">
          <h2>Đặt lịch hẹn khám</h2>

          <p>Chọn ngày và giờ khám phù hợp với lịch làm việc của bác sĩ.</p>
        </div>

        {msg && <Alert variant="info">{msg}</Alert>}

        <div className="booking-card">
          {doctor && (
            <div className="mb-4">
              <h3>{doctor.fullName}</h3>

              <p className="mb-0">
                <strong>Chuyên khoa:</strong>{" "}
                {doctor.specialtyId?.name || "Chưa rõ"}
              </p>
            </div>
          )}

          <Form onSubmit={bookAppointment}>
            <Form.Group className="mb-3">
              <Form.Label>Ngày khám</Form.Label>

              <DatePicker
                selected={selectedDate}
                onChange={(date) => {
                  setSelectedDate(date);
                  setAppointmentTime("");

                  if (date === null) {
                    setWorkDate("");
                    return;
                  }

                  const year = date.getFullYear();
                  const month = String(date.getMonth() + 1).padStart(2, "0");
                  const day = String(date.getDate()).padStart(2, "0");

                  setWorkDate(`${year}-${month}-${day}`);
                }}
                dateFormat="dd/MM/yyyy"
                placeholderText="Chọn ngày khám"
                className="form-control"
                wrapperClassName="w-100"
                showPopperArrow={false}
                required
              />
            </Form.Group>

            <div className="row g-2 mb-3">
              <div className="col-md-6">
                <div className="booking-info-box">
                  <h7 className="mb-2 fw-normal">Lịch làm việc trong ngày</h7>

                  {!workDate ? (
                    <p className="text-muted mb-0">
                      Chọn ngày khám để xem lịch làm việc.
                    </p>
                  ) : selectedSchedules.length === 0 ? (
                    <p className="text-warning mb-0">
                      Bác sĩ không có lịch làm việc trong ngày này.
                    </p>
                  ) : (
                    selectedSchedules.map((schedule) => (
                      <div
                        key={schedule.scheduleId}
                        className="d-flex justify-content-between align-items-center border-bottom py-1"
                      >
                        <span>
                          {schedule.startTime.substring(0, 5)} -{" "}
                          {schedule.endTime.substring(0, 5)}
                        </span>

                        <span
                          className={
                            schedule.status === "available"
                              ? "text-success"
                              : "text-danger"
                          }
                        >
                          {schedule.status === "available"
                            ? "Có làm việc"
                            : "Không làm việc"}
                        </span>
                      </div>
                    ))
                  )}
                </div>
              </div>

              <div className="col-md-6">
                <div className="booking-info-box">
                  <DoctorBookedSlots
                    appointments={appointments}
                    workDate={workDate}
                  />
                </div>
              </div>
            </div>

            <Form.Group className="mb-3">
              <Form.Label>Giờ khám</Form.Label>

              <Form.Control
                type="time"
                value={appointmentTime}
                onChange={(e) => setAppointmentTime(e.target.value)}
                disabled={!workDate}
                required
              />

              <Form.Text>
                Chọn giờ nằm trong lịch làm việc của bác sĩ và tránh các giờ đã
                có người đặt.
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
            {!workDate && (
              <Alert variant="warning" className="py-2">
                Vui lòng chọn ngày khám để tiếp tục.
              </Alert>
            )}

            {workDate && !appointmentTime && (
              <Alert variant="warning" className="py-2">
                Vui lòng chọn giờ khám để tiếp tục.
              </Alert>
            )}

            <Button
              type="submit"
              variant="primary"
              disabled={loading || !workDate || !appointmentTime}
            >
              {loading ? "Đang đặt lịch..." : "Đặt lịch"}
            </Button>

            <Button
              type="button"
              variant="secondary"
              className="ms-2"
              onClick={() => nav("/doctor")}
              disabled={loading}
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
