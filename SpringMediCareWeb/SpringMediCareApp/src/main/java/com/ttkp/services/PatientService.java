package com.ttkp.services;

import com.ttkp.pojo.Patient;

public interface PatientService {

    Patient getPatientById(int id);

    Patient getPatientByUserId(int userId);
}
