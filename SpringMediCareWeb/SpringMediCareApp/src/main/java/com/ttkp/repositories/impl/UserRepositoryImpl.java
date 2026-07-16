package com.ttkp.repositories.impl;

import com.ttkp.pojo.Patient;
import com.ttkp.pojo.User;
import com.ttkp.repositories.UserRepository;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.Date;
import org.hibernate.Session;
import org.hibernate.query.Query;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.orm.hibernate5.LocalSessionFactoryBean;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

@Repository
@Transactional
public class UserRepositoryImpl implements UserRepository {

    @Autowired
    private LocalSessionFactoryBean factory;

    @Override
    public User getUserByUsername(String username) {
        Session session = this.factory.getObject().getCurrentSession();

        Query<User> q = session.createNamedQuery("User.findByUsername", User.class);
        q.setParameter("username", username);

        return q.uniqueResult();
    }

    @Override
    public User getUserByUsernameOrEmail(String keyword) {
        Session session = this.factory.getObject().getCurrentSession();

        Query<User> q = session.createNamedQuery("User.findByUsernameOrEmail", User.class);
        q.setParameter("keyword", keyword);

        return q.uniqueResult();
    }

    @Override
    public User addUser(User u) {
        Session session = this.factory.getObject().getCurrentSession();
        session.persist(u);

        return u;
    }

    @Override
    public boolean existsUsername(String username) {
        Session session = this.factory.getObject().getCurrentSession();

        Query<User> q = session.createNamedQuery("User.findByUsername", User.class);
        q.setParameter("username", username);
        q.setMaxResults(1);

        return !q.getResultList().isEmpty();
    }

    @Override
    public boolean existsEmail(String email) {
        Session session = this.factory.getObject().getCurrentSession();

        Query<User> q = session.createNamedQuery("User.findByEmail",User.class);
        q.setParameter("email", email);
        q.setMaxResults(1);

        return !q.getResultList().isEmpty();
    }

    @Override
    public boolean registerPatient(String firstName, String lastName, String email,
            String phone, String username, String password,
            String dateOfBirth, String gender, String address) {

        Session session = this.factory.getObject().getCurrentSession();

        User user = new User();
        user.setFirstName(firstName);
        user.setLastName(lastName);
        user.setEmail(email);
        user.setPhone(phone);
        user.setUsername(username);
        user.setPassword(password);
        user.setRole("patient");
        user.setCreatedDate(new Date());

        session.persist(user);

        LocalDate localDate = LocalDate.parse(dateOfBirth);
        Date dob = Date.from(localDate.atStartOfDay(ZoneId.systemDefault()).toInstant());

        Patient p = new Patient();
        p.setUserId(user);
        p.setFullName(firstName + " " + lastName);
        p.setDateOfBirth(dob);
        p.setGender(gender);
        p.setAddress(address);

        session.persist(p);

        return true;
    }
}
