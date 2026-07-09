package com.ttkp.controllers;

import com.ttkp.pojo.Notification;
import com.ttkp.services.NotificationService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
@CrossOrigin
public class ApiNotificationController {

    @Autowired
    private NotificationService notificationService;

    @GetMapping("/notifications/user/{userId}")
    public ResponseEntity<List<Notification>> listByUser(
            @PathVariable("userId") int userId) {
        return new ResponseEntity<>(
                this.notificationService.getNotificationsByUserId(userId),
                HttpStatus.OK
        );
    }
}