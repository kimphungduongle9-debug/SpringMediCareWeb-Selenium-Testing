package com.ttkp.controllers;

import com.ttkp.pojo.User;
import com.ttkp.services.DoctorService;
import com.ttkp.services.SpecialtyService;
import com.ttkp.services.UserService;
import jakarta.servlet.http.HttpSession;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.beans.factory.annotation.Autowired;

@Controller
public class HomeController {

    @Autowired
    private DoctorService doctorService;

    @Autowired
    private SpecialtyService specialtyService;

    @Autowired
    private UserService userService;

    @RequestMapping({"/", "/home"})
    public String home() {
        return "index";
    }

    @RequestMapping("/doctors")
    public String doctors(Model model) {
        model.addAttribute("doctors", this.doctorService.getDoctors(null));
        return "doctor";
    }

    @RequestMapping("/specialties")
    public String specialties(Model model) {
        model.addAttribute("specialties", this.specialtyService.getSpecialties(null));
        return "specialties";
    }

    @RequestMapping("/login")
    public String login() {
        return "login";
    }

    @PostMapping("/login")
    public String doLogin(@RequestParam("username") String username,
            @RequestParam("password") String password,
            Model model,
            HttpSession session) {
        User user = this.userService.login(username, password);

        if (user == null) {
            model.addAttribute("error", "Sai tên đăng nhập/email hoặc mật khẩu");
            return "login";
        }

        session.setAttribute("currentUser", user);

        return "redirect:/home";
    }

    @GetMapping("/logout")
    public String logout(HttpSession session) {
        session.invalidate();
        return "redirect:/";
    }

    @RequestMapping("/register")
    public String register() {
        return "register";
    }

    @PostMapping("/register")
    public String doRegister(@RequestParam("firstName") String firstName,
            @RequestParam("lastName") String lastName,
            @RequestParam("email") String email,
            @RequestParam("phone") String phone,
            @RequestParam("username") String username,
            @RequestParam("password") String password,
            @RequestParam("dateOfBirth") String dateOfBirth,
            @RequestParam("gender") String gender,
            @RequestParam("address") String address,
            Model model) {

        if (this.userService.existsUsername(username)) {
            model.addAttribute("error", "Tên đăng nhập đã tồn tại");
            return "register";
        }

        if (this.userService.existsEmail(email)) {
            model.addAttribute("error", "Email đã tồn tại");
            return "register";
        }

        try {
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
            LocalDate dob = LocalDate.parse(dateOfBirth, formatter);

            this.userService.registerPatient(
                    firstName,
                    lastName,
                    email,
                    phone,
                    username,
                    password,
                    dob.toString(),
                    gender,
                    address
            );

        } catch (Exception ex) {
            model.addAttribute("error", "Ngày sinh phải đúng định dạng dd/MM/yyyy");
            return "register";
        }

        model.addAttribute("success", "Đăng ký thành công, hãy đăng nhập");
        return "login";
    }
}
