package com.ttkp.controllers;

import com.ttkp.pojo.User;
import com.ttkp.services.UserService;
import com.ttkp.utils.JwtUtils;
import java.util.Collections;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api")
@CrossOrigin
public class ApiUserController {

    @Autowired
    private UserService userService;

    @PostMapping("/users")
    public ResponseEntity<User> create(@RequestParam Map<String, String> info,
            @RequestParam(value = "avatar") MultipartFile avatar) {
        User u = this.userService.addUser(info, avatar);
        return new ResponseEntity<>(u, HttpStatus.CREATED);
    }

    @PostMapping(value = "/login", consumes = "application/json")
    public ResponseEntity<?> login(@RequestBody User u) {

        User user = this.userService.login(u.getUsername(), u.getPassword());

        if (user != null) {
            try {
                String token = JwtUtils.generateToken(user.getUsername());
                return ResponseEntity.ok().body(Collections.singletonMap("token", token));
            } catch (Exception e) {
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                        .body("Lỗi khi tạo JWT");
            }
        }

        return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                .body("Sai thông tin đăng nhập");
    }

    @GetMapping("/secure/profile")
    public ResponseEntity<?> profile(@RequestHeader("Authorization") String authorization) {
        try {
            if (authorization == null || !authorization.startsWith("Bearer ")) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                        .body("Thiếu token");
            }

            String token = authorization.substring(7);
            String username = JwtUtils.validateTokenAndGetUsername(token);

            if (username == null) {
                return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                        .body("Token không hợp lệ");
            }

            User user = this.userService.getUserByUsername(username);

            if (user == null) {
                return ResponseEntity.status(HttpStatus.NOT_FOUND)
                        .body("Không tìm thấy người dùng");
            }

            return ResponseEntity.ok(user);

        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                    .body("Token không hợp lệ");
        }
    }
}
