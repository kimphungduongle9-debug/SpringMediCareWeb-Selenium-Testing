import requests


class DoctorScheduleApi:

    BASE_URL = "http://localhost:8080/SpringMediCareApp/api"

    def get_schedules(self):
        response = requests.get(
            f"{self.BASE_URL}/doctor-schedules"
        )

        if response.status_code != 200:
            raise Exception(
                "Không lấy được danh sách lịch bác sĩ"
            )

        return response.json()

    def find_schedule(
            self,
            doctor_name,
            work_date,
            shift):

        schedules = self.get_schedules()

        for schedule in schedules:
            doctor = schedule.get(
                "doctorId"
            )

            if (
                    doctor is not None
                    and doctor.get("fullName")
                    == doctor_name
                    and schedule.get("workDate")
                    == work_date
                    and schedule.get("shift")
                    == shift
            ):
                return schedule

        return None

    def get_token(
            self,
            username,
            password):

        response = requests.post(
            f"{self.BASE_URL}/login",
            json={
                "username": username,
                "password": password
            },
            timeout=10
        )

        assert response.status_code == 200, (
            "Không đăng nhập được để lấy token. "
            f"HTTP {response.status_code}: {response.text}"
        )

        return response.json()["token"]

    def delete_schedule(
            self,
            schedule_id,
            token):

        response = requests.delete(
            f"{self.BASE_URL}/secure/doctor-schedules/{schedule_id}",
            headers={
                "Authorization": f"Bearer {token}"
            },
            timeout=10
        )

        if response.status_code not in [200, 204]:
            raise Exception(
                "Không xóa được lịch bác sĩ. "
                f"HTTP {response.status_code}: {response.text}"
            )

    def delete_matching_schedule(
            self,
            doctor_name,
            work_date,
            shift,
            token):

        schedule = self.find_schedule(
            doctor_name,
            work_date,
            shift
        )

        if schedule is None:
            return False

        self.delete_schedule(
            schedule["scheduleId"],
            token
        )
        return True

    def count_matching_schedules(
            self,
            doctor_name,
            work_date,
            shift):

        schedules = self.get_schedules()

        count = 0

        for schedule in schedules:
            doctor = schedule.get(
                "doctorId"
            )

            if (
                    doctor is not None
                    and doctor.get("fullName")
                    == doctor_name
                    and schedule.get("workDate")
                    == work_date
                    and schedule.get("shift")
                    == shift
            ):
                count += 1

        return count

    def get_doctors(self):
        response = requests.get(
            f"{self.BASE_URL}/doctors/all",
            timeout=10
        )

        if response.status_code != 200:
            raise Exception(
                "Không lấy được danh sách bác sĩ. "
                f"HTTP {response.status_code}: "
                f"{response.text}"
            )

        return response.json()

    def find_doctor_id(self, doctor_name):
        doctors = self.get_doctors()

        for doctor in doctors:
            if doctor.get("fullName") == doctor_name:
                return doctor.get("doctorId")

        return None

    def create_schedule(
            self,
            doctor_name,
            work_date,
            shift,
            start_time,
            end_time,
            status,
            note,
            token):

        doctor_id = self.find_doctor_id(
            doctor_name
        )

        if doctor_id is None:
            raise Exception(
                f"Không tìm thấy bác sĩ {doctor_name}"
            )

        response = requests.post(
            f"{self.BASE_URL}/secure/doctor-schedules",
            headers={
                "Authorization": f"Bearer {token}"
            },
            json={
                "doctorId": doctor_id,
                "workDate": work_date,
                "shift": shift,
                "startTime": start_time,
                "endTime": end_time,
                "status": status,
                "note": note
            },
            timeout=10
        )

        if response.status_code not in [200, 201]:
            raise Exception(
                "Không tạo được lịch bác sĩ. "
                f"HTTP {response.status_code}: "
                f"{response.text}"
            )
