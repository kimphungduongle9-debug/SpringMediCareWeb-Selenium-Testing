import { useContext, useEffect, useState } from "react";
import { Alert } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { MyUserContext } from "../../configs/Contexts";
import { authApis, endpoints } from "../../configs/Apis";
import MySpinner from "../../components/MySpinner";
import MedicalRecordTable from "../../components/MedicalRecordTable";

const PatientMedicalHistory = () => {
  const [user] = useContext(MyUserContext);
  const nav = useNavigate();

  const [medicalRecords, setMedicalRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const isPatient = user !== null && user.role === "patient";

  const loadMedicalRecords = async () => {
    let res = await authApis().get(
      endpoints.medicalRecordsByPatient(user.patientId),
    );

    setMedicalRecords(res.data);
  };

  const viewMedicalRecord = (record) => {
    nav(`/patient-medical-record/${record.recordId}`);
  };

  useEffect(() => {
    if (user !== null && isPatient && user.patientId) {
      setLoading(true);

      loadMedicalRecords()
        .catch((err) => {
          console.error(err);
          setMsg("Không tải được lịch sử khám bệnh.");
        })
        .finally(() => setLoading(false));
    }
  }, [user]);

  if (user === null) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="warning">
            Vui lòng đăng nhập để xem lịch sử khám bệnh.
          </Alert>
        </div>
      </div>
    );
  }

  if (!isPatient) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="danger">
            Chỉ tài khoản bệnh nhân mới được xem trang này.
          </Alert>
        </div>
      </div>
    );
  }

  if (!user.patientId) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="warning">
            Không tìm thấy hồ sơ bệnh nhân của tài khoản hiện tại.
          </Alert>
        </div>
      </div>
    );
  }

  return (
    <div className="main-content">
      <div className="container">
        <div className="section-box">
          <h2>Lịch sử khám bệnh</h2>
          <p>Danh sách các hồ sơ khám bệnh đã được bác sĩ ghi nhận.</p>
        </div>

        {msg && <Alert variant="info">{msg}</Alert>}

        <div className="feature-card">
          <MedicalRecordTable
            medicalRecords={medicalRecords}
            showDoctor={true}
            showView={true}
            onView={viewMedicalRecord}
          />

          {medicalRecords.length === 0 && !loading && (
            <Alert variant="info">Bạn chưa có hồ sơ khám bệnh nào.</Alert>
          )}
        </div>

        {loading && <MySpinner />}
      </div>
    </div>
  );
};

export default PatientMedicalHistory;
