import { useContext, useEffect, useState } from "react";
import { Alert } from "react-bootstrap";
import Apis, { endpoints } from "../../configs/Apis";
import MySpinner from "../../components/MySpinner";
import { MyUserContext } from "../../configs/Contexts";
import NotificationItem from "../../components/NotificationItem";

const PatientNotification = () => {
  const [user] = useContext(MyUserContext);
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  const [msg, setMsg] = useState("");

  const isPatient = user !== null && user.role === "patient";

  const loadNotifications = async () => {
    let res = await Apis.get(endpoints.notificationsByUser(user.id));
    setNotifications(res.data);
  };

  useEffect(() => {
    if (user !== null && isPatient) {
      setLoading(true);

      loadNotifications()
        .catch((err) => {
          console.error(err);
          setMsg("Không tải được danh sách thông báo.");
        })
        .finally(() => setLoading(false));
    }
  }, [user]);

  if (user === null) {
    return (
      <div className="main-content">
        <div className="container">
          <Alert variant="warning">Vui lòng đăng nhập để xem thông báo.</Alert>
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

  return (
    <div className="main-content">
      <div className="container">
        <div className="section-box">
          <h2>Thông báo của tôi</h2>
          <p>Theo dõi các thông báo mới từ phòng khám.</p>
        </div>

        {msg && <Alert variant="info">{msg}</Alert>}

        <div className="feature-card">
          {notifications.map((notification) => (
            <NotificationItem
              key={notification.notificationId}
              notification={notification}
            />
          ))}

          {notifications.length === 0 && !loading && (
            <Alert variant="info">Bạn chưa có thông báo nào.</Alert>
          )}
        </div>

        {loading && <MySpinner />}
      </div>
    </div>
  );
};

export default PatientNotification;
