package com.ttkp.controllers;

import com.ttkp.pojo.Doctor;
import com.ttkp.services.DoctorService;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.PathVariable;

@RestController
@RequestMapping("/api")
@CrossOrigin
public class ApiDoctorController {

    @Autowired
    private DoctorService doctorService;

    @GetMapping("/doctors")
    public ResponseEntity<List<Doctor>> list(@RequestParam Map<String, String> params) {
        return new ResponseEntity<>(this.doctorService.getDoctors(params), HttpStatus.OK);
    }

    @GetMapping("/doctors/all")
    public ResponseEntity<List<Doctor>> listAll() {
        return new ResponseEntity<>(this.doctorService.getAllDoctors(), HttpStatus.OK);
    }

    @GetMapping("/doctors/user/{userId}")
    public ResponseEntity<Doctor> retrieveByUserId(@PathVariable("userId") int userId) {
        Doctor d = this.doctorService.getDoctorByUserId(userId);

        if (d == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        return new ResponseEntity<>(d, HttpStatus.OK);
    }

    @GetMapping("/doctors/{id}")
    public ResponseEntity<Doctor> retrieve(@PathVariable("id") int id) {
        Doctor d = this.doctorService.getDoctorById(id);

        if (d == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        return new ResponseEntity<>(d, HttpStatus.OK);
    }
}
