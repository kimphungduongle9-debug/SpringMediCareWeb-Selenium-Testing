package com.ttkp.repositories;

import com.ttkp.pojo.Appointment;
import java.util.Date;
import java.util.List;

public interface AppointmentRepository {

    boolean addAppointment(Appointment appointment);

    List<Appointment> getAppointments();

    List<Appointment> getAppointmentsByPatientId(int patientId);
    
    List<Appointment> getAppointmentsByDoctorId(int doctorId);

    Appointment getAppointmentById(int id);

    boolean updateAppointmentStatus(int id, String status);
    
    boolean confirmAppointment(int id);

    boolean isAppointmentTimeBooked(int doctorId, Date appointmentDate);
}
