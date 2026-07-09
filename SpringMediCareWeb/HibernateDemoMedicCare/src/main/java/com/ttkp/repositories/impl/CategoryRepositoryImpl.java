package com.ttkp.repositories.impl;

import com.ttkp.hibernatedemomedicare.HibernateUtils;
import com.ttkp.pojo.Category;
import com.ttkp.repositories.CategoryRepository;
import java.util.List;
import org.hibernate.Session;

public class CategoryRepositoryImpl implements CategoryRepository {

    @Override
    public List<Category> getCategories() {
        try (Session session = HibernateUtils.getFactory().openSession()) {
            return session.createNamedQuery("Category.findAll", Category.class).getResultList();
        }
    }

    @Override
    public Category getCategoryById(int id) {
        try (Session session = HibernateUtils.getFactory().openSession()) {
            return session.get(Category.class, id);
        }
    }
}