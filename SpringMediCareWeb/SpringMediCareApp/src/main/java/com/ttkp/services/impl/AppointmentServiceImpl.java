package com.ttkp.services.impl;

import com.ttkp.pojo.Appointment;
import com.ttkp.pojo.Doctor;
import com.ttkp.pojo.Patient;
import com.ttkp.services.PatientService;
import com.ttkp.repositories.AppointmentRepository;
import com.ttkp.repositories.DoctorRepository;
import com.ttkp.services.AppointmentService;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.Date;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.ttkp.services.DoctorScheduleService;

@Service
@Transactional
public class AppointmentServiceImpl implements AppointmentService {

    @Autowired
    private AppointmentRepository appointmentRepo;

    @Autowired
    private PatientService patientService;

    @Autowired
    private DoctorRepository doctorRepo;

    @Autowired
    private DoctorScheduleService doctorScheduleService;

    @Override
    public String addAppointment(
            int patientId,
            int doctorId,
            String appointmentDate,
            String notes) {

        Patient patient
                = this.patientService.getPatientById(patientId);

        Doctor doctor
                = this.doctorRepo.getDoctorById(doctorId);

        if (patient == null) {
            return "PATIENT_NOT_FOUND";
        }

        if (doctor == null) {
            return "DOCTOR_NOT_FOUND";
        }

        LocalDateTime ldt
                = LocalDateTime.parse(appointmentDate);

        Date date = Date.from(
                ldt.atZone(ZoneId.systemDefault()).toInstant()
        );

        if (!this.doctorScheduleService
                .isDoctorAvailable(doctorId, date)) {

            return "OUTSIDE_WORKING_HOURS";
        }

        if (this.appointmentRepo
                .isExactAppointmentTimeBooked(doctorId, date)) {

            return "DUPLICATE_TIME";
        }

        if (this.appointmentRepo
                .isAppointmentWithinThirtyMinutes(doctorId, date)) {

            return "WITHIN_THIRTY_MINUTES";
        }

        Appointment a = new Appointment();

        a.setPatientId(patient);
        a.setDoctorId(doctor);
        a.setAppointmentDate(date);
        a.setNotes(notes);
        a.setStatus("pending");
        a.setCreatedDate(new Date());

        boolean result
                = this.appointmentRepo.addAppointment(a);

        if (result) {
            return "SUCCESS";
        }

        return "FAILED";
    }

    @Override
    public List<Appointment> getAppointments() {
        return this.appointmentRepo.getAppointments();
    }

    @Override
    public List<Appointment> getAppointmentsByPatientId(int patientId) {
        return this.appointmentRepo.getAppointmentsByPatientId(patientId);
    }

    @Override
    public List<Appointment> getAppointmentsByDoctorId(int doctorId) {
        return this.appointmentRepo.getAppointmentsByDoctorId(doctorId);
    }

    @Override
    public Appointment getAppointmentById(int id) {
        return this.appointmentRepo.getAppointmentById(id);
    }

    @Override
    public boolean cancelAppointment(int id) {
        return this.appointmentRepo.updateAppointmentStatus(id, "cancelled");
    }

    @Override
    public boolean confirmAppointment(int id) {
        return this.appointmentRepo.confirmAppointment(id);
    }

    @Override
    public boolean updateAppointmentStatus(int id, String status) {
        return this.appointmentRepo.updateAppointmentStatus(id, status);
    }
}
