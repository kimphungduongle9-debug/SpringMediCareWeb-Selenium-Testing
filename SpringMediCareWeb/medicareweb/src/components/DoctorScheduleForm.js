import { Button, Form } from "react-bootstrap";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
const parseLocalDate = (value) => {
  if (!value) return null;

  const [year, month, day] = value.split("-").map(Number);
  return new Date(year, month - 1, day);
};

const formatLocalDate = (date) => {
  if (!date) return "";

  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`;
};
const DoctorScheduleForm = ({
  scheduleId,
  doctors,
  doctorId,
  setDoctorId,
  workDate,
  setWorkDate,
  shift,
  changeShift,
  status,
  setStatus,
  note,
  setNote,
  saveSchedule,
  resetForm,
}) => {
  return (
    <div className="feature-card" style={{ marginBottom: "30px" }}>
      <h3>
        {scheduleId === null ? "Thêm lịch làm việc" : "Cập nhật lịch làm việc"}
      </h3>

      <Form onSubmit={saveSchedule}>
        <Form.Group className="mb-3">
          <Form.Label>Bác sĩ</Form.Label>
          <Form.Select
            value={doctorId}
            onChange={(e) => setDoctorId(e.target.value)}
            required
          >
            <option value="">-- Chọn bác sĩ --</option>
            {doctors.map((d) => (
              <option key={d.doctorId} value={d.doctorId}>
                {d.fullName}
              </option>
            ))}
          </Form.Select>
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Ngày làm việc</Form.Label>
          <Form.Control
            type="date"
            value={workDate}
            onChange={(e) => setWorkDate(e.target.value)}
            required
          />
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Ca làm việc</Form.Label>
          <Form.Select
            value={shift}
            onChange={(e) => changeShift(e.target.value)}
            required
          >
            <option value="morning">Ca sáng: 07:00 - 11:30</option>
            <option value="afternoon">Ca chiều: 13:00 - 17:00</option>
            <option value="evening">Ca tối: 17:30 - 21:00</option>
          </Form.Select>
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Trạng thái</Form.Label>
          <Form.Select
            value={status}
            onChange={(e) => setStatus(e.target.value)}
          >
            <option value="available">Có lịch làm việc</option>
            <option value="unavailable">Không làm việc</option>
          </Form.Select>
        </Form.Group>

        <Form.Group className="mb-3">
          <Form.Label>Ghi chú</Form.Label>
          <DatePicker
            selected={parseLocalDate(workDate)}
            onChange={(date) => setWorkDate(formatLocalDate(date))}
            dateFormat="dd/MM/yyyy"
            placeholderText="dd/mm/yyyy"
            className="form-control"
            wrapperClassName="w-100"
            showPopperArrow={false}
            required
          />
        </Form.Group>

        <Button type="submit" variant="primary">
          {scheduleId === null ? "Thêm lịch" : "Cập nhật"}
        </Button>

        {scheduleId !== null && (
          <Button
            type="button"
            variant="secondary"
            className="ms-2"
            onClick={resetForm}
          >
            Hủy sửa
          </Button>
        )}
      </Form>
    </div>
  );
};

export default DoctorScheduleForm;
