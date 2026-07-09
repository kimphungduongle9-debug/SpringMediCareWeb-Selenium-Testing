package com.ttkp.services;

import com.ttkp.pojo.Specialty;
import java.util.List;
import java.util.Map;

public interface SpecialtyService {
    List<Specialty> getSpecialties(Map<String, String> params);
    Specialty getSpecialtyById(int id);
}