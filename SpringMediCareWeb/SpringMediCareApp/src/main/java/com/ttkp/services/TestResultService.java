package com.ttkp.services;

import com.ttkp.pojo.TestResult;
import java.util.List;

public interface TestResultService {

    List<TestResult> getTestResultsByRecordId(int recordId);

    boolean addTestResult(int recordId, String testName, String result);
}
