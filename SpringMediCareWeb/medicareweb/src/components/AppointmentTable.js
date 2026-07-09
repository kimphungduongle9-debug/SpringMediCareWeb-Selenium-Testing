import { Button, Table } from "react-bootstrap";

const AppointmentTable = ({
  appointments,
  showPatient = false,
  showDoctor = false,
  showActions = false,
  showMedicalRecordAction = false,
  onConfirm,
  onCancel,
  onViewMedicalRecords,
  onExamine,
}) => {
  const formatDateTime = (value) => {
    if (!value) return "";

    return new Date(value).toLocaleString("vi-VN", {
      hour: "2-digit",
      minute: "2-digit",
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });
  };

  const getStatusName = (status) => {
    if (status === "pending") return "Chờ xác nhận";
    if (status === "confirmed") return "Đã xác nhận";
    if (status === "completed") return "Đã hoàn thành";
    if (status === "cancelled") return "Đã hủy";

    return status;
  };

  const getPatientName = (appointment) => {
    if (appointment.patientId?.userId) {
      return `${appointment.patientId.userId.firstName} ${appointment.patientId.userId.lastName}`;
    }

    if (appointment.patientId?.fullName) {
      return appointment.patientId.fullName;
    }

    return "";
  };

  return (
    <Table striped bordered hover responsive>
      <thead>
        <tr>
          <th>ID</th>

          {showPatient && <th>Bệnh nhân</th>}

          {showDoctor && <th>Bác sĩ</th>}

          <th>Thời gian khám</th>
          <th>Trạng thái</th>
          <th>Ghi chú</th>

          {showActions && <th>Thao tác</th>}

          {showMedicalRecordAction && <th>Hồ sơ bệnh án</th>}
        </tr>
      </thead>

      <tbody>
        {appointments.map((a) => (
          <tr key={a.appointmentId}>
            <td>{a.appointmentId}</td>

            {showPatient && <td>{getPatientName(a)}</td>}

            {showDoctor && <td>{a.doctorId?.fullName}</td>}

            <td>{formatDateTime(a.appointmentDate)}</td>
            <td>{getStatusName(a.status)}</td>
            <td>{a.notes}</td>

            {showActions && (
              <td>
                {a.status === "pending" ? (
                  <>
                    <Button
                      variant="success"
                      size="sm"
                      onClick={() => onConfirm(a.appointmentId)}
                    >
                      Xác nhận
                    </Button>

                    <Button
                      variant="danger"
                      size="sm"
                      className="ms-2"
                      onClick={() => onCancel(a.appointmentId)}
                    >
                      Hủy
                    </Button>
                  </>
                ) : (
                  <span>{getStatusName(a.status)}</span>
                )}
              </td>
            )}

            {showMedicalRecordAction && (
              <td>
                {a.status === "confirmed" && (
                  <Button
                    variant="success"
                    size="sm"
                    onClick={() => onExamine(a)}
                  >
                    Khám bệnh
                  </Button>
                )}

                {a.status === "completed" && (
                  <Button
                    variant="info"
                    size="sm"
                    onClick={() => onViewMedicalRecords(a)}
                  >
                    Xem hồ sơ
                  </Button>
                )}

                {a.status === "pending" && (
                  <span className="text-secondary">Chờ xác nhận</span>
                )}

                {a.status === "cancelled" && (
                  <span className="text-danger">Đã hủy</span>
                )}
              </td>
            )}
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

export default AppointmentTable;
