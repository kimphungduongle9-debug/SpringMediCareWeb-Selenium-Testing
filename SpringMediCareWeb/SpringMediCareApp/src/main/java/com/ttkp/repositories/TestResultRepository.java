package com.ttkp.repositories;

import com.ttkp.pojo.TestResult;
import java.util.List;

public interface TestResultRepository {

    List<TestResult> getTestResultsByRecordId(int recordId);

    void addTestResult(TestResult testResult);
}
