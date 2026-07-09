package com.ttkp.repositories;

import com.ttkp.pojo.Prescription;
import com.ttkp.pojo.PrescriptionDetail;
import com.ttkp.pojo.PrescriptionItem;
import java.util.List;

public interface PrescriptionRepository {

    List<Prescription> getPrescriptionsByRecordId(int recordId);

    List<PrescriptionDetail> getPrescriptionDetailsByPrescriptionId(
            int prescriptionId
    );

    boolean addPrescription(int recordId, List<PrescriptionItem> items);
}
