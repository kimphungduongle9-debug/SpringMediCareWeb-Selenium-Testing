package com.ttkp.repositories.impl;

import com.ttkp.pojo.MedicalRecord;
import com.ttkp.repositories.MedicalRecordRepository;
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

@Repository
@Transactional
public class MedicalRecordRepositoryImpl implements MedicalRecordRepository {

    @Autowired
    private LocalSessionFactoryBean factory;

    @Override
    public List<MedicalRecord> getMedicalRecordsByPatientId(int patientId) {
        Session session = this.factory.getObject().getCurrentSession();

        CriteriaBuilder b = session.getCriteriaBuilder();
        CriteriaQuery<MedicalRecord> q = b.createQuery(MedicalRecord.class);
        Root root = q.from(MedicalRecord.class);

        q.select(root);
        q.where(b.equal(root.get("patientId").get("patientId"), patientId));
        q.orderBy(b.desc(root.get("createdDate")));

        Query query = session.createQuery(q);

        return query.getResultList();
    }

    @Override
    public MedicalRecord getMedicalRecordById(int id) {
        Session session = this.factory.getObject().getCurrentSession();
        return session.get(MedicalRecord.class, id);
    }

    @Override
    public MedicalRecord getMedicalRecordByAppointmentId(int appointmentId) {
        Session session = this.factory.getObject().getCurrentSession();

        CriteriaBuilder b = session.getCriteriaBuilder();
        CriteriaQuery<MedicalRecord> q = b.createQuery(MedicalRecord.class);
        Root root = q.from(MedicalRecord.class);

        q.select(root);
        q.where(
                b.equal(
                        root.get("appointmentId").get("appointmentId"),
                        appointmentId
                )
        );

        Query query = session.createQuery(q);
        List<MedicalRecord> medicalRecords = query.getResultList();

        if (medicalRecords.isEmpty()) {
            return null;
        }

        return medicalRecords.get(0);
    }

    @Override
    public void addOrUpdateMedicalRecord(MedicalRecord medicalRecord) {
        Session session = this.factory.getObject().getCurrentSession();

        if (medicalRecord.getRecordId() == null) {
            session.persist(medicalRecord);
        } else {
            session.merge(medicalRecord);
        }
    }
}
