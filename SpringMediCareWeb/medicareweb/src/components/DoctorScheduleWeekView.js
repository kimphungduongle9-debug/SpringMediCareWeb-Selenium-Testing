import { Table } from "react-bootstrap";
import { formatScheduleDateKey } from "../utils/doctorScheduleDate";

const DoctorScheduleWeekView = ({ schedules, filterWeekStart }) => {
  const shiftRows = [
    {
      value: "morning",
      label: "Ca sáng",
      time: "07:00 - 11:30",
    },
    {
      value: "afternoon",
      label: "Ca chiều",
      time: "13:00 - 17:00",
    },
    {
      value: "evening",
      label: "Ca tối",
      time: "17:30 - 21:00",
    },
  ];

  const dayNames = [
    "Thứ Hai",
    "Thứ Ba",
    "Thứ Tư",
    "Thứ Năm",
    "Thứ Sáu",
    "Thứ Bảy",
    "Chủ Nhật",
  ];

  const formatInputDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const day = String(date.getDate()).padStart(2, "0");

    return `${year}-${month}-${day}`;
  };

  const formatDisplayDate = (date) => {
    return date.toLocaleDateString("vi-VN");
  };

  const weekStartDate = new Date(`${filterWeekStart}T00:00:00`);

  const weekDays = dayNames.map((name, index) => {
    const date = new Date(weekStartDate);
    date.setDate(date.getDate() + index);

    return {
      name,
      date,
      value: formatInputDate(date),
    };
  });

  const getSchedulesByDayAndShift = (date, shift) => {
    return schedules.filter((schedule) => {
      const scheduleDate = formatScheduleDateKey(schedule.workDate);

      return scheduleDate === date && schedule.shift === shift;
    });
  };

  return (
    <div className="feature-card" style={{ marginBottom: "30px" }}>
      <h3>Lịch làm việc theo tuần</h3>

      <Table bordered responsive className="text-center align-middle">
        <thead>
          <tr>
            <th style={{ minWidth: "130px" }}>Ca làm việc</th>

            {weekDays.map((day) => (
              <th key={day.value} style={{ minWidth: "150px" }}>
                <div>{day.name}</div>
                <small>{formatDisplayDate(day.date)}</small>
              </th>
            ))}
          </tr>
        </thead>

        <tbody>
          {shiftRows.map((shift) => (
            <tr key={shift.value}>
              <th>
                <div>{shift.label}</div>
                <small>{shift.time}</small>
              </th>

              {weekDays.map((day) => {
                const daySchedules = getSchedulesByDayAndShift(
                  day.value,
                  shift.value,
                );

                return (
                  <td key={`${day.value}-${shift.value}`}>
                    {daySchedules.length === 0 ? (
                      <span className="text-muted">Trống</span>
                    ) : (
                      daySchedules.map((schedule) => (
                        <div
                          key={schedule.scheduleId}
                          className="border rounded p-2 mb-2"
                        >
                          <strong>
                            {schedule.doctorId?.fullName || "Chưa có tên"}
                          </strong>

                          <div>
                            {schedule.status === "available"
                              ? "Có lịch"
                              : "Không làm"}
                          </div>

                          {schedule.note && (
                            <small className="text-muted">
                              {schedule.note}
                            </small>
                          )}
                        </div>
                      ))
                    )}
                  </td>
                );
              })}
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
};

export default DoctorScheduleWeekView;
