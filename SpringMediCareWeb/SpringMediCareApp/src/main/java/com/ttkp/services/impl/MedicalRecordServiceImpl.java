package com.ttkp.services.impl;

import com.ttkp.pojo.Appointment;
import com.ttkp.pojo.MedicalRecord;
import com.ttkp.repositories.MedicalRecordRepository;
import com.ttkp.services.AppointmentService;
import com.ttkp.services.MedicalRecordService;
import java.util.Date;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.ttkp.pojo.Notification;
import com.ttkp.services.NotificationService;

@Service
@Transactional
public class MedicalRecordServiceImpl implements MedicalRecordService {

    @Autowired
    private MedicalRecordRepository medicalRecordRepo;

    @Autowired
    private AppointmentService appointmentService;

    @Autowired
    private NotificationService notificationService;

    @Override
    public List<MedicalRecord> getMedicalRecordsByPatientId(int patientId) {
        return this.medicalRecordRepo.getMedicalRecordsByPatientId(patientId);
    }

    @Override
    public MedicalRecord getMedicalRecordById(int id) {
        return this.medicalRecordRepo.getMedicalRecordById(id);
    }

    @Override
    public MedicalRecord getMedicalRecordByAppointmentId(int appointmentId) {
        return this.medicalRecordRepo
                .getMedicalRecordByAppointmentId(appointmentId);
    }

    @Override
    public boolean addMedicalRecord(int appointmentId,
            String diagnosis, String treatment) {

        Appointment appointment
                = this.appointmentService.getAppointmentById(appointmentId);

        if (appointment == null) {
            return false;
        }

        if (!"confirmed".equals(appointment.getStatus())) {
            return false;
        }

        MedicalRecord existingMedicalRecord
                = this.medicalRecordRepo
                        .getMedicalRecordByAppointmentId(appointmentId);

        if (existingMedicalRecord != null) {
            return false;
        }

        MedicalRecord medicalRecord = new MedicalRecord();

        medicalRecord.setAppointmentId(appointment);
        medicalRecord.setPatientId(appointment.getPatientId());
        medicalRecord.setDoctorId(appointment.getDoctorId());
        medicalRecord.setDiagnosis(diagnosis);
        medicalRecord.setTreatment(treatment);
        medicalRecord.setCreatedDate(new Date());

        this.medicalRecordRepo.addOrUpdateMedicalRecord(medicalRecord);

        this.medicalRecordRepo.addOrUpdateMedicalRecord(medicalRecord);

        boolean completed = this.appointmentService
                .updateAppointmentStatus(appointmentId, "completed");

        if (!completed) {
            return false;
        }

        Notification notification = new Notification();

        notification.setUserId(
                appointment.getPatientId().getUserId()
        );

        String message = String.format(
                "Ket qua kham cua ban da duoc bac si %s cap nhat",
                appointment.getDoctorId().getFullName()
        );

        notification.setMessage(message);
        notification.setIsRead(false);
        notification.setCreatedDate(new Date());

        this.notificationService.addNotification(notification);

        return true;
    }

    @Override
    public boolean updateMedicalRecord(int id,
            String diagnosis, String treatment) {

        MedicalRecord medicalRecord
                = this.medicalRecordRepo.getMedicalRecordById(id);

        if (medicalRecord == null) {
            return false;
        }

        medicalRecord.setDiagnosis(diagnosis);
        medicalRecord.setTreatment(treatment);

        this.medicalRecordRepo.addOrUpdateMedicalRecord(medicalRecord);

        return true;
    }
}
