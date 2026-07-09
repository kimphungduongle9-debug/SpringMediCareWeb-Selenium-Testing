package com.ttkp.repositories;

import com.ttkp.pojo.Specialty;
import java.util.List;

public interface SpecialtyRepository {

    List<Specialty> getSpecialties();

    Specialty getSpecialtyById(int id);
}
