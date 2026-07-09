package com.ttkp.repositories.impl;

import com.ttkp.pojo.Drug;
import com.ttkp.pojo.MedicalRecord;
import com.ttkp.pojo.Prescription;
import com.ttkp.pojo.PrescriptionDetail;
import com.ttkp.pojo.PrescriptionItem;
import com.ttkp.repositories.DrugRepository;
import com.ttkp.repositories.MedicalRecordRepository;
import com.ttkp.repositories.PrescriptionRepository;
import java.util.Date;
import java.util.List;
import org.hibernate.Session;
import jakarta.persistence.Query;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.orm.hibernate5.LocalSessionFactoryBean;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;
import java.util.HashMap;
import java.util.Map;
import com.ttkp.pojo.Notification;

@Repository
@Transactional
public class PrescriptionRepositoryImpl implements PrescriptionRepository {

    @Autowired
    private LocalSessionFactoryBean factory;

    @Autowired
    private MedicalRecordRepository medicalRecordRepo;

    @Autowired
    private DrugRepository drugRepo;

    @Override
    public List<Prescription> getPrescriptionsByRecordId(int recordId) {
        Session session = this.factory.getObject().getCurrentSession();

        Query query = session.createNamedQuery(
                "Prescription.findByRecordId",
                Prescription.class
        );

        query.setParameter("recordId", recordId);

        return query.getResultList();
    }

    @Override
    public List<PrescriptionDetail> getPrescriptionDetailsByPrescriptionId(
            int prescriptionId) {

        Session session = this.factory.getObject().getCurrentSession();

        Query query = session.createNamedQuery(
                "PrescriptionDetail.findByPrescriptionId",
                PrescriptionDetail.class
        );

        query.setParameter("prescriptionId", prescriptionId);

        return query.getResultList();
    }

    @Override
    public boolean addPrescription(int recordId,
            List<PrescriptionItem> items) {

        Session session = this.factory.getObject().getCurrentSession();

        MedicalRecord medicalRecord
                = this.medicalRecordRepo.getMedicalRecordById(recordId);

        if (medicalRecord == null || items == null || items.isEmpty()) {
            return false;
        }

        Map<Integer, Integer> quantities = new HashMap<>();

        for (PrescriptionItem item : items) {
            if (item.getId() == null || item.getQuantity() <= 0) {
                return false;
            }

            int totalQuantity = quantities.getOrDefault(item.getId(), 0)
                    + item.getQuantity();

            quantities.put(item.getId(), totalQuantity);
        }

        for (Map.Entry<Integer, Integer> entry : quantities.entrySet()) {
            Drug drug = this.drugRepo.getDrugById(entry.getKey());

            if (drug == null || drug.getQuantity() < entry.getValue()) {
                return false;
            }
        }

        Prescription prescription = new Prescription();

        prescription.setRecordId(medicalRecord);
        prescription.setDoctorId(medicalRecord.getDoctorId());
        prescription.setPatientId(medicalRecord.getPatientId());
        prescription.setCreatedDate(new Date());

        session.persist(prescription);

        for (PrescriptionItem item : items) {
            Drug drug = this.drugRepo.getDrugById(item.getId());

            PrescriptionDetail detail = new PrescriptionDetail();

            detail.setPrescriptionId(prescription);
            detail.setDrugId(drug);
            detail.setQuantity(item.getQuantity());
            detail.setDosage(item.getDosage());

            session.persist(detail);

            drug.setQuantity(
                    drug.getQuantity() - item.getQuantity()
            );

            session.merge(drug);
        }
        Notification notification = new Notification();
        notification.setUserId(medicalRecord.getPatientId().getUserId());
        String message = String.format(
                "Ban co don thuoc moi #%d trong ho so kham benh #%d",
                prescription.getPrescriptionId(),
                medicalRecord.getRecordId()
        );

        notification.setMessage(message);
        notification.setIsRead(false);
        notification.setCreatedDate(new Date());

        session.persist(notification);
        return true;
    }
}
