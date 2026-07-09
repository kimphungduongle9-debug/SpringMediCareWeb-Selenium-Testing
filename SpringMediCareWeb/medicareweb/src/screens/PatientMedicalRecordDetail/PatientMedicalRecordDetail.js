import { useContext, useEffect, useState } from "react";
import { Alert } from "react-bootstrap";
import { useParams } from "react-router-dom";
import { MyUserContext } from "../../configs/Contexts";
import { authApis, endpoints } from "../../configs/Apis";
import MySpinner from "../../components/MySpinner";
import MedicalRecordDetail from "../../components/MedicalRecordDetail";
import TestResultList from "../../components/TestResultList";
import PrescriptionList from "../../components/PrescriptionList";

const PatientMedicalRecordDetail = () => {
  const [user] = useContext(MyUserContext);
  const { recordId } = useParams();

  const [medicalRecord, setMedicalRecord] = useState(null);
  const [testResults, setTestResults] = useState([]);
  const [prescriptions, setPrescriptions] = useState([]);
  const [loading, setLoading] = useState(false);

  const [msg, setMsg] = useState("");

  const isPatient = user !== null && user.role === "patient";

  const loadTestResults = async () => {
    let res = await authApis().get(
      endpoints.testResultsByMedicalRecord(recordId),
    );

    setTestResults(res.data);
  };
  const loadPrescriptions = async () => {
    let res = await authApis().get(
      endpoints.prescriptionsByMedicalRecord(recordId),
    );

    let prescriptionList = [];

    for (let prescription of res.data) {
      let detailRes = await authApis().get(
        endpoints.prescriptionDetailsByPrescription(
          prescription.prescriptionId,
        ),
      );

      prescriptionList.push({
        ...prescription,
        details: detailRes.data,
      });
    }

    setPrescriptions(prescriptionList);
  };
  const loadMedicalRecord = async () => {
    let res = await authApis().get(endpoints.medicalRecordDetail(recordId));

    if (res.data.patientId?.patientId !== user.patientId) {
      setMsg("Bạn không được phép xem hồ sơ bệnh án này.");
      return;
    }

    setMedicalRecord(res.data);

    await loadTestResults();
    await loadPrescriptions();
  };

  useEffect(() => {
    if (user !== null && isPatient && user.patientId && recordId) {
      setLoading(true);

      loadMedicalRecord()
        .catch((err) => {
          console.error(err);

          if (err.response?.status === 404) {
            setMsg("Không tìm thấy hồ sơ bệnh án.");
          } else {
            setMsg("Không tải được chi tiết hồ sơ bệnh án.");
          }
        })
        .finally(() => setLoading(false));
    }
  }, [user, recordId]);

  if (user === null) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="warning">
            Vui lòng đăng nhập để xem hồ sơ bệnh án.
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
          <h2>Chi tiết hồ sơ bệnh án</h2>

          <p>Thông tin chẩn đoán và hướng điều trị trong lần khám bệnh.</p>
        </div>

        {medicalRecord && <MedicalRecordDetail medicalRecord={medicalRecord} />}

        {medicalRecord && <TestResultList testResults={testResults} />}

        {medicalRecord && <PrescriptionList prescriptions={prescriptions} />}

        {loading && <MySpinner />}
      </div>
    </div>
  );
};

export default PatientMedicalRecordDetail;
