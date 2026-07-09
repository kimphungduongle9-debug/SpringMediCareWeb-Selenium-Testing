/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package com.ttkp.hibernatedemomedicare;

import com.ttkp.pojo.Appointment;
import com.ttkp.pojo.Doctor;
import com.ttkp.pojo.Drug;
import com.ttkp.pojo.Category;
import com.ttkp.pojo.MedicalRecord;
import com.ttkp.pojo.Notification;
import com.ttkp.pojo.Patient;
import com.ttkp.pojo.Payment;
import com.ttkp.pojo.Prescription;
import com.ttkp.pojo.PrescriptionDetail;
import com.ttkp.pojo.Specialty;
import com.ttkp.pojo.TestResult;
import com.ttkp.pojo.User;
import java.util.Properties;
import org.hibernate.SessionFactory;
import org.hibernate.boot.registry.StandardServiceRegistryBuilder;
import org.hibernate.cfg.Configuration;
import org.hibernate.cfg.Environment;
import org.hibernate.service.ServiceRegistry;

/**
 *
 * @author MY PC
 */
public class HibernateUtils {
    private static final SessionFactory factory;

    static {
        Configuration conf = new Configuration();
        
        Properties props = new Properties();
        props.setProperty(Environment.DIALECT, "org.hibernate.dialect.MySQLDialect");
        props.setProperty(Environment.JAKARTA_JDBC_DRIVER, "com.mysql.cj.jdbc.Driver");
        props.setProperty(Environment.JAKARTA_JDBC_URL, "jdbc:mysql://localhost/medicare_db");
        props.setProperty(Environment.JAKARTA_JDBC_USER, "root");
        props.setProperty(Environment.JAKARTA_JDBC_PASSWORD, "root");
        props.setProperty(Environment.SHOW_SQL, "true");
        
        conf.setProperties(props);
        
        conf.addAnnotatedClass(Appointment.class);
        conf.addAnnotatedClass(Doctor.class);
        conf.addAnnotatedClass(Drug.class);
        conf.addAnnotatedClass(Category.class);
        conf.addAnnotatedClass(MedicalRecord.class);
        conf.addAnnotatedClass(Notification.class);
        conf.addAnnotatedClass(Patient.class);
        conf.addAnnotatedClass(Payment.class);
        conf.addAnnotatedClass(Prescription.class);
        conf.addAnnotatedClass(PrescriptionDetail.class);
        conf.addAnnotatedClass(Specialty.class);
        conf.addAnnotatedClass(TestResult.class);
        conf.addAnnotatedClass(User.class);
        
        ServiceRegistry serviceRegistry = new StandardServiceRegistryBuilder()
                .applySettings(conf.getProperties()).build();
        
        factory = conf.buildSessionFactory(serviceRegistry);
        
    }
    /**
     * @return the factory
     */
    public static SessionFactory getFactory() {
        return factory;
    }
    
}
