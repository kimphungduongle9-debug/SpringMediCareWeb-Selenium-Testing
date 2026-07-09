import { Button, Table } from "react-bootstrap";

const MedicalRecordTable = ({
  medicalRecords,
  showDoctor = false,
  showPatient = false,
  showActions = false,
  showView = false,
  onEdit,
  onView,
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

  return (
    <Table striped bordered hover responsive>
      <thead>
        <tr>
          <th>ID</th>

          {showPatient && <th>Bệnh nhân</th>}

          {showDoctor && <th>Bác sĩ</th>}

          <th>Chẩn đoán</th>
          <th>Điều trị</th>
          <th>Ngày tạo</th>

          {(showActions || showView) && <th>Thao tác</th>}
        </tr>
      </thead>

      <tbody>
        {medicalRecords.map((record) => (
          <tr key={record.recordId}>
            <td>{record.recordId}</td>

            {showPatient && <td>{record.patientId?.fullName}</td>}

            {showDoctor && <td>{record.doctorId?.fullName}</td>}

            <td>{record.diagnosis}</td>
            <td>{record.treatment}</td>
            <td>{formatDateTime(record.createdDate)}</td>

            {(showActions || showView) && (
              <td>
                <div className="d-flex gap-2">
                  {showView && (
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={() => onView(record)}
                    >
                      Xem chi tiết
                    </Button>
                  )}

                  {showActions && (
                    <Button
                      variant="warning"
                      size="sm"
                      onClick={() => onEdit(record)}
                    >
                      Sửa
                    </Button>
                  )}
                </div>
              </td>
            )}
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

export default MedicalRecordTable;
