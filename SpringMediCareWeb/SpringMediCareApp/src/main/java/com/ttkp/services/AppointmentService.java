package com.ttkp.services;

import com.ttkp.pojo.Appointment;
import java.util.List;

public interface AppointmentService {

    String addAppointment(int patientId,int doctorId,String appointmentDate,String notes);

    List<Appointment> getAppointmentsByPatientId(int patientId);

    List<Appointment> getAppointmentsByDoctorId(int doctorId);

    List<Appointment> getAppointments();

    Appointment getAppointmentById(int id);

    boolean cancelAppointment(int id);

    boolean confirmAppointment(int id);

    boolean updateAppointmentStatus(int id, String status);
}
