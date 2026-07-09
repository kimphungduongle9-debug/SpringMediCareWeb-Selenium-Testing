package com.ttkp.services.impl;

import com.ttkp.pojo.Prescription;
import com.ttkp.pojo.PrescriptionItem;
import com.ttkp.repositories.PrescriptionRepository;
import com.ttkp.services.PrescriptionService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ttkp.pojo.PrescriptionDetail;
@Service
public class PrescriptionServiceImpl implements PrescriptionService {

    @Autowired
    private PrescriptionRepository prescriptionRepo;

    @Override
    public List<Prescription> getPrescriptionsByRecordId(int recordId) {
        return this.prescriptionRepo.getPrescriptionsByRecordId(recordId);
    }

    @Override
    public List<PrescriptionDetail> getPrescriptionDetailsByPrescriptionId(
            int prescriptionId) {

        return this.prescriptionRepo
                .getPrescriptionDetailsByPrescriptionId(prescriptionId);
    }

    @Override
    public boolean addPrescription(int recordId,
            List<PrescriptionItem> items) {

        return this.prescriptionRepo.addPrescription(recordId, items);
    }
}
