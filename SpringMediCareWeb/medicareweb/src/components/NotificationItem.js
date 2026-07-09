const NotificationItem = ({ notification }) => {
  const message = notification.message.toLowerCase();

  const getNotificationLabel = () => {
    if (message.includes("xet nghiem")) {
      return "[Kết quả xét nghiệm] ";
    }
    if (message.includes("don thuoc")) {
      return "[Đơn thuốc] ";
    }
    if (message.includes("lich hen")) {
      return "[Lịch hẹn] ";
    }

    return "[Thông báo] ";
  };

  return (
    <div
      className={`notification-item ${
        notification.isRead ? "" : "notification-unread"
      }`}
    >
      <p>
        <strong>{getNotificationLabel()}</strong>
        {notification.message}
      </p>

      <span>{new Date(notification.createdDate).toLocaleString("vi-VN")}</span>
    </div>
  );
};

export default NotificationItem;
