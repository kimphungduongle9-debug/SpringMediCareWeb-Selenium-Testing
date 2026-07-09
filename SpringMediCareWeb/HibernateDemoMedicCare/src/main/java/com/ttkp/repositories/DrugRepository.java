package com.ttkp.repositories;

import com.ttkp.pojo.Drug;
import java.util.List;

public interface DrugRepository {

    List<Drug> getDrugs();

    Drug getDrugById(int id);

    boolean addOrUpdateDrug(Drug drug);

    boolean deleteDrug(int id);
}
