import { useContext, useEffect, useState } from "react";
import { Alert } from "react-bootstrap";
import Apis, { authApis, endpoints } from "../../configs/Apis";
import MySpinner from "../../components/MySpinner";
import { MyUserContext } from "../../configs/Contexts";
import DoctorScheduleForm from "../../components/DoctorScheduleForm";
import DoctorScheduleTable from "../../components/DoctorScheduleTable";
import DoctorScheduleFilter from "../../components/DoctorScheduleFilter";
import DoctorScheduleWeekView from "../../components/DoctorScheduleWeekView";
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
const DoctorSchedule = () => {
  const [user] = useContext(MyUserContext);
  const isAdminOrStaff =
    user !== null && (user.role === "admin" || user.role === "staff");
  const [schedules, setSchedules] = useState([]);
  const [doctors, setDoctors] = useState([]);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const [filterDoctorId, setFilterDoctorId] = useState("");
  const [filterWeekStart, setFilterWeekStart] = useState(() =>
    formatLocalDate(getStartOfWeek(new Date())),
  );

  const [scheduleId, setScheduleId] = useState(null);
  const [doctorId, setDoctorId] = useState("");
  const [workDate, setWorkDate] = useState("");

  const [shift, setShift] = useState("morning");
  const [startTime, setStartTime] = useState("07:00");
  const [endTime, setEndTime] = useState("11:30");
  const [status, setStatus] = useState("available");
  const [note, setNote] = useState("");

  const loadDoctors = async () => {
    let res = await Apis.get(endpoints.allDoctors);
    setDoctors(res.data);
  };

  const loadSchedules = async () => {
    let res = await Apis.get(endpoints.doctorSchedules);

    console.log("DANH SÁCH LỊCH:", res.data);
    console.log("LỊCH ĐẦU TIÊN:", res.data[0]);
    console.log("WORK DATE:", res.data[0]?.workDate);
    console.log("DOCTOR ID:", res.data[0]?.doctorId?.doctorId);

    setSchedules(res.data);
  };

  const resetForm = () => {
    setScheduleId(null);
    setDoctorId("");
    setWorkDate("");
    setShift("morning");
    setStartTime("07:00");
    setEndTime("11:30");
    setStatus("available");
    setNote("");
  };
  const changeShift = (value) => {
    setShift(value);

    if (value === "morning") {
      setStartTime("07:00");
      setEndTime("11:30");
    } else if (value === "afternoon") {
      setStartTime("13:00");
      setEndTime("17:00");
    } else if (value === "evening") {
      setStartTime("17:30");
      setEndTime("21:00");
    }
  };
  const saveSchedule = async (e) => {
    e.preventDefault();

    let data = {
      doctorId: parseInt(doctorId, 10),
      workDate: workDate,
      shift: shift,
      startTime: `${startTime}:00`,
      endTime: `${endTime}:00`,
      status: status,
      note: note,
    };
    setLoading(true);

    try {
      if (scheduleId === null) {
        await authApis().post(endpoints.secureDoctorSchedules, data);
        setMsg("Thêm lịch làm việc thành công!");
      } else {
        await authApis().put(
          endpoints.secureDoctorScheduleDetail(scheduleId),
          data,
        );
        setMsg("Cập nhật lịch làm việc thành công!");
      }

      resetForm();
      await loadSchedules();
    } catch (err) {
      console.error(err);
      setMsg("Có lỗi xảy ra. Kiểm tra lại đăng nhập hoặc dữ liệu nhập.");
    } finally {
      setLoading(false);
    }
  };

  const editSchedule = (s) => {
    setScheduleId(s.scheduleId);
    setDoctorId(s.doctorId?.doctorId || "");
    setWorkDate(formatScheduleDateKey(s.workDate));
    setShift(s.shift || "morning");
    setStartTime(
      s.startTime ? new Date(s.startTime).toTimeString().slice(0, 5) : "07:00",
    );
    setEndTime(
      s.endTime ? new Date(s.endTime).toTimeString().slice(0, 5) : "11:30",
    );
    setStatus(s.status || "available");
    setNote(s.note || "");
    window.scrollTo(0, 0);
  };

  const deleteSchedule = async (id) => {
    if (window.confirm("Bạn chắc chắn muốn xóa lịch này không?") === false)
      return;

    setLoading(true);

    try {
      await authApis().delete(endpoints.secureDoctorScheduleDetail(id));
      setMsg("Xóa lịch làm việc thành công!");
      await loadSchedules();
    } catch (err) {
      console.error(err);
      setMsg("Không xóa được lịch. Kiểm tra lại quyền đăng nhập.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setLoading(true);

    Promise.all([loadDoctors(), loadSchedules()])
      .catch((err) => {
        console.error(err);
        setMsg("Không tải được dữ liệu lịch làm việc.");
      })
      .finally(() => setLoading(false));
  }, []);
  const weekEndDate = new Date(`${filterWeekStart}T00:00:00`);
  weekEndDate.setDate(weekEndDate.getDate() + 6);

  const filterWeekEnd = formatLocalDate(weekEndDate);

  const filteredSchedules = schedules.filter((schedule) => {
    const scheduleDoctorId = schedule.doctorId?.doctorId ?? schedule.doctorId;

    const matchesDoctor =
      filterDoctorId === "" ||
      String(scheduleDoctorId) === String(filterDoctorId);

    const scheduleDate = formatScheduleDateKey(schedule.workDate);

    const matchesWeek =
      scheduleDate !== "" &&
      scheduleDate >= filterWeekStart &&
      scheduleDate <= filterWeekEnd;

    return matchesDoctor && matchesWeek;
  });
  if (user === null) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="warning">
            Vui lòng đăng nhập để sử dụng chức năng này.
          </Alert>
        </div>
      </div>
    );
  }

  if (!isAdminOrStaff) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="danger">
            Bạn không có quyền truy cập trang quản lý lịch làm việc.
          </Alert>
        </div>
      </div>
    );
  }
  return (
    <div className="main-content">
      <div className="container">
        <div className="section-box">
          <h2>Quản lý lịch làm việc bác sĩ</h2>
          <p>Thêm, cập nhật và theo dõi ca làm việc của bác sĩ.</p>
        </div>

        {msg && <Alert variant="info">{msg}</Alert>}

        <DoctorScheduleForm
          scheduleId={scheduleId}
          doctors={doctors}
          doctorId={doctorId}
          setDoctorId={setDoctorId}
          workDate={workDate}
          setWorkDate={setWorkDate}
          shift={shift}
          changeShift={changeShift}
          status={status}
          setStatus={setStatus}
          note={note}
          setNote={setNote}
          saveSchedule={saveSchedule}
          resetForm={resetForm}
        />
        <DoctorScheduleFilter
          doctors={doctors}
          filterDoctorId={filterDoctorId}
          setFilterDoctorId={setFilterDoctorId}
          filterWeekStart={filterWeekStart}
          setFilterWeekStart={setFilterWeekStart}
        />

        <DoctorScheduleWeekView
          schedules={filteredSchedules}
          filterWeekStart={filterWeekStart}
        />

        <DoctorScheduleTable
          schedules={schedules}
          editSchedule={editSchedule}
          deleteSchedule={deleteSchedule}
        />
        {schedules.length === 0 && !loading && (
          <Alert variant="info" className="mt-3">
            Chưa có lịch làm việc.
          </Alert>
        )}

        {loading && <MySpinner />}
      </div>
    </div>
  );
};

export default DoctorSchedule;
