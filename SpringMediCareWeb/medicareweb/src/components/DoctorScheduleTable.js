import { Button, Table } from "react-bootstrap";

const DoctorScheduleTable = ({
  schedules,
  editSchedule,
  deleteSchedule,
  showActions = true,
}) => {
  const formatDate = (value) => {
    if (!value) return "";
    return new Date(value).toLocaleDateString("vi-VN");
  };

  const formatTime = (value) => {
    if (!value) return "";

    if (typeof value === "string") {
      return value.substring(0, 5);
    }

    return new Date(value).toLocaleTimeString("vi-VN", {
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const getShiftName = (shift) => {
    if (shift === "morning") return "Ca sáng";
    if (shift === "afternoon") return "Ca chiều";
    return "Ca tối";
  };

  return (
    <div className="feature-card">
      <h3>Danh sách lịch làm việc</h3>

      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>ID</th>
            <th>Bác sĩ</th>
            <th>Ngày</th>
            <th>Ca</th>
            <th>Bắt đầu</th>
            <th>Kết thúc</th>
            <th>Trạng thái</th>
            <th>Ghi chú</th>
            {showActions && <th>Thao tác</th>}
          </tr>
        </thead>

        <tbody>
          {schedules.map((s) => (
            <tr key={s.scheduleId}>
              <td>{s.scheduleId}</td>
              <td>{s.doctorId?.fullName}</td>
              <td>{formatDate(s.workDate)}</td>
              <td>{getShiftName(s.shift)}</td>
              <td>{formatTime(s.startTime)}</td>
              <td>{formatTime(s.endTime)}</td>
              <td>{s.status === "available" ? "Có lịch" : "Không làm"}</td>
              <td>{s.note}</td>
              {showActions && (
                <td>
                  <Button
                    variant="warning"
                    size="sm"
                    onClick={() => editSchedule(s)}
                  >
                    Sửa
                  </Button>

                  <Button
                    variant="danger"
                    size="sm"
                    className="ms-2"
                    onClick={() => deleteSchedule(s.scheduleId)}
                  >
                    Xóa
                  </Button>
                </td>
              )}
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default DoctorScheduleTable;
