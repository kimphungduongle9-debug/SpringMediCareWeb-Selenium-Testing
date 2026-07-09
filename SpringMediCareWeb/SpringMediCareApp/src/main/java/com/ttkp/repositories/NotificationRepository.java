package com.ttkp.repositories;

import com.ttkp.pojo.Notification;
import java.util.List;

public interface NotificationRepository {

    List<Notification> getNotificationsByUserId(int userId);

    Notification addNotification(Notification notification);
}
