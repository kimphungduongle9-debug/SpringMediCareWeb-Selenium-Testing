package com.ttkp.controllers;

import com.ttkp.pojo.Appointment;
import com.ttkp.services.AppointmentService;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
@CrossOrigin
public class ApiAppointmentController {

    @Autowired
    private AppointmentService appointmentService;

    @PostMapping("/appointments")
    public ResponseEntity<?> create(@RequestBody Map<String, String> params) {
        boolean result = this.appointmentService.addAppointment(
                Integer.parseInt(params.get("patientId")),
                Integer.parseInt(params.get("doctorId")),
                params.get("appointmentDate"),
                params.get("notes")
        );

        if (result) {
            return new ResponseEntity<>("Đặt lịch thành công", HttpStatus.CREATED);
        }

        return new ResponseEntity<>("Đặt lịch thất bại", HttpStatus.BAD_REQUEST);
    }

    @GetMapping("/appointments")
    public ResponseEntity<List<Appointment>> list() {
        return new ResponseEntity<>(this.appointmentService.getAppointments(), HttpStatus.OK);
    }

    @GetMapping("/appointments/patient/{patientId}")
    public ResponseEntity<List<Appointment>> listByPatient(@PathVariable("patientId") int patientId) {
        return new ResponseEntity<>(
                this.appointmentService.getAppointmentsByPatientId(patientId),
                HttpStatus.OK
        );
    }

    @GetMapping("/appointments/doctor/{doctorId}")
    public ResponseEntity<List<Appointment>> listByDoctor(@PathVariable("doctorId") int doctorId) {
        return new ResponseEntity<>(
                this.appointmentService.getAppointmentsByDoctorId(doctorId),
                HttpStatus.OK
        );
    }

    @GetMapping("/appointments/{id}")
    public ResponseEntity<Appointment> retrieve(@PathVariable("id") int id) {
        Appointment a = this.appointmentService.getAppointmentById(id);

        if (a == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        return new ResponseEntity<>(a, HttpStatus.OK);
    }

    @PutMapping("/appointments/{id}/cancel")
    public ResponseEntity<?> cancel(@PathVariable("id") int id) {
        if (this.appointmentService.cancelAppointment(id)) {
            return new ResponseEntity<>("Hủy lịch thành công", HttpStatus.OK);
        }

        return new ResponseEntity<>("Không tìm thấy lịch hẹn", HttpStatus.NOT_FOUND);
    }

    @PutMapping("/appointments/{id}/confirm")
    public ResponseEntity<?> confirm(@PathVariable("id") int id) {
        if (this.appointmentService.confirmAppointment(id)) {
            return new ResponseEntity<>("Xác nhận lịch thành công", HttpStatus.OK);
        }

        return new ResponseEntity<>("Không tìm thấy lịch hẹn", HttpStatus.NOT_FOUND);
    }
}
