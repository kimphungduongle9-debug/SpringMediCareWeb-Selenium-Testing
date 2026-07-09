package com.ttkp.services.impl;

import com.ttkp.pojo.Drug;
import com.ttkp.repositories.DrugRepository;
import com.ttkp.services.DrugService;
import java.util.List;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class DrugServiceImpl implements DrugService {

    @Autowired
    private DrugRepository drugRepository;

    @Override
    public List<Drug> getDrugs(Map<String, String> params) {
        return this.drugRepository.getDrugs(params);
    }

    @Override
    public Drug getDrugById(int id) {
        return this.drugRepository.getDrugById(id);
    }

    @Override
    public boolean addOrUpdateDrug(Drug drug) {
        return this.drugRepository.addOrUpdateDrug(drug);
    }

    @Override
    public boolean deleteDrug(int id) {
        return this.drugRepository.deleteDrug(id);
    }

    @Override
    public Long countDrugs() {
        return this.drugRepository.countDrugs();
    }

    @Override
    public List<Object[]> countDrugsByCategory() {
        return this.drugRepository.countDrugsByCategory();
    }

}
