package com.ttkp.controllers;

import com.ttkp.services.StatisticsService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.math.BigDecimal;
import org.springframework.web.bind.annotation.RequestParam;

@RestController
@RequestMapping("/api")
@CrossOrigin
public class ApiStatisticsController {

    @Autowired
    private StatisticsService statisticsService;

    @GetMapping("/statistics/patients-by-gender")
    public ResponseEntity<List<Object[]>> countPatientsByGender() {
        return new ResponseEntity<>(
                this.statisticsService.countPatientsByGender(),
                HttpStatus.OK
        );
    }

    @GetMapping("/statistics/patients-by-age-group")
    public ResponseEntity<List<Object[]>> countPatientsByAgeGroup() {
        return new ResponseEntity<>(
                this.statisticsService.countPatientsByAgeGroup(),
                HttpStatus.OK
        );
    }

    @GetMapping("/statistics/patients-by-specialty")
    public ResponseEntity<List<Object[]>> countPatientsBySpecialty() {
        return new ResponseEntity<>(
                this.statisticsService.countPatientsBySpecialty(),
                HttpStatus.OK
        );
    }

    @GetMapping("/statistics/patients-by-diagnosis")
    public ResponseEntity<List<Object[]>> countPatientsByDiagnosis() {
        return new ResponseEntity<>(
                this.statisticsService.countPatientsByDiagnosis(),
                HttpStatus.OK
        );
    }

    @GetMapping("/statistics/revenue-total")
    public ResponseEntity<BigDecimal> getTotalRevenue() {
        return new ResponseEntity<>(
                this.statisticsService.getTotalRevenue(),
                HttpStatus.OK
        );
    }

    @GetMapping("/statistics/revenue-by-month")
    public ResponseEntity<List<Object[]>> getRevenueByMonth(
            @RequestParam("year") int year) {
        return new ResponseEntity<>(
                this.statisticsService.getRevenueByMonth(year),
                HttpStatus.OK
        );
    }
}
