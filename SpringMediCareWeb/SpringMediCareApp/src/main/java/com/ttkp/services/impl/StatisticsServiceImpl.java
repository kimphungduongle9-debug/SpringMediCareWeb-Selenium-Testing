package com.ttkp.services.impl;

import com.ttkp.repositories.StatisticsRepository;
import com.ttkp.services.StatisticsService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.math.BigDecimal;

@Service
public class StatisticsServiceImpl implements StatisticsService {

    @Autowired
    private StatisticsRepository statisticsRepo;

    @Override
    public List<Object[]> countPatientsByGender() {
        return this.statisticsRepo.countPatientsByGender();
    }

    @Override
    public List<Object[]> countPatientsByAgeGroup() {
        return this.statisticsRepo.countPatientsByAgeGroup();
    }

    @Override
    public List<Object[]> countPatientsBySpecialty() {
        return this.statisticsRepo.countPatientsBySpecialty();
    }

    @Override
    public List<Object[]> countPatientsByDiagnosis() {
        return this.statisticsRepo.countPatientsByDiagnosis();
    }

    @Override
    public BigDecimal getTotalRevenue() {
        return this.statisticsRepo.getTotalRevenue();
    }

    @Override
    public List<Object[]> getRevenueByMonth(int year) {
        return this.statisticsRepo.getRevenueByMonth(year);
    }
}
