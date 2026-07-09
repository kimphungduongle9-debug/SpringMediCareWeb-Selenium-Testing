package com.ttkp.repositories.impl;

import com.ttkp.pojo.Patient;
import com.ttkp.repositories.StatisticsRepository;
import jakarta.persistence.criteria.CriteriaBuilder;
import jakarta.persistence.criteria.CriteriaQuery;
import jakarta.persistence.criteria.Root;
import java.util.List;
import org.hibernate.Session;
import org.hibernate.query.Query;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.orm.hibernate5.LocalSessionFactoryBean;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;
import jakarta.persistence.criteria.Predicate;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;
import com.ttkp.pojo.Doctor;
import com.ttkp.pojo.MedicalRecord;
import com.ttkp.pojo.Specialty;
import jakarta.persistence.criteria.Join;
import jakarta.persistence.criteria.JoinType;
import com.ttkp.pojo.Payment;
import java.math.BigDecimal;

@Repository
@Transactional
public class StatisticsRepositoryImpl implements StatisticsRepository {

    @Autowired
    private LocalSessionFactoryBean factory;

    @Override
    public List<Object[]> countPatientsByGender() {
        Session session = this.factory.getObject().getCurrentSession();

        CriteriaBuilder b = session.getCriteriaBuilder();
        CriteriaQuery<Object[]> q = b.createQuery(Object[].class);

        Root root = q.from(Patient.class);

        q.multiselect(root.get("gender"), b.count(root));
        q.groupBy(root.get("gender"));

        Query query = session.createQuery(q);
        return query.getResultList();
    }

    @Override
    public List<Object[]> countPatientsByAgeGroup() {
        Session session = this.factory.getObject().getCurrentSession();

        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.HOUR_OF_DAY, 0);
        cal.set(Calendar.MINUTE, 0);
        cal.set(Calendar.SECOND, 0);
        cal.set(Calendar.MILLISECOND, 0);

        cal.add(Calendar.YEAR, -18);
        Date eighteenYearsAgo = cal.getTime();

        cal = Calendar.getInstance();
        cal.set(Calendar.HOUR_OF_DAY, 0);
        cal.set(Calendar.MINUTE, 0);
        cal.set(Calendar.SECOND, 0);
        cal.set(Calendar.MILLISECOND, 0);
        cal.add(Calendar.YEAR, -31);
        Date thirtyOneYearsAgo = cal.getTime();

        cal = Calendar.getInstance();
        cal.set(Calendar.HOUR_OF_DAY, 0);
        cal.set(Calendar.MINUTE, 0);
        cal.set(Calendar.SECOND, 0);
        cal.set(Calendar.MILLISECOND, 0);
        cal.add(Calendar.YEAR, -46);
        Date fortySixYearsAgo = cal.getTime();

        List<Object[]> results = new ArrayList<>();

        results.add(new Object[]{
            "Dưới 18",
            this.countPatientsByDateOfBirth(session, eighteenYearsAgo, null)
        });

        results.add(new Object[]{
            "18 - 30",
            this.countPatientsByDateOfBirth(session, thirtyOneYearsAgo, eighteenYearsAgo)
        });

        results.add(new Object[]{
            "31 - 45",
            this.countPatientsByDateOfBirth(session, fortySixYearsAgo, thirtyOneYearsAgo)
        });

        results.add(new Object[]{
            "Trên 45",
            this.countPatientsByDateOfBirth(session, null, fortySixYearsAgo)
        });

        return results;
    }

    private Long countPatientsByDateOfBirth(Session session, Date minDate, Date maxDate) {
        CriteriaBuilder b = session.getCriteriaBuilder();
        CriteriaQuery<Long> q = b.createQuery(Long.class);

        Root root = q.from(Patient.class);

        List<Predicate> predicates = new ArrayList<>();
        predicates.add(b.isNotNull(root.get("dateOfBirth")));

        if (minDate != null) {
            predicates.add(
                    b.greaterThan(root.<Date>get("dateOfBirth"), minDate)
            );
        }

        if (maxDate != null) {
            predicates.add(
                    b.lessThanOrEqualTo(root.<Date>get("dateOfBirth"), maxDate)
            );
        }

        q.select(b.count(root));
        q.where(predicates.toArray(new Predicate[0]));

        Query query = session.createQuery(q);
        return (Long) query.getSingleResult();
    }

    @Override
    public List<Object[]> countPatientsBySpecialty() {
        Session session = this.factory.getObject().getCurrentSession();

        CriteriaBuilder b = session.getCriteriaBuilder();
        CriteriaQuery<Object[]> q = b.createQuery(Object[].class);

        Root root = q.from(MedicalRecord.class);
        Join<MedicalRecord, Doctor> doctorJoin = root.join("doctorId", JoinType.INNER);
        Join<Doctor, Specialty> specialtyJoin = doctorJoin.join("specialtyId", JoinType.INNER);

        q.multiselect(
                specialtyJoin.get("name"),
                b.countDistinct(root.get("patientId").get("patientId"))
        );

        q.groupBy(
                specialtyJoin.get("specialtyId"),
                specialtyJoin.get("name")
        );

        Query query = session.createQuery(q);
        return query.getResultList();
    }

    @Override
    public List<Object[]> countPatientsByDiagnosis() {
        Session session = this.factory.getObject().getCurrentSession();

        CriteriaBuilder b = session.getCriteriaBuilder();
        CriteriaQuery<Object[]> q = b.createQuery(Object[].class);

        Root root = q.from(MedicalRecord.class);

        q.multiselect(
                root.get("diagnosis"),
                b.countDistinct(root.get("patientId").get("patientId"))
        );

        q.where(b.isNotNull(root.get("diagnosis")));
        q.groupBy(root.get("diagnosis"));

        Query query = session.createQuery(q);
        return query.getResultList();
    }

    @Override
    public BigDecimal getTotalRevenue() {
        Session session = this.factory.getObject().getCurrentSession();

        CriteriaBuilder b = session.getCriteriaBuilder();
        CriteriaQuery<BigDecimal> q = b.createQuery(BigDecimal.class);

        Root root = q.from(Payment.class);

        q.select(b.sum(root.<BigDecimal>get("amount")));
        q.where(b.equal(root.get("status"), "paid"));

        Query query = session.createQuery(q);
        BigDecimal total = (BigDecimal) query.getSingleResult();

        return total != null ? total : BigDecimal.ZERO;
    }

    @Override
    public List<Object[]> getRevenueByMonth(int year) {
        Session session = this.factory.getObject().getCurrentSession();

        CriteriaBuilder b = session.getCriteriaBuilder();
        CriteriaQuery<Object[]> q = b.createQuery(Object[].class);

        Root root = q.from(Payment.class);

        q.multiselect(
                b.function("MONTH", Integer.class, root.get("createdDate")),
                b.sum(root.<BigDecimal>get("amount"))
        );

        q.where(
                b.equal(root.get("status"), "paid"),
                b.equal(
                        b.function("YEAR", Integer.class, root.get("createdDate")),
                        year
                )
        );

        q.groupBy(
                b.function("MONTH", Integer.class, root.get("createdDate"))
        );

        Query query = session.createQuery(q);
        return query.getResultList();
    }

}
