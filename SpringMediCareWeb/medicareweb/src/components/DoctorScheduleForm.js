import { Button, Form } from "react-bootstrap";

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
          <Form.Control
            type="text"
            value={note}
            onChange={(e) => setNote(e.target.value)}
            placeholder="Ví dụ: Ca sáng, ca chiều, nghỉ phép..."
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
