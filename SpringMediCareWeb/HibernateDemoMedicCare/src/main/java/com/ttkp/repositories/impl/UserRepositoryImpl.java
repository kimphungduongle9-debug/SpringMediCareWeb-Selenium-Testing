package com.ttkp.repositories.impl;

import com.ttkp.hibernatedemomedicare.HibernateUtils;
import com.ttkp.pojo.Patient;
import com.ttkp.pojo.User;
import com.ttkp.repositories.UserRepository;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.Date;
import org.hibernate.Session;
import org.hibernate.Transaction;
import org.hibernate.query.Query;

public class UserRepositoryImpl implements UserRepository {

    @Override
    public User login(String username, String password) {
        try (Session session = HibernateUtils.getFactory().openSession()) {

            Query<User> q = session.createNamedQuery("User.findByUsername", User.class);
            q.setParameter("username", username);

            User u = q.uniqueResult();

            if (u != null && u.getPassword().equals(password)) {
                return u;
            }

            return null;
        }
    }

    @Override
    public boolean existsUsername(String username) {
        try (Session session = HibernateUtils.getFactory().openSession()) {

            Query<User> q = session.createNamedQuery("User.findByUsername", User.class);
            q.setParameter("username", username);

            return q.uniqueResult() != null;
        }
    }

    @Override
    public boolean existsEmail(String email) {
        try (Session session = HibernateUtils.getFactory().openSession()) {

            Query<User> q = session.createNamedQuery("User.findByEmail", User.class);
            q.setParameter("email", email);

            return q.uniqueResult() != null;
        }
    }

    @Override
    public boolean registerPatient(String firstName, String lastName, String email,
            String phone, String username, String password,
            String dateOfBirth, String gender, String address) {

        Transaction tx = null;

        try (Session session = HibernateUtils.getFactory().openSession()) {
            tx = session.beginTransaction();

            User user = new User();
            user.setFirstName(firstName);
            user.setLastName(lastName);
            user.setEmail(email);
            user.setPhone(phone);
            user.setUsername(username);
            user.setPassword(password);
            user.setRole("patient");
            user.setCreatedDate(new Date()); // QUAN TRỌNG

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

            tx.commit();
            return true;

        } catch (Exception e) {
            if (tx != null) {
                tx.rollback();
            }
            e.printStackTrace();
            return false;
        }
    }
}
