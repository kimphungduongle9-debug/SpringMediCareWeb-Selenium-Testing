package com.ttkp.repositories;

import java.util.List;
import java.math.BigDecimal;

public interface StatisticsRepository {

    List<Object[]> countPatientsByGender();

    List<Object[]> countPatientsByAgeGroup();

    List<Object[]> countPatientsBySpecialty();

    List<Object[]> countPatientsByDiagnosis();

    BigDecimal getTotalRevenue();

    List<Object[]> getRevenueByMonth(int year);
}
