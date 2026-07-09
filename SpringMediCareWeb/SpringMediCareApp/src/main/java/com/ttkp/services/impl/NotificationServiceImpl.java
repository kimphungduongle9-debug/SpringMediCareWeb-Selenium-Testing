package com.ttkp.services.impl;

import com.ttkp.pojo.Notification;
import com.ttkp.repositories.NotificationRepository;
import com.ttkp.services.NotificationService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class NotificationServiceImpl implements NotificationService {

    @Autowired
    private NotificationRepository notificationRepo;

    @Override
    public List<Notification> getNotificationsByUserId(int userId) {
        return this.notificationRepo.getNotificationsByUserId(userId);
    }

    @Override
    public Notification addNotification(Notification notification) {
        return this.notificationRepo.addNotification(notification);
    }
}
