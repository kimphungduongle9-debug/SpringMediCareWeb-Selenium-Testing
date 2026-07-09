package com.ttkp.repositories.impl;


import com.ttkp.pojo.Category;
import com.ttkp.repositories.CategoryRepository;
import java.util.List;
import org.hibernate.Session;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.orm.hibernate5.LocalSessionFactoryBean;
import org.springframework.stereotype.Repository;
import org.springframework.transaction.annotation.Transactional;

@Repository
@Transactional
public class CategoryRepositoryImpl implements CategoryRepository {

    @Autowired
    private LocalSessionFactoryBean factory;
    
    @Override
    public List<Category> getCategories() {
        Session session = this.factory.getObject().getCurrentSession();
        return session.createNamedQuery("Category.findAll", Category.class).getResultList();
    }

    @Override
    public Category getCategoryById(int id) {
        Session session = this.factory.getObject().getCurrentSession();
        return session.get(Category.class, id);
    }
}