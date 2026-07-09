package com.ttkp.services.impl;

import com.ttkp.pojo.Doctor;
import com.ttkp.repositories.DoctorRepository;
import com.ttkp.services.DoctorService;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class DoctorServiceImpl implements DoctorService {

    @Autowired
    private DoctorRepository doctorRepository;

    @Override
    public List<Doctor> getDoctors(Map<String, String> params) {
        return this.doctorRepository.getDoctors(params);
    }

    @Override
    public List<Doctor> getAllDoctors() {
        return this.doctorRepository.getAllDoctors();
    }

    @Override
    public Doctor getDoctorById(int id) {
        return this.doctorRepository.getDoctorById(id);
    }

    @Override
    public Doctor getDoctorByUserId(int userId) {
        return this.doctorRepository.getDoctorByUserId(userId);
    }
}
