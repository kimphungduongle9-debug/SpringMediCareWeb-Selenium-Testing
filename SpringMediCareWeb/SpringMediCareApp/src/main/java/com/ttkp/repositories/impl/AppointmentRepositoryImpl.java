package com.ttkp.repositories.impl;

import com.ttkp.pojo.Appointment;
import com.ttkp.repositories.AppointmentRepository;
import jakarta.persistence.criteria.CriteriaBuilder;
import jakarta.persistence.criteria.CriteriaQuery;
import jakarta.persistence.criteria.Root;
import java.util.Date;
import java.util.List;
import org.hibernate.Session;
import org.hibernate.query.Query;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.orm.hibernate5.LocalSessionFactoryBean;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;
import com.ttkp.pojo.Notification;
import java.text.SimpleDateFormat;

@Repository
@Transactional
public class AppointmentRepositoryImpl implements AppointmentRepository {

    @Autowired
    private LocalSessionFactoryBean factory;

    @Override
    public boolean addAppointment(Appointment appointment) {
        Session session = this.factory.getObject().getCurrentSession();
        session.persist(appointment);

        return true;
    }

    @Override
    public List<Appointment> getAppointments() {
        Session session = this.factory.getObject().getCurrentSession();

        CriteriaBuilder b = session.getCriteriaBuilder();
        CriteriaQuery<Appointment> q = b.createQuery(Appointment.class);
        Root root = q.from(Appointment.class);

        q.select(root);
        q.orderBy(b.desc(root.get("appointmentId")));

        Query query = session.createQuery(q);

        return query.getResultList();
    }

    @Override
    public List<Appointment> getAppointmentsByPatientId(int patientId) {
        Session session = this.factory.getObject().getCurrentSession();

        CriteriaBuilder b = session.getCriteriaBuilder();
        CriteriaQuery<Appointment> q = b.createQuery(Appointment.class);
        Root root = q.from(Appointment.class);

        q.select(root);
        q.where(b.equal(root.get("patientId").get("patientId"), patientId));
        q.orderBy(b.desc(root.get("appointmentDate")));

        Query query = session.createQuery(q);

        return query.getResultList();
    }

    @Override
    public List<Appointment> getAppointmentsByDoctorId(int doctorId) {
        Session session = this.factory.getObject().getCurrentSession();

        CriteriaBuilder b = session.getCriteriaBuilder();
        CriteriaQuery<Appointment> q = b.createQuery(Appointment.class);
        Root root = q.from(Appointment.class);

        q.select(root);
        q.where(b.equal(root.get("doctorId").get("doctorId"), doctorId));
        q.orderBy(b.desc(root.get("appointmentDate")));

        Query query = session.createQuery(q);

        return query.getResultList();
    }

    @Override
    public Appointment getAppointmentById(int id) {
        Session session = this.factory.getObject().getCurrentSession();
        return session.get(Appointment.class, id);
    }

    @Override
    public boolean isAppointmentTimeBooked(int doctorId, Date appointmentDate) {
        Session session = this.factory.getObject().getCurrentSession();

        // Mỗi lượt khám kéo dài 30 phút
        long appointmentDuration = 30 * 60 * 1000L;

        Date startTime = new Date(
                appointmentDate.getTime() - appointmentDuration
        );

        Date endTime = new Date(
                appointmentDate.getTime() + appointmentDuration
        );

        CriteriaBuilder b = session.getCriteriaBuilder();
        CriteriaQuery<Appointment> q = b.createQuery(Appointment.class);
        Root<Appointment> root = q.from(Appointment.class);

        q.select(root);

        q.where(
                b.and(
                        b.equal(
                                root.get("doctorId").get("doctorId"),
                                doctorId
                        ),
                        // Tìm lịch hẹn cách giờ mới ít hơn 30 phút
                        b.greaterThan(
                                root.<Date>get("appointmentDate"),
                                startTime
                        ),
                        b.lessThan(
                                root.<Date>get("appointmentDate"),
                                endTime
                        ),
                        // Lịch đã hủy không được tính là chiếm chỗ
                        b.notEqual(
                                root.get("status"),
                                "cancelled"
                        )
                )
        );

        Query<Appointment> query = session.createQuery(q);
        query.setMaxResults(1);

        return !query.getResultList().isEmpty();
    }

    @Override
    public boolean updateAppointmentStatus(int id, String status) {
        Session session = this.factory.getObject().getCurrentSession();

        Appointment a = session.get(Appointment.class, id);

        if (a == null) {
            return false;
        }

        a.setStatus(status);
        session.merge(a);

        return true;
    }

    @Override
    public boolean confirmAppointment(int id) {
        Session session = this.factory.getObject().getCurrentSession();

        Appointment a = session.get(Appointment.class, id);

        if (a == null) {
            return false;
        }

        if ("confirmed".equals(a.getStatus())) {
            return true;
        }

        a.setStatus("confirmed");
        session.merge(a);

        Notification n = new Notification();
        n.setUserId(a.getPatientId().getUserId());
        SimpleDateFormat formatter = new SimpleDateFormat("HH:mm dd/MM/yyyy");

        String message = String.format(
                "Lich hen #%d voi bac si %s vao %s da duoc xac nhan",
                a.getAppointmentId(),
                a.getDoctorId().getFullName(),
                formatter.format(a.getAppointmentDate())
        );

        n.setMessage(message);
        n.setIsRead(false);
        n.setCreatedDate(new Date());

        session.persist(n);

        return true;
    }
}
