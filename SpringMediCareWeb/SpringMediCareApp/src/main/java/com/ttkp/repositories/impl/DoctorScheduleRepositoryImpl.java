package com.ttkp.repositories.impl;

import com.ttkp.pojo.DoctorSchedule;
import com.ttkp.repositories.DoctorScheduleRepository;
import org.hibernate.query.Query;
import jakarta.persistence.criteria.CriteriaBuilder;
import jakarta.persistence.criteria.CriteriaQuery;
import jakarta.persistence.criteria.Root;
import java.util.List;
import org.hibernate.Session;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.orm.hibernate5.LocalSessionFactoryBean;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;
import java.util.Date;

@Repository
@Transactional
public class DoctorScheduleRepositoryImpl implements DoctorScheduleRepository {

    @Autowired
    private LocalSessionFactoryBean factory;

    @Override
    public List<DoctorSchedule> getSchedules() {
        Session s = this.factory.getObject().getCurrentSession();

        CriteriaBuilder b = s.getCriteriaBuilder();
        CriteriaQuery<DoctorSchedule> q = b.createQuery(DoctorSchedule.class);
        Root root = q.from(DoctorSchedule.class);

        q.select(root);
        q.orderBy(b.desc(root.get("scheduleId")));

        Query query = s.createQuery(q);

        return query.getResultList();
    }

    @Override
    public List<DoctorSchedule> getSchedulesByDoctorId(int doctorId) {
        Session s = this.factory.getObject().getCurrentSession();

        CriteriaBuilder b = s.getCriteriaBuilder();
        CriteriaQuery<DoctorSchedule> q = b.createQuery(DoctorSchedule.class);
        Root root = q.from(DoctorSchedule.class);

        q.select(root);
        q.where(b.equal(root.get("doctorId").get("doctorId"), doctorId));
        q.orderBy(b.asc(root.get("workDate")), b.asc(root.get("startTime")));

        Query query = s.createQuery(q);

        return query.getResultList();
    }

    @Override
    public boolean isDoctorAvailable(int doctorId, Date appointmentDate) {
        Session s = this.factory.getObject().getCurrentSession();

        java.sql.Date workDate = new java.sql.Date(appointmentDate.getTime());
        java.sql.Time appointmentTime = new java.sql.Time(appointmentDate.getTime());

        CriteriaBuilder b = s.getCriteriaBuilder();
        CriteriaQuery<DoctorSchedule> q = b.createQuery(DoctorSchedule.class);
        Root root = q.from(DoctorSchedule.class);

        q.select(root);
        q.where(
                b.and(
                        b.equal(root.get("doctorId").get("doctorId"), doctorId),
                        b.equal(root.get("workDate"), workDate),
                        b.equal(root.get("status"), "available"),
                        b.lessThanOrEqualTo(root.get("startTime"), appointmentTime),
                        b.greaterThan(root.get("endTime"), appointmentTime)
                )
        );

        Query query = s.createQuery(q);

        return !query.getResultList().isEmpty();
    }

    @Override
    public DoctorSchedule getScheduleById(int id) {
        Session s = this.factory.getObject().getCurrentSession();
        return s.get(DoctorSchedule.class, id);
    }

    @Override
    public void addOrUpdateSchedule(DoctorSchedule schedule) {
        Session s = this.factory.getObject().getCurrentSession();

        if (schedule.getScheduleId() == null) {
            s.persist(schedule);
        } else {
            s.merge(schedule);
        }
    }

    @Override
    public void deleteSchedule(int id) {
        Session s = this.factory.getObject().getCurrentSession();

        DoctorSchedule schedule = this.getScheduleById(id);
        s.remove(schedule);
    }
}
