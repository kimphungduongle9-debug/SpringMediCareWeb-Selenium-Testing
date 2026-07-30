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
import com.ttkp.pojo.Doctor;
import com.ttkp.pojo.User;
import com.ttkp.services.DoctorService;
import com.ttkp.services.UserService;
import com.ttkp.utils.JwtUtils;
import org.springframework.web.bind.annotation.RequestHeader;

@RestController
@RequestMapping("/api")
@CrossOrigin
public class ApiAppointmentController {

    @Autowired
    private AppointmentService appointmentService;

    @Autowired
    private UserService userService;

    @Autowired
    private DoctorService doctorService;

    @PostMapping("/appointments")
    public ResponseEntity<?> create(
            @RequestBody Map<String, String> params) {

        String result = this.appointmentService.addAppointment(
                Integer.parseInt(params.get("patientId")),
                Integer.parseInt(params.get("doctorId")),
                params.get("appointmentDate"),
                params.get("notes")
        );

        switch (result) {
            case "SUCCESS":
                return new ResponseEntity<>(
                        "Đặt lịch thành công",
                        HttpStatus.CREATED
                );

            case "OUTSIDE_WORKING_HOURS":
                return new ResponseEntity<>(
                        "Giờ khám không nằm trong lịch làm việc của bác sĩ.",
                        HttpStatus.BAD_REQUEST
                );

            case "DUPLICATE_TIME":
                return new ResponseEntity<>(
                        "Khung giờ này đã có người đặt.",
                        HttpStatus.CONFLICT
                );

            case "WITHIN_THIRTY_MINUTES":
                return new ResponseEntity<>(
                        "Lịch hẹn phải cách lịch đã đặt ít nhất 30 phút.",
                        HttpStatus.CONFLICT
                );

            case "PATIENT_NOT_FOUND":
                return new ResponseEntity<>(
                        "Không tìm thấy thông tin bệnh nhân.",
                        HttpStatus.NOT_FOUND
                );

            case "DOCTOR_NOT_FOUND":
                return new ResponseEntity<>(
                        "Không tìm thấy thông tin bác sĩ.",
                        HttpStatus.NOT_FOUND
                );

            default:
                return new ResponseEntity<>(
                        "Đặt lịch thất bại. Vui lòng thử lại.",
                        HttpStatus.BAD_REQUEST
                );
        }
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

    @GetMapping("/appointments/{id}/examination")
    public ResponseEntity<?> retrieveForExamination(
            @PathVariable("id") int id,
            @RequestHeader(value = "Authorization", required = false) String authorization) {

        try {
            // 1. Kiểm tra token
            if (authorization == null
                    || !authorization.startsWith("Bearer ")) {

                return new ResponseEntity<>(
                        "Bạn chưa đăng nhập.",
                        HttpStatus.UNAUTHORIZED
                );
            }

            String token = authorization.substring(7);

            String username
                    = JwtUtils.validateTokenAndGetUsername(token);

            if (username == null) {
                return new ResponseEntity<>(
                        "Token không hợp lệ.",
                        HttpStatus.UNAUTHORIZED
                );
            }

            // 2. Lấy người dùng đang đăng nhập
            User user = this.userService.getUserByUsername(username);

            if (user == null) {
                return new ResponseEntity<>(
                        "Không tìm thấy người dùng.",
                        HttpStatus.UNAUTHORIZED
                );
            }

            // 3. Kiểm tra người dùng có phải bác sĩ
            Doctor currentDoctor
                    = this.doctorService.getDoctorByUserId(user.getId());

            if (currentDoctor == null) {
                return new ResponseEntity<>(
                        "Bạn không có quyền thực hiện khám bệnh.",
                        HttpStatus.FORBIDDEN
                );
            }

            // 4. Lấy lịch hẹn
            Appointment appointment
                    = this.appointmentService.getAppointmentById(id);

            if (appointment == null) {
                return new ResponseEntity<>(
                        "Không tìm thấy lịch hẹn.",
                        HttpStatus.NOT_FOUND
                );
            }

            // 5. Kiểm tra lịch có thuộc bác sĩ đang đăng nhập
            if (!appointment.getDoctorId().getDoctorId()
                    .equals(currentDoctor.getDoctorId())) {

                return new ResponseEntity<>(
                        "Lịch hẹn không thuộc bác sĩ đang đăng nhập.",
                        HttpStatus.FORBIDDEN
                );
            }

            // 6. Chỉ lịch đã xác nhận mới được khám
            if (!"confirmed".equals(appointment.getStatus())) {
                return new ResponseEntity<>(
                        "Chỉ được khám lịch hẹn đã được xác nhận.",
                        HttpStatus.CONFLICT
                );
            }

            return new ResponseEntity<>(
                    appointment,
                    HttpStatus.OK
            );

        } catch (Exception e) {
            return new ResponseEntity<>(
                    "Token không hợp lệ.",
                    HttpStatus.UNAUTHORIZED
            );
        }
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
