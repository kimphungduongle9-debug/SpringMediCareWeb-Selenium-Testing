package com.ttkp.services;

import com.ttkp.pojo.Prescription;
import com.ttkp.pojo.PrescriptionItem;
import java.util.List;
import com.ttkp.pojo.PrescriptionDetail;

public interface PrescriptionService {

    List<Prescription> getPrescriptionsByRecordId(int recordId);

    List<PrescriptionDetail> getPrescriptionDetailsByPrescriptionId(int prescriptionId);

    boolean addPrescription(int recordId, List<PrescriptionItem> items);
}
