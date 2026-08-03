import { Button, Form } from "react-bootstrap";

const DoctorScheduleFilter = ({
  doctors,
  filterDoctorId,
  setFilterDoctorId,
  filterWeekStart,
  setFilterWeekStart,
}) => {
  const parseLocalDate = (value) => {
    return new Date(`${value}T00:00:00`);
  };

  const formatInputDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
  };

  const formatDisplayDate = (date) => {
    return date.toLocaleDateString("vi-VN");
  };

  const weekStartDate = parseLocalDate(filterWeekStart);

  const weekEndDate = new Date(weekStartDate);
  weekEndDate.setDate(weekEndDate.getDate() + 6);

  const changeWeek = (numberOfDays) => {
    const newWeekStart = new Date(weekStartDate);
    newWeekStart.setDate(newWeekStart.getDate() + numberOfDays);

    setFilterWeekStart(formatInputDate(newWeekStart));
  };
  return (
    <div className="feature-card" style={{ marginBottom: "30px" }}>
      <h3>Lọc lịch làm việc</h3>

      <Form.Group>
        <Form.Label>Bác sĩ</Form.Label>

        <Form.Select
          value={filterDoctorId}
          onChange={(e) => setFilterDoctorId(e.target.value)}
        >
          <option value="">Tất cả bác sĩ</option>

          {doctors.map((doctor) => (
            <option key={doctor.doctorId} value={doctor.doctorId}>
              {doctor.fullName}
            </option>
          ))}
        </Form.Select>
      </Form.Group>

      <div className="mt-3">
        <Form.Label>Tuần làm việc</Form.Label>

        <div className="d-flex align-items-center gap-2 flex-wrap">
          <Button
            type="button"
            variant="outline-primary"
            onClick={() => changeWeek(-7)}
          >
            ← Tuần trước
          </Button>

          <div
            className="border rounded px-3 py-2 text-center"
            style={{ minWidth: "240px" }}
          >
            {formatDisplayDate(weekStartDate)} -{" "}
            {formatDisplayDate(weekEndDate)}
          </div>

          <Button
            type="button"
            variant="outline-primary"
            onClick={() => changeWeek(7)}
          >
            Tuần sau →
          </Button>
        </div>
      </div>
    </div>
  );
};

export default DoctorScheduleFilter;
