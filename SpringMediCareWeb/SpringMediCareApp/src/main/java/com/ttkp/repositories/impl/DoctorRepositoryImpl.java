package com.ttkp.repositories.impl;

import com.ttkp.pojo.Doctor;
import com.ttkp.repositories.DoctorRepository;
import jakarta.persistence.criteria.CriteriaBuilder;
import jakarta.persistence.criteria.CriteriaQuery;
import jakarta.persistence.criteria.Predicate;
import jakarta.persistence.criteria.Root;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import org.hibernate.Session;
import org.hibernate.query.Query;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.PropertySource;
import org.springframework.core.env.Environment;
import org.springframework.orm.hibernate5.LocalSessionFactoryBean;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

@Repository
@Transactional
@PropertySource("classpath:configs.properties")
public class DoctorRepositoryImpl implements DoctorRepository {

    @Autowired
    private LocalSessionFactoryBean factory;

    @Autowired
    private Environment env;

    @Override
    public List<Doctor> getDoctors(Map<String, String> params) {
        Session session = this.factory.getObject().getCurrentSession();
        CriteriaBuilder b = session.getCriteriaBuilder();
        CriteriaQuery<Doctor> q = b.createQuery(Doctor.class);
        Root root = q.from(Doctor.class);
        q.select(root);

        if (params != null && !params.isEmpty()) {
            List<Predicate> predicates = new ArrayList<>();

            String kw = params.get("kw");
            if (kw != null && !kw.isEmpty()) {
                predicates.add(b.like(root.get("fullName"), String.format("%%%s%%", kw.trim())));
            }

            String specialtyId = params.get("specialtyId");
            if (specialtyId != null && !specialtyId.isEmpty()) {
                predicates.add(b.equal(root.get("specialtyId").get("specialtyId").as(Integer.class), Integer.parseInt(specialtyId)));
            }

            if (!predicates.isEmpty()) {
                q.where(predicates.toArray(Predicate[]::new));
            }
        }

        q.orderBy(b.desc(root.get("doctorId")));

        Query query = session.createQuery(q);

        if (params != null) {

            int pageSize = this.env.getProperty("doctors.pageSize", Integer.class);

            int page = Integer.parseInt(params.getOrDefault("page", "1"));
            int start = (page - 1) * pageSize;

            query.setMaxResults(pageSize);
            query.setFirstResult(start);
        }

        return query.getResultList();
    }

    @Override
    public List<Doctor> getAllDoctors() {
        Session session = this.factory.getObject().getCurrentSession();
        CriteriaBuilder b = session.getCriteriaBuilder();
        CriteriaQuery<Doctor> q = b.createQuery(Doctor.class);
        Root root = q.from(Doctor.class);

        q.select(root);
        q.orderBy(b.desc(root.get("doctorId")));

        Query query = session.createQuery(q);

        return query.getResultList();
    }

    @Override
    public Doctor getDoctorById(int id) {
        Session session = this.factory.getObject().getCurrentSession();
        return session.get(Doctor.class, id);
    }

    @Override
    public Doctor getDoctorByUserId(int userId) {
        Session session = this.factory.getObject().getCurrentSession();

        CriteriaBuilder b = session.getCriteriaBuilder();
        CriteriaQuery<Doctor> q = b.createQuery(Doctor.class);
        Root root = q.from(Doctor.class);

        q.select(root);
        q.where(b.equal(root.get("userId").get("id"), userId));

        Query query = session.createQuery(q);

        List<Doctor> doctors = query.getResultList();

        if (doctors.isEmpty()) {
            return null;
        }

        return doctors.get(0);
    }
}
