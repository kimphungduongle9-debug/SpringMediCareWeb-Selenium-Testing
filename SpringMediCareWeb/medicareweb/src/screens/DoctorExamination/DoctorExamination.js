import { useEffect, useState } from "react";
import { Alert, Card, Col, Image, Row } from "react-bootstrap";
import { useNavigate, useSearchParams } from "react-router-dom";
import { authApis, endpoints } from "../../configs/Apis";
import MySpinner from "../../components/MySpinner";
import MedicalRecordForm from "../../components/MedicalRecordForm";

const DoctorExamination = () => {
  const [q] = useSearchParams();

  const nav = useNavigate();

  const [appointment, setAppointment] = useState(null);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const [diagnosis, setDiagnosis] = useState("");
  const [treatment, setTreatment] = useState("");

  const [saving, setSaving] = useState(false);

  const appointmentId = q.get("appointmentId");

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

  const loadAppointment = async () => {
    let res = await authApis().get(endpoints.appointmentDetail(appointmentId));

    setAppointment(res.data);
  };
  const saveMedicalRecord = async (e) => {
    e.preventDefault();

    if (!diagnosis.trim() || !treatment.trim()) {
      setMsg("Vui lòng nhập đầy đủ chẩn đoán và hướng điều trị.");
      return;
    }

    setSaving(true);
    setMsg("");

    try {
      await authApis().post(endpoints.medicalRecords, {
        appointmentId,
        diagnosis,
        treatment,
      });

      nav(`/doctor-medical-record?appointmentId=${appointmentId}`);
    } catch (err) {
      console.error(err);

      if (err.response?.status === 400) {
        setMsg("Không thể tạo hồ sơ bệnh án cho lịch hẹn này.");
      } else {
        setMsg("Lưu hồ sơ bệnh án thất bại.");
      }
    } finally {
      setSaving(false);
    }
  };
  useEffect(() => {
    if (appointmentId) {
      setLoading(true);

      loadAppointment()
        .catch((err) => {
          console.error(err);
          setMsg("Không tải được thông tin lịch hẹn.");
        })
        .finally(() => setLoading(false));
    }
  }, [appointmentId]);

  if (!appointmentId) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="warning">Không xác định được lịch hẹn.</Alert>
        </div>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="container">
        <div className="section-box">
          <h2>Khám bệnh</h2>

          <p className="text-secondary">
            Mã lịch hẹn:{" "}
            <span className="fw-semibold text-dark">{appointmentId}</span>
          </p>
        </div>

        {msg && <Alert variant="danger">{msg}</Alert>}

        {appointment && (
          <Card className="shadow-sm border-0">
            <Card.Header className="bg-info-subtle py-3">
              <h4 className="mb-0 text-primary">Thông tin lịch hẹn</h4>
            </Card.Header>

            <Card.Body className="p-4">
              <Row className="g-4 align-items-stretch">
                <Col md={3}>
                  <div className="border rounded p-3 h-100 text-center">
                    <Image
                      src={appointment.patientId?.image}
                      roundedCircle
                      width={140}
                      height={140}
                      className="object-fit-cover mb-3"
                    />

                    <h5 className="mb-1">{appointment.patientId?.fullName}</h5>

                    <p className="text-secondary mb-0">Bệnh nhân</p>
                  </div>
                </Col>

                <Col md={4}>
                  <div className="border rounded p-4 h-100">
                    <h5 className="text-primary mb-4">Thông tin bệnh nhân</h5>

                    <p className="mb-3">
                      <strong>Giới tính:</strong>
                      <br />
                      {appointment.patientId?.gender}
                    </p>

                    <p className="mb-0">
                      <strong>Địa chỉ:</strong>
                      <br />
                      {appointment.patientId?.address}
                    </p>
                  </div>
                </Col>

                <Col md={5}>
                  <div className="border rounded p-4 h-100">
                    <h5 className="text-primary mb-4">Nội dung lịch hẹn</h5>

                    <p className="mb-3">
                      <strong>Thời gian khám:</strong>
                      <br />
                      {formatDateTime(appointment.appointmentDate)}
                    </p>

                    <p className="mb-3">
                      <strong>Lý do khám:</strong>
                      <br />
                      {appointment.notes}
                    </p>

                    <p className="mb-0">
                      <strong>Trạng thái:</strong>
                      <br />
                      {appointment.status === "confirmed"
                        ? "Đã xác nhận"
                        : appointment.status}
                    </p>
                  </div>
                </Col>
              </Row>
            </Card.Body>
          </Card>
        )}

        {loading && <MySpinner />}

        {appointment && (
          <MedicalRecordForm
            title="Ghi nhận kết quả khám"
            diagnosis={diagnosis}
            treatment={treatment}
            setDiagnosis={setDiagnosis}
            setTreatment={setTreatment}
            onSubmit={saveMedicalRecord}
            saving={saving}
            submitLabel="Lưu hồ sơ bệnh án"
          />
        )}
      </div>
    </div>
  );
};

export default DoctorExamination;
