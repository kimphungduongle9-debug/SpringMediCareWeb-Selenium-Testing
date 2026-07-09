package com.ttkp.services.impl;

import com.ttkp.pojo.DoctorSchedule;
import com.ttkp.repositories.DoctorScheduleRepository;
import com.ttkp.services.DoctorScheduleService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.Date;
@Service
public class DoctorScheduleServiceImpl implements DoctorScheduleService {

    @Autowired
    private DoctorScheduleRepository doctorScheduleRepo;

    @Override
    public List<DoctorSchedule> getSchedules() {
        return this.doctorScheduleRepo.getSchedules();
    }

    @Override
    public List<DoctorSchedule> getSchedulesByDoctorId(int doctorId) {
        return this.doctorScheduleRepo.getSchedulesByDoctorId(doctorId);
    }

    @Override
    public DoctorSchedule getScheduleById(int id) {
        return this.doctorScheduleRepo.getScheduleById(id);
    }

    @Override
    public void addOrUpdateSchedule(DoctorSchedule schedule) {
        this.doctorScheduleRepo.addOrUpdateSchedule(schedule);
    }

    @Override
    public void deleteSchedule(int id) {
        this.doctorScheduleRepo.deleteSchedule(id);
    }

    @Override
    public boolean isDoctorAvailable(int doctorId, java.util.Date appointmentDate) {
        return this.doctorScheduleRepo.isDoctorAvailable(doctorId, appointmentDate);
    }
}
