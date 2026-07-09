package com.ttkp.repositories;

import com.ttkp.pojo.Drug;
import java.util.List;
import java.util.Map;

public interface DrugRepository {

    List<Drug> getDrugs(Map<String, String> params);

    Drug getDrugById(int id);

    boolean addOrUpdateDrug(Drug drug);

    boolean deleteDrug(int id);
    
    public Long countDrugs();
    
    public List<Object[]> countDrugsByCategory();
}
