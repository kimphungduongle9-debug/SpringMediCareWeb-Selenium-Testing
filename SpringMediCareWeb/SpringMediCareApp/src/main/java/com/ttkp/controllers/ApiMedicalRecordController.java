package com.ttkp.controllers;

import com.ttkp.pojo.MedicalRecord;
import com.ttkp.services.MedicalRecordService;
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
public class ApiMedicalRecordController {

    @Autowired
    private MedicalRecordService medicalRecordService;

    @GetMapping("/medical-records/patient/{patientId}")
    public ResponseEntity<List<MedicalRecord>> listByPatient(
            @PathVariable("patientId") int patientId) {

        return new ResponseEntity<>(
                this.medicalRecordService.getMedicalRecordsByPatientId(patientId),
                HttpStatus.OK
        );
    }

    @GetMapping("/medical-records/appointment/{appointmentId}")
    public ResponseEntity<MedicalRecord> retrieveByAppointment(
            @PathVariable("appointmentId") int appointmentId) {

        MedicalRecord medicalRecord
                = this.medicalRecordService
                        .getMedicalRecordByAppointmentId(appointmentId);

        if (medicalRecord == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        return new ResponseEntity<>(medicalRecord, HttpStatus.OK);
    }

    @GetMapping("/medical-records/{id}")
    public ResponseEntity<MedicalRecord> retrieve(
            @PathVariable("id") int id) {

        MedicalRecord medicalRecord
                = this.medicalRecordService.getMedicalRecordById(id);

        if (medicalRecord == null) {
            return new ResponseEntity<>(HttpStatus.NOT_FOUND);
        }

        return new ResponseEntity<>(medicalRecord, HttpStatus.OK);
    }

    @PostMapping("/medical-records")
    public ResponseEntity<?> create(
            @RequestBody Map<String, String> params) {

        boolean result = this.medicalRecordService.addMedicalRecord(
                Integer.parseInt(params.get("appointmentId")),
                params.get("diagnosis"),
                params.get("treatment")
        );

        if (result) {
            return new ResponseEntity<>(
                    "Tạo hồ sơ bệnh án thành công",
                    HttpStatus.CREATED
            );
        }

        return new ResponseEntity<>(
                "Tạo hồ sơ bệnh án thất bại",
                HttpStatus.BAD_REQUEST
        );
    }

    @PutMapping("/medical-records/{id}")
    public ResponseEntity<?> update(
            @PathVariable("id") int id,
            @RequestBody Map<String, String> params) {

        boolean result = this.medicalRecordService.updateMedicalRecord(
                id,
                params.get("diagnosis"),
                params.get("treatment")
        );

        if (result) {
            return new ResponseEntity<>(
                    "Cập nhật hồ sơ bệnh án thành công",
                    HttpStatus.OK
            );
        }

        return new ResponseEntity<>(
                "Không tìm thấy hồ sơ bệnh án",
                HttpStatus.NOT_FOUND
        );
    }
}
