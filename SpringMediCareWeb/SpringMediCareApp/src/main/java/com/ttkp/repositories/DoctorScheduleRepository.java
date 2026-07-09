package com.ttkp.repositories;

import com.ttkp.pojo.DoctorSchedule;
import java.util.List;

public interface DoctorScheduleRepository {

    List<DoctorSchedule> getSchedules();

    List<DoctorSchedule> getSchedulesByDoctorId(int doctorId);

    DoctorSchedule getScheduleById(int id);
    
    boolean isDoctorAvailable(int doctorId, java.util.Date appointmentDate);

    void addOrUpdateSchedule(DoctorSchedule schedule);

    void deleteSchedule(int id);
    
    
}