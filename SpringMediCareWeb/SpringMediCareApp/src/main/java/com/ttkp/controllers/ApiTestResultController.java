package com.ttkp.controllers;

import com.ttkp.pojo.TestResult;
import com.ttkp.services.TestResultService;
import java.util.List;
import java.util.Map;
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
public class ApiTestResultController {

    @Autowired
    private TestResultService testResultService;

    @GetMapping("/test-results/medical-record/{recordId}")
    public ResponseEntity<List<TestResult>> listByMedicalRecord(
            @PathVariable("recordId") int recordId) {

        return new ResponseEntity<>(
                this.testResultService.getTestResultsByRecordId(recordId),
                HttpStatus.OK
        );
    }

    @PostMapping("/test-results")
    public ResponseEntity<?> create(
            @RequestBody Map<String, String> params) {

        boolean result = this.testResultService.addTestResult(
                Integer.parseInt(params.get("recordId")),
                params.get("testName"),
                params.get("result")
        );

        if (result) {
            return new ResponseEntity<>(
                    "Thêm kết quả xét nghiệm thành công",
                    HttpStatus.CREATED
            );
        }

        return new ResponseEntity<>(
                "Không tìm thấy hồ sơ bệnh án",
                HttpStatus.NOT_FOUND
        );
    }
}
