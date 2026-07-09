package com.ttkp.services;

import com.ttkp.pojo.Category;
import java.util.List;

public interface CategoryService {

    List<Category> getCategories();

    Category getCategoryById(int id);
}
