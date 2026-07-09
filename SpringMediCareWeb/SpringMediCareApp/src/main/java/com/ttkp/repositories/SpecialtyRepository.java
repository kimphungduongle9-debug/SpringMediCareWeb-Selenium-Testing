package com.ttkp.repositories;

import com.ttkp.pojo.Specialty;
import java.util.List;
import java.util.Map;

public interface SpecialtyRepository {

    List<Specialty> getSpecialties(Map<String, String> params);
    Specialty getSpecialtyById(int id);
}
