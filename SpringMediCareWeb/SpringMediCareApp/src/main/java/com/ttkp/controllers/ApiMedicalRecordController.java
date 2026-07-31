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
import com.ttkp.pojo.Doctor;
import com.ttkp.pojo.User;
import com.ttkp.services.DoctorService;
import com.ttkp.services.UserService;
import com.ttkp.utils.JwtUtils;
import org.springframework.web.bind.annotation.RequestHeader;

@RestController
@RequestMapping("/api")
@CrossOrigin
public class ApiMedicalRecordController {

    @Autowired
    private MedicalRecordService medicalRecordService;

    @Autowired
    private UserService userService;

    @Autowired
    private DoctorService doctorService;

    private User getCurrentUser(String authorization) throws Exception {
        if (authorization == null
                || !authorization.startsWith("Bearer ")) {
            return null;
        }

        String token = authorization.substring(7);

        String username = JwtUtils.validateTokenAndGetUsername(token);

        if (username == null) {
            return null;
        }

        return this.userService.getUserByUsername(username);
    }

    @GetMapping("/medical-records/patient/{patientId}")
    public ResponseEntity<List<MedicalRecord>> listByPatient(
            @PathVariable("patientId") int patientId) {

        return new ResponseEntity<>(
                this.medicalRecordService.getMedicalRecordsByPatientId(patientId),
                HttpStatus.OK
        );
    }

    @GetMapping("/medical-records/appointment/{appointmentId}")
    public ResponseEntity<?> retrieveByAppointment(
            @PathVariable("appointmentId") int appointmentId,
            @RequestHeader(value = "Authorization", required = false) String authorization) {

        try {
            User user = this.getCurrentUser(authorization);

            if (user == null) {
                return new ResponseEntity<>(
                        "Bạn chưa đăng nhập hoặc token không hợp lệ.",
                        HttpStatus.UNAUTHORIZED
                );
            }

            Doctor currentDoctor
                    = this.doctorService.getDoctorByUserId(user.getId());

            if (currentDoctor == null) {
                return new ResponseEntity<>(
                        "Chỉ bác sĩ mới được xem hồ sơ bệnh án.",
                        HttpStatus.FORBIDDEN
                );
            }

            MedicalRecord medicalRecord
                    = this.medicalRecordService
                            .getMedicalRecordByAppointmentId(appointmentId);

            if (medicalRecord == null) {
                return new ResponseEntity<>(
                        "Không tìm thấy hồ sơ bệnh án.",
                        HttpStatus.NOT_FOUND
                );
            }

            if (!medicalRecord.getDoctorId().getDoctorId()
                    .equals(currentDoctor.getDoctorId())) {

                return new ResponseEntity<>(
                        "Bạn không có quyền xem hồ sơ bệnh án này.",
                        HttpStatus.FORBIDDEN
                );
            }

            return new ResponseEntity<>(medicalRecord, HttpStatus.OK);

        } catch (Exception e) {
            return new ResponseEntity<>(
                    "Token không hợp lệ.",
                    HttpStatus.UNAUTHORIZED
            );
        }
    }

    @PutMapping("/medical-records/{id}")
    public ResponseEntity<?> update(
            @PathVariable("id") int id,
            @RequestBody Map<String, String> params,
            @RequestHeader(value = "Authorization", required = false) String authorization) {

        try {
            User user = this.getCurrentUser(authorization);

            if (user == null) {
                return new ResponseEntity<>(
                        "Bạn chưa đăng nhập hoặc token không hợp lệ.",
                        HttpStatus.UNAUTHORIZED
                );
            }

            Doctor currentDoctor
                    = this.doctorService.getDoctorByUserId(user.getId());

            if (currentDoctor == null) {
                return new ResponseEntity<>(
                        "Chỉ bác sĩ mới được cập nhật hồ sơ bệnh án.",
                        HttpStatus.FORBIDDEN
                );
            }

            MedicalRecord medicalRecord
                    = this.medicalRecordService.getMedicalRecordById(id);

            if (medicalRecord == null) {
                return new ResponseEntity<>(
                        "Không tìm thấy hồ sơ bệnh án.",
                        HttpStatus.NOT_FOUND
                );
            }

            if (!medicalRecord.getDoctorId().getDoctorId()
                    .equals(currentDoctor.getDoctorId())) {

                return new ResponseEntity<>(
                        "Bạn không có quyền cập nhật hồ sơ bệnh án này.",
                        HttpStatus.FORBIDDEN
                );
            }

            String diagnosis = params.get("diagnosis");
            String treatment = params.get("treatment");

            if (diagnosis == null || diagnosis.trim().isEmpty()
                    || treatment == null || treatment.trim().isEmpty()) {

                return new ResponseEntity<>(
                        "Vui lòng nhập đầy đủ chẩn đoán và hướng điều trị.",
                        HttpStatus.BAD_REQUEST
                );
            }

            boolean result = this.medicalRecordService.updateMedicalRecord(
                    id,
                    diagnosis.trim(),
                    treatment.trim()
            );

            if (result) {
                return new ResponseEntity<>(
                        "Cập nhật hồ sơ bệnh án thành công",
                        HttpStatus.OK
                );
            }

            return new ResponseEntity<>(
                    "Cập nhật hồ sơ bệnh án thất bại",
                    HttpStatus.BAD_REQUEST
            );

        } catch (Exception e) {
            return new ResponseEntity<>(
                    "Token không hợp lệ.",
                    HttpStatus.UNAUTHORIZED
            );
        }
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

}
