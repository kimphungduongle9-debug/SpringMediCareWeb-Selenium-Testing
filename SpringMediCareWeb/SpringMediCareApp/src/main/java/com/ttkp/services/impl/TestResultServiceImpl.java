package com.ttkp.services.impl;

import com.ttkp.pojo.MedicalRecord;
import com.ttkp.pojo.TestResult;
import com.ttkp.repositories.TestResultRepository;
import com.ttkp.services.MedicalRecordService;
import com.ttkp.services.TestResultService;
import java.util.Date;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import com.ttkp.pojo.Notification;
import com.ttkp.services.NotificationService;

@Service
@Transactional
public class TestResultServiceImpl implements TestResultService {

    @Autowired
    private TestResultRepository testResultRepo;

    @Autowired
    private MedicalRecordService medicalRecordService;

    @Autowired
    private NotificationService notificationService;

    @Override
    public List<TestResult> getTestResultsByRecordId(int recordId) {
        return this.testResultRepo.getTestResultsByRecordId(recordId);
    }

    @Override
    public boolean addTestResult(int recordId, String testName, String result) {
        MedicalRecord medicalRecord
                = this.medicalRecordService.getMedicalRecordById(recordId);

        if (medicalRecord == null) {
            return false;
        }

        TestResult testResult = new TestResult();

        testResult.setRecordId(medicalRecord);
        testResult.setTestName(testName);
        testResult.setResult(result);
        testResult.setCreatedDate(new Date());

        this.testResultRepo.addTestResult(testResult);

        Notification notification = new Notification();

        notification.setUserId(
                medicalRecord.getPatientId().getUserId()
        );

        String message = String.format(
                "Ket qua xet nghiem %s trong ho so kham benh #%d da duoc cap nhat",
                testName,
                medicalRecord.getRecordId()
        );

        notification.setMessage(message);
        notification.setIsRead(false);
        notification.setCreatedDate(new Date());

        this.notificationService.addNotification(notification);

        return true;

    }
}
