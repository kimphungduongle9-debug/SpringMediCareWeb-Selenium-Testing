package com.ttkp.services.impl;

import com.ttkp.pojo.User;
import com.ttkp.repositories.UserRepository;
import com.ttkp.services.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import com.cloudinary.Cloudinary;
import com.cloudinary.utils.ObjectUtils;
import java.io.IOException;
import java.util.Map;
import org.springframework.web.multipart.MultipartFile;

@Service
public class UserServiceImpl implements UserService {

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private BCryptPasswordEncoder passwordEncoder;

    @Autowired
    private Cloudinary cloudinary;

    @Override
    public boolean authenticate(String username, String password) {
        User u = this.login(username, password);
        return u != null;
    }

    @Override
    public User login(String username, String password) {
        if (username == null || password == null) {
            return null;
        }

        User u = this.userRepository.getUserByUsernameOrEmail(username.trim());

        if (u == null) {
            return null;
        }

        if (this.passwordEncoder.matches(password, u.getPassword())) {
            return u;
        }

        if (u.getPassword().equals(password)) {
            return u;
        }

        return null;
    }

    @Override
    public User getUserByUsername(String username) {
        return this.userRepository.getUserByUsername(username);
    }

    @Override
    public User addUser(User u) {
        u.setPassword(this.passwordEncoder.encode(u.getPassword()));
        u.setCreatedDate(new java.util.Date());

        if (u.getFile() != null && !u.getFile().isEmpty()) {
            try {
                Map res = this.cloudinary.uploader().upload(u.getFile().getBytes(),
                        ObjectUtils.asMap("resource_type", "auto"));

                u.setImage(res.get("secure_url").toString());
            } catch (IOException ex) {
                System.err.println(ex.getMessage());
            }
        }

        return this.userRepository.addUser(u);
    }

    @Override
    public User addUser(Map<String, String> params, MultipartFile avatar) {
        User u = new User();

        u.setFirstName(params.get("firstName"));
        u.setLastName(params.get("lastName"));
        u.setEmail(params.get("email"));
        u.setPhone(params.get("phone"));
        u.setUsername(params.get("username"));
        u.setPassword(this.passwordEncoder.encode(params.get("password")));
        u.setRole(params.get("role") != null ? params.get("role") : "patient");
        u.setCreatedDate(new java.util.Date());

        if (avatar != null && !avatar.isEmpty()) {
            try {
                Map res = this.cloudinary.uploader().upload(avatar.getBytes(),
                        ObjectUtils.asMap("resource_type", "auto"));

                u.setImage(res.get("secure_url").toString());
            } catch (IOException ex) {
                System.err.println(ex.getMessage());
            }
        }

        return this.userRepository.addUser(u);
    }

    @Override
    public boolean existsUsername(String username) {
        return this.userRepository.existsUsername(username);
    }

    @Override
    public boolean existsEmail(String email) {
        return this.userRepository.existsEmail(email);
    }

    @Override
    public boolean registerPatient(String firstName, String lastName, String email,
            String phone, String username, String password,
            String dateOfBirth, String gender, String address) {
        String encodedPassword = this.passwordEncoder.encode(password);

        return this.userRepository.registerPatient(
                firstName, lastName, email, phone, username,
                encodedPassword, dateOfBirth, gender, address);
    }
}
