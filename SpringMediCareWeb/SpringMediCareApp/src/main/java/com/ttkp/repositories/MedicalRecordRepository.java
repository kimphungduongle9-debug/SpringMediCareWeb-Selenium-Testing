package com.ttkp.repositories;

import com.ttkp.pojo.MedicalRecord;
import java.util.List;

public interface MedicalRecordRepository {

    List<MedicalRecord> getMedicalRecordsByPatientId(int patientId);

    MedicalRecord getMedicalRecordById(int id);
    
    MedicalRecord getMedicalRecordByAppointmentId(int appointmentId);

    void addOrUpdateMedicalRecord(MedicalRecord medicalRecord);
}