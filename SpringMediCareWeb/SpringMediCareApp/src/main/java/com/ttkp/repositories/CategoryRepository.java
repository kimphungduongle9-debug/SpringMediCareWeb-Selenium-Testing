package com.ttkp.repositories;

import com.ttkp.pojo.Category;
import java.util.List;

public interface CategoryRepository {

    List<Category> getCategories();

    Category getCategoryById(int id);
}
