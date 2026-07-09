package com.ttkp.services;

import com.ttkp.pojo.DoctorSchedule;
import java.util.List;

public interface DoctorScheduleService {

    List<DoctorSchedule> getSchedules();

    List<DoctorSchedule> getSchedulesByDoctorId(int doctorId);

    DoctorSchedule getScheduleById(int id);

    void addOrUpdateSchedule(DoctorSchedule schedule);

    void deleteSchedule(int id);
    
    boolean isDoctorAvailable(int doctorId, java.util.Date appointmentDate);
}
