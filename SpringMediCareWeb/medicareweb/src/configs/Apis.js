import axios from "axios";
import cookies from "react-cookies";

export const endpoints = {
  doctors: "/doctors",
  login: "/login",
  "current-user": "/secure/profile",
  users: "/users",
  specialties: "/specialties",
  categories: "/drug-categories",
  drugs: "/drugs",
  allDoctors: "/doctors/all",
  doctorByUser: (userId) => `/doctors/user/${userId}`,

  doctorSchedules: "/doctor-schedules",
  doctorScheduleDetail: (id) => `/doctor-schedules/${id}`,
  doctorSchedulesByDoctor: (doctorId) => `/doctors/${doctorId}/schedules`,

  secureDoctorSchedules: "/secure/doctor-schedules",
  secureDoctorScheduleDetail: (id) => `/secure/doctor-schedules/${id}`,

  appointments: "/appointments",
  appointmentsByDoctor: (doctorId) => `/appointments/doctor/${doctorId}`,

  appointmentDetail: (id) => `/appointments/${id}`,

  notificationsByUser: (userId) => `/notifications/user/${userId}`,

  medicalRecords: "/medical-records",
  medicalRecordsByPatient: (patientId) =>
    `/medical-records/patient/${patientId}`,
  medicalRecordDetail: (id) => `/medical-records/${id}`,
  medicalRecordByAppointment: (appointmentId) =>
    `/medical-records/appointment/${appointmentId}`,

  testResultsByMedicalRecord: (recordId) =>
    `/test-results/medical-record/${recordId}`,

  testResults: "/test-results",
  prescriptionsByMedicalRecord: (recordId) =>
    `/prescriptions/medical-record/${recordId}`,

  prescriptionDetailsByPrescription: (prescriptionId) =>
    `/prescription-details/prescription/${prescriptionId}`,

  statisticsPatientsByGender: "/statistics/patients-by-gender",
  statisticsPatientsByAgeGroup: "/statistics/patients-by-age-group",
  statisticsPatientsBySpecialty: "/statistics/patients-by-specialty",
  statisticsPatientsByDiagnosis: "/statistics/patients-by-diagnosis",
  statisticsRevenueTotal: "/statistics/revenue-total",
  statisticsDrugsTotal: "/statistics/drugs-total",
  statisticsDrugsByCategory: "/statistics/drugs-by-category",
  statisticsRevenueByMonth: (year) =>
    `/statistics/revenue-by-month?year=${year}`,
};
export const authApis = () => {
  return axios.create({
    baseURL: "http://localhost:8080/SpringMediCareApp/api/",
    headers: {
      Authorization: `Bearer ${cookies.load("token")}`,
    },
  });
};

export default axios.create({
  baseURL: "http://localhost:8080/SpringMediCareApp/api/",
});
