package com.ttkp.controllers;

import com.ttkp.pojo.DoctorSchedule;
import com.ttkp.services.DoctorScheduleService;
import com.ttkp.services.DoctorService;
import java.util.HashMap;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/admin")
public class DoctorScheduleController {

    @Autowired
    private DoctorScheduleService doctorScheduleService;

    @Autowired
    private DoctorService doctorService;

    @GetMapping("/doctor-schedules")
    public String createView(Model model) {
        model.addAttribute("schedule", new DoctorSchedule());
        model.addAttribute("schedules", this.doctorScheduleService.getSchedules());
        model.addAttribute("doctors", this.doctorService.getDoctors(new HashMap<>()));

        return "doctor-schedules";
    }

    @PostMapping("/doctor-schedules")
    public String create(Model model, @ModelAttribute(value = "schedule") DoctorSchedule schedule) {
        this.doctorScheduleService.addOrUpdateSchedule(schedule);

        return "redirect:/admin/doctor-schedules";
    }

    @GetMapping("/doctor-schedules/{scheduleId}")
    public String updateView(@PathVariable(value = "scheduleId") int id, Model model) {
        model.addAttribute("schedule", this.doctorScheduleService.getScheduleById(id));
        model.addAttribute("schedules", this.doctorScheduleService.getSchedules());
        model.addAttribute("doctors", this.doctorService.getDoctors(new HashMap<>()));

        return "doctor-schedules";
    }
}
