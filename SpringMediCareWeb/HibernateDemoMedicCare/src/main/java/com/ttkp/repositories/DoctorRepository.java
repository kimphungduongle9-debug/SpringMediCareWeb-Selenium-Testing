package com.ttkp.repositories;

import com.ttkp.pojo.Doctor;
import java.util.List;

public interface DoctorRepository {
    List<Doctor> getDoctors();
    Doctor getDoctorById(int id);
}