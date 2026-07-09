package com.ttkp.services;

import com.ttkp.pojo.Drug;
import java.util.List;
import java.util.Map;

public interface DrugService {

    List<Drug> getDrugs(Map<String, String> params);

    Drug getDrugById(int id);

    boolean addOrUpdateDrug(Drug drug);

    boolean deleteDrug(int id);
    
    public Long countDrugs();
    public List<Object[]> countDrugsByCategory();
}
