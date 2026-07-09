package com.ttkp.services;

import com.ttkp.pojo.MedicalRecord;
import java.util.List;

public interface MedicalRecordService {

    List<MedicalRecord> getMedicalRecordsByPatientId(int patientId);

    MedicalRecord getMedicalRecordById(int id);

    MedicalRecord getMedicalRecordByAppointmentId(int appointmentId);

    boolean addMedicalRecord(int appointmentId,
            String diagnosis, String treatment);

    boolean updateMedicalRecord(int id,
            String diagnosis, String treatment);
}
