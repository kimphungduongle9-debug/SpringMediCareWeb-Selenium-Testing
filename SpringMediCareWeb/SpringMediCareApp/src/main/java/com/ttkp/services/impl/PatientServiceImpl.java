package com.ttkp.services.impl;

import com.ttkp.pojo.Patient;
import com.ttkp.repositories.PatientRepository;
import com.ttkp.services.PatientService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class PatientServiceImpl implements PatientService {

    @Autowired
    private PatientRepository patientRepo;

    @Override
    public Patient getPatientById(int id) {
        return this.patientRepo.getPatientById(id);
    }

    @Override
    public Patient getPatientByUserId(int userId) {
        return this.patientRepo.getPatientByUserId(userId);
    }
}
