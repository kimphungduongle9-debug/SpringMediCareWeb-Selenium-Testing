package com.ttkp.repositories.impl;

import com.ttkp.pojo.Notification;
import com.ttkp.repositories.NotificationRepository;
import java.util.List;
import org.hibernate.Session;
import org.hibernate.query.Query;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.orm.hibernate5.LocalSessionFactoryBean;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

@Repository
@Transactional
public class NotificationRepositoryImpl implements NotificationRepository {

    @Autowired
    private LocalSessionFactoryBean factory;

    @Override
    public List<Notification> getNotificationsByUserId(int userId) {
        Session session = this.factory.getObject().getCurrentSession();
        Query q = session.createNamedQuery("Notification.findByUserId", Notification.class);
        q.setParameter("userId", userId);

        return q.getResultList();
    }

    @Override
    public Notification addNotification(Notification notification) {
        Session session = this.factory.getObject().getCurrentSession();
        session.persist(notification);

        return notification;
    }
}
