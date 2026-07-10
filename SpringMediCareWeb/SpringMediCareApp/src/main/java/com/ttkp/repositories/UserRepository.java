package com.ttkp.repositories;

import com.ttkp.pojo.User;

public interface UserRepository {
    
    User getUserByUsername(String username);
    
    User getUserByUsernameOrEmail(String keyword);
    
    User addUser(User u);

    boolean existsUsername(String username);

    boolean existsEmail(String email);

    boolean registerPatient(String firstName, String lastName, String email,
            String phone, String username, String password,
            String dateOfBirth, String gender, String address);
}
