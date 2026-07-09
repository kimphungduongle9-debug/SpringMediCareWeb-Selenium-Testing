package com.ttkp.hibernatedemomedicare;

import com.ttkp.pojo.Drug;
import org.hibernate.Session;

public class HibernateDemoMediCare {

    public static void main(String[] args) {
        try (Session s = HibernateUtils.getFactory().openSession()) {
            Drug d = s.get(Drug.class, 1);

            System.out.println("Ten thuoc: " + d.getName());
            System.out.println("So luong: " + d.getQuantity());
            System.out.println("Han su dung: " + d.getExpiryDate());
            System.out.println("Danh muc: " + d.getCategoryId().getCategoryName());
        }
    }
}