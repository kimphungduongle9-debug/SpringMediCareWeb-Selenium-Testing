package com.ttkp.repositories;

import com.ttkp.pojo.Doctor;
import java.util.List;
import java.util.Map;

public interface DoctorRepository {
    List<Doctor> getDoctors(Map<String, String> params);
    List<Doctor> getAllDoctors();
    Doctor getDoctorById(int id);
    Doctor getDoctorByUserId(int userId);
}