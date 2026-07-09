package com.ttkp.controllers;

import com.ttkp.pojo.DoctorSchedule;
import com.ttkp.services.DoctorScheduleService;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
@CrossOrigin
public class ApiDoctorScheduleController {

    @Autowired
    private DoctorScheduleService doctorScheduleService;

    @GetMapping("/doctor-schedules")
    public ResponseEntity<List<DoctorSchedule>> list(@RequestParam Map<String, String> params) {
        return new ResponseEntity<>(this.doctorScheduleService.getSchedules(), HttpStatus.OK);
    }

    @GetMapping("/doctors/{doctorId}/schedules")
    public ResponseEntity<List<DoctorSchedule>> listByDoctor(@PathVariable(value = "doctorId") int doctorId) {
        return new ResponseEntity<>(this.doctorScheduleService.getSchedulesByDoctorId(doctorId), HttpStatus.OK);
    }

    @GetMapping("/doctor-schedules/{scheduleId}")
    public ResponseEntity<DoctorSchedule> retrieve(@PathVariable(value = "scheduleId") int id) {
        return new ResponseEntity<>(this.doctorScheduleService.getScheduleById(id), HttpStatus.OK);
    }

    @PostMapping("/secure/doctor-schedules")
    @ResponseStatus(HttpStatus.CREATED)
    public void create(@RequestBody DoctorSchedule schedule) {
        this.doctorScheduleService.addOrUpdateSchedule(schedule);
    }

    @PutMapping("/secure/doctor-schedules/{scheduleId}")
    @ResponseStatus(HttpStatus.OK)
    public void update(@PathVariable(value = "scheduleId") int id, @RequestBody DoctorSchedule schedule) {
        schedule.setScheduleId(id);
        this.doctorScheduleService.addOrUpdateSchedule(schedule);
    }

    @DeleteMapping("/secure/doctor-schedules/{scheduleId}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void destroy(@PathVariable(value = "scheduleId") int id) {
        this.doctorScheduleService.deleteSchedule(id);
    }
}
