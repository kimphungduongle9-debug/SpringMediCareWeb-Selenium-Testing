from datetime import datetime

import requests


class AppointmentApi:

    BASE_URL = "http://localhost:8080/SpringMediCareApp/api"

    def get_appointments_by_doctor(self, doctor_id):
        response = requests.get(
            f"{self.BASE_URL}/appointments/doctor/{doctor_id}",
            timeout=10
        )

        assert response.status_code == 200, (
            "Không lấy được danh sách lịch hẹn. "
            f"HTTP {response.status_code}: {response.text}"
        )

        return response.json()

    def create_appointment(
            self,
            patient_id,
            doctor_id,
            booking_date,
            booking_time,
            notes="AUTOMATION TEST DATA"):

        appointment_date = datetime.strptime(
            f"{booking_date} {booking_time}",
            "%d/%m/%Y %H:%M"
        ).strftime("%Y-%m-%dT%H:%M:%S")

        response = requests.post(
            f"{self.BASE_URL}/appointments",
            json={
                "patientId": str(patient_id),
                "doctorId": str(doctor_id),
                "appointmentDate": appointment_date,
                "notes": notes
            },
            timeout=10
        )

        assert response.status_code == 201, (
            "Không tạo được dữ liệu lịch hẹn ban đầu. "
            f"HTTP {response.status_code}: {response.text}"
        )
        appointments = self.get_appointments_by_doctor(
            doctor_id
        )

        for appointment in appointments:
            if appointment.get("notes") == notes:
                return appointment

        raise AssertionError(
            "Đã tạo lịch nhưng không tìm thấy "
            "lịch vừa tạo theo ghi chú."
        )

    def cancel_appointment(self, appointment_id):
        response = requests.put(
            f"{self.BASE_URL}/appointments/"
            f"{appointment_id}/cancel",
            timeout=10
        )

        assert response.status_code == 200, (
            "Không hủy được dữ liệu lịch hẹn. "
            f"HTTP {response.status_code}: {response.text}"
        )

    def cancel_matching_appointments(
            self,
            doctor_id,
            booking_date,
            booking_time,
            patient_ids):

        expected_date = datetime.strptime(
            f"{booking_date} {booking_time}",
            "%d/%m/%Y %H:%M"
        )

        appointments = self.get_appointments_by_doctor(
            doctor_id
        )

        for appointment in appointments:
            status = appointment.get(
                "status",
                ""
            ).lower()

            if status == "cancelled":
                continue

            actual_date = self.parse_appointment_date(
                appointment.get("appointmentDate")
            )

            actual_date = actual_date.replace(
                second=0,
                microsecond=0
            )

            if actual_date != expected_date:
                continue

            patient = appointment.get("patientId")

            if isinstance(patient, dict):
                patient_id = patient.get("patientId")
            else:
                patient_id = patient

            if patient_id not in patient_ids:
                continue

            appointment_id = appointment.get(
                "appointmentId"
            )

            self.cancel_appointment(appointment_id)

    @staticmethod
    def parse_appointment_date(value):
        if isinstance(value, (int, float)):
            if value > 100000000000:
                value = value / 1000

            return datetime.fromtimestamp(value)

        if isinstance(value, list):
            year = value[0]
            month = value[1]
            day = value[2]
            hour = value[3]
            minute = value[4]

            return datetime(
                year,
                month,
                day,
                hour,
                minute
            )

        value = str(value).replace(
            "Z",
            "+00:00"
        )

        result = datetime.fromisoformat(value)

        if result.tzinfo is not None:
            result = result.astimezone().replace(
                tzinfo=None
            )

        return result

    def find_appointment_by_note(
            self,
            doctor_id,
            note):
        """
        Tìm lịch hẹn theo ghi chú nhận diện.
        """

        appointments = (
            self.get_appointments_by_doctor(
                doctor_id
            )
        )

        for appointment in appointments:
            if appointment.get("notes") == note:
                return appointment

        raise AssertionError(
            "Không tìm thấy lịch hẹn có ghi chú: "
            + note
        )

