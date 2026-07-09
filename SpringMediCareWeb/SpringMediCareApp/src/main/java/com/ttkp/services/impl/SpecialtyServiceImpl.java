package com.ttkp.services.impl;

import com.ttkp.pojo.Specialty;
import com.ttkp.repositories.SpecialtyRepository;
import com.ttkp.services.SpecialtyService;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class SpecialtyServiceImpl implements SpecialtyService {

    @Autowired
    private SpecialtyRepository specialtyRepository;

    @Override
    public List<Specialty> getSpecialties(Map<String, String> params) {
        return this.specialtyRepository.getSpecialties(params);
    }

    @Override
    public Specialty getSpecialtyById(int id) {
        return this.specialtyRepository.getSpecialtyById(id);
    }
}
