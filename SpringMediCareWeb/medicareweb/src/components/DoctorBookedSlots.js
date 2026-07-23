import { Badge } from "react-bootstrap";

const DoctorBookedSlots = ({ appointments, workDate }) => {
  const bookedAppointments = appointments.filter((appointment) => {
    const appointmentDate = new Date(appointment.appointmentDate);

    const year = appointmentDate.getFullYear();
    const month = String(appointmentDate.getMonth() + 1).padStart(2, "0");
    const day = String(appointmentDate.getDate()).padStart(2, "0");

    const formattedDate = `${year}-${month}-${day}`;

    return (
      formattedDate === workDate &&
      (appointment.status === "pending" || appointment.status === "confirmed")
    );
  });

  return (
    <div>
      <h6 className="booking-info-title">Giờ đã được đặt</h6>

      {!workDate ? (
        <p className="text-muted mb-0">
          Chọn ngày khám để xem các giờ đã có người đặt.
        </p>
      ) : bookedAppointments.length === 0 ? (
        <p className="text-success mb-0">Ngày này chưa có lịch hẹn.</p>
      ) : (
        <div className="d-flex flex-wrap gap-2">
          {bookedAppointments.map((appointment) => (
            <Badge
              key={appointment.appointmentId}
              bg="danger"
              className="px-3 py-2"
            >
              {new Date(appointment.appointmentDate).toLocaleTimeString(
                "vi-VN",
                {
                  hour: "2-digit",
                  minute: "2-digit",
                },
              )}
            </Badge>
          ))}
        </div>
      )}
    </div>
  );
};

export default DoctorBookedSlots;
