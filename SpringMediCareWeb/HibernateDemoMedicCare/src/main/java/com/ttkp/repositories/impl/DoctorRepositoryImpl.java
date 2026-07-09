package com.ttkp.repositories.impl;

import com.ttkp.hibernatedemomedicare.HibernateUtils;
import com.ttkp.pojo.Doctor;
import com.ttkp.repositories.DoctorRepository;
import java.util.List;
import org.hibernate.Session;

public class DoctorRepositoryImpl implements DoctorRepository {

    @Override
    public List<Doctor> getDoctors() {
        try (Session session = HibernateUtils.getFactory().openSession()) {
            return session.createNamedQuery("Doctor.findAll", Doctor.class).getResultList();
        }
    }

    @Override
    public Doctor getDoctorById(int id) {
        try (Session session = HibernateUtils.getFactory().openSession()) {
            return session.get(Doctor.class, id);
        }
    }
}