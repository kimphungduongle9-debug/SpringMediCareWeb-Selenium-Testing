package com.ttkp.controllers;

import com.ttkp.pojo.Prescription;
import com.ttkp.pojo.PrescriptionDetail;
import com.ttkp.pojo.PrescriptionItem;
import com.ttkp.services.PrescriptionService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
@CrossOrigin
public class ApiPrescriptionController {

    @Autowired
    private PrescriptionService prescriptionService;

    @GetMapping("/prescriptions/medical-record/{recordId}")
    public ResponseEntity<List<Prescription>> listByMedicalRecord(
            @PathVariable("recordId") int recordId) {

        return new ResponseEntity<>(
                this.prescriptionService
                        .getPrescriptionsByRecordId(recordId),
                HttpStatus.OK
        );
    }

    @GetMapping("/prescription-details/prescription/{prescriptionId}")
    public ResponseEntity<List<PrescriptionDetail>> listDetailsByPrescription(
            @PathVariable("prescriptionId") int prescriptionId) {

        return new ResponseEntity<>(
                this.prescriptionService
                        .getPrescriptionDetailsByPrescriptionId(prescriptionId),
                HttpStatus.OK
        );
    }

    @PostMapping("/prescriptions/medical-record/{recordId}")
    public ResponseEntity<?> create(
            @PathVariable("recordId") int recordId,
            @RequestBody List<PrescriptionItem> items) {

        boolean result
                = this.prescriptionService
                        .addPrescription(recordId, items);

        if (result) {
            return new ResponseEntity<>(
                    "Kê đơn thuốc thành công",
                    HttpStatus.CREATED
            );
        }

        return new ResponseEntity<>(
                "Không thể kê đơn thuốc. Vui lòng kiểm tra hồ sơ và số lượng tồn kho.",
                HttpStatus.BAD_REQUEST
        );
    }
}
