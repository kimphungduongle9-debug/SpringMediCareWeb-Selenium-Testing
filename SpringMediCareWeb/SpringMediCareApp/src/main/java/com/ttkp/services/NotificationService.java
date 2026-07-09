package com.ttkp.services;

import com.ttkp.pojo.Notification;
import java.util.List;

public interface NotificationService {

    List<Notification> getNotificationsByUserId(int userId);

    Notification addNotification(Notification notification);
}
