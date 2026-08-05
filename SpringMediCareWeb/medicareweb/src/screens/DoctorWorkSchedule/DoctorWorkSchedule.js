import { useContext, useEffect, useState } from "react";
import { Alert } from "react-bootstrap";
import { MyUserContext } from "../../configs/Contexts";
import { authApis, endpoints } from "../../configs/Apis";
import MySpinner from "../../components/MySpinner";
import DoctorScheduleTable from "../../components/DoctorScheduleTable";
import DoctorScheduleWeekView from "../../components/DoctorScheduleWeekView";
import DoctorScheduleWeekNavigation from "../../components/DoctorScheduleWeekNavigation";
import { formatScheduleDateKey } from "../../utils/doctorScheduleDate";

const formatLocalDate = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");

  return `${year}-${month}-${day}`;
};

const getStartOfWeek = (date) => {
  const result = new Date(date);
  result.setHours(0, 0, 0, 0);

  const day = result.getDay();
  const distanceToMonday = day === 0 ? -6 : 1 - day;

  result.setDate(result.getDate() + distanceToMonday);

  return result;
};

const DoctorWorkSchedule = () => {
  const [user] = useContext(MyUserContext);

  const [doctor, setDoctor] = useState(null);
  const [schedules, setSchedules] = useState([]);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const [filterWeekStart, setFilterWeekStart] = useState(() =>
    formatLocalDate(getStartOfWeek(new Date())),
  );

  const isDoctor = user !== null && user.role === "doctor";

  const loadDoctor = async () => {
    const res = await authApis().get(endpoints.doctorByUser(user.id));

    setDoctor(res.data);

    return res.data;
  };

  const loadSchedules = async () => {
    const currentDoctor = await loadDoctor();

    const res = await authApis().get(
      endpoints.doctorSchedulesByDoctor(currentDoctor.doctorId),
    );

    setSchedules(res.data);
  };

  useEffect(() => {
    if (user !== null && isDoctor) {
      setLoading(true);

      loadSchedules()
        .catch((err) => {
          console.error(err);
          setMsg("Không tải được lịch làm việc.");
        })
        .finally(() => setLoading(false));
    }
  }, [user]);

  const weekEndDate = new Date(`${filterWeekStart}T00:00:00`);
  weekEndDate.setDate(weekEndDate.getDate() + 6);

  const filterWeekEnd = formatLocalDate(weekEndDate);

  const filteredSchedules = schedules.filter((schedule) => {
    const scheduleDate = formatScheduleDateKey(schedule.workDate);

    return (
      scheduleDate !== "" &&
      scheduleDate >= filterWeekStart &&
      scheduleDate <= filterWeekEnd
    );
  });

  if (user === null) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="warning">
            Vui lòng đăng nhập để xem lịch làm việc.
          </Alert>
        </div>
      </div>
    );
  }

  if (!isDoctor) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="danger">
            Chỉ tài khoản bác sĩ mới được xem trang này.
          </Alert>
        </div>
      </div>
    );
  }

  return (
    <div className="main-content" style={{ paddingTop: "60px" }}>
      <div className="container">
        <div className="section-box">
          <h2>Lịch làm việc của tôi</h2>

          {doctor && (
            <p>
              Bác sĩ: <strong>{doctor.fullName}</strong> - Chuyên khoa:{" "}
              <strong>{doctor.specialtyId?.name}</strong>
            </p>
          )}
        </div>

        {msg && <Alert variant="info">{msg}</Alert>}

        <div className="feature-card" style={{ marginBottom: "30px" }}>
          <h3>Chọn tuần làm việc</h3>

          <DoctorScheduleWeekNavigation
            filterWeekStart={filterWeekStart}
            setFilterWeekStart={setFilterWeekStart}
          />
        </div>

        <DoctorScheduleWeekView
          schedules={filteredSchedules}
          filterWeekStart={filterWeekStart}
        />

        <DoctorScheduleTable
          schedules={filteredSchedules}
          showActions={false}
        />

        {filteredSchedules.length === 0 && !loading && (
          <Alert variant="info" className="mt-3">
            Không có lịch làm việc trong tuần này.
          </Alert>
        )}

        {loading && <MySpinner />}
      </div>
    </div>
  );
};

export default DoctorWorkSchedule;
