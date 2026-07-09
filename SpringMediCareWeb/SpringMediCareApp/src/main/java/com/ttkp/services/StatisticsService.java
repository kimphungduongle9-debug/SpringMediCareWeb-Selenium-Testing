package com.ttkp.services;

import java.util.List;
import java.math.BigDecimal;

public interface StatisticsService {

    List<Object[]> countPatientsByGender();

    List<Object[]> countPatientsByAgeGroup();

    List<Object[]> countPatientsBySpecialty();

    List<Object[]> countPatientsByDiagnosis();

    BigDecimal getTotalRevenue();

    List<Object[]> getRevenueByMonth(int year);
}
