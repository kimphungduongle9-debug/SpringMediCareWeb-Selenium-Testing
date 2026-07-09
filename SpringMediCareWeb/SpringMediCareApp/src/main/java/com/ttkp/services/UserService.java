package com.ttkp.services;

import com.ttkp.pojo.User;
import java.util.Map;
import org.springframework.web.multipart.MultipartFile;

public interface UserService {

    User login(String username, String password);

    User getUserByUsername(String username);

    User addUser(User u);

    User addUser(Map<String, String> params, MultipartFile avatar);

    boolean authenticate(String username, String password);

    boolean existsUsername(String username);

    boolean existsEmail(String email);

    boolean registerPatient(String firstName, String lastName, String email,
            String phone, String username, String password,
            String dateOfBirth, String gender, String address);
}
