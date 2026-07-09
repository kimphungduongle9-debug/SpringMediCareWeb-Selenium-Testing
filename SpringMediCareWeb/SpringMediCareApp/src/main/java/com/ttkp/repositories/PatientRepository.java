package com.ttkp.repositories;

import com.ttkp.pojo.Patient;

public interface PatientRepository {

    Patient getPatientById(int id);

    Patient getPatientByUserId(int userId);
}
