package com.ttkp.formatters;

import com.ttkp.pojo.Doctor;
import java.text.ParseException;
import java.util.Locale;
import org.springframework.format.Formatter;

public class DoctorFormatter implements Formatter<Doctor> {

    @Override
    public String print(Doctor doctor, Locale locale) {
        return String.valueOf(doctor.getDoctorId());
    }

    @Override
    public Doctor parse(String doctorId, Locale locale) throws ParseException {
        Doctor d = new Doctor();
        d.setDoctorId(Integer.valueOf(doctorId));
        return d;
    }
}
