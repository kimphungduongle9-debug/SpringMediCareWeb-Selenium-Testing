from datetime import datetime, timedelta

import requests


class MedicalRecordApi:

    BASE_URL = "http://localhost:8080/SpringMediCareApp/api"

    TEST_NOTE = "SELENIUM-TC-MEDICAL-007"

    def get_doctor_schedules(self, doctor_id):
        response = requests.get(
            f"{self.BASE_URL}/doctors/{doctor_id}/schedules",
            timeout=10
        )

        assert response.status_code == 200, (
            "Không lấy được lịch làm việc của bác sĩ. "
            f"HTTP {response.status_code}: {response.text}"
        )

        return response.json()

    def get_appointments_by_doctor(self, doctor_id):
        response = requests.get(
            f"{self.BASE_URL}/appointments/doctor/{doctor_id}",
            timeout=10
        )

        assert response.status_code == 200, (
            "Không lấy được danh sách lịch hẹn của bác sĩ. "
            f"HTTP {response.status_code}: {response.text}"
        )

        return response.json()

    @staticmethod
    def parse_work_date(value):
        """
        Chuyển workDate từ API thành ngày Python.
        API có thể trả milliseconds, list hoặc chuỗi ngày.
        """

        if isinstance(value, (int, float)):
            if value > 100000000000:
                value = value / 1000

            return datetime.fromtimestamp(value).date()

        if isinstance(value, list):
            return datetime(
                value[0],
                value[1],
                value[2]
            ).date()

        value = str(value).replace(
            "Z",
            "+00:00"
        )

        result = datetime.fromisoformat(value)

        if result.tzinfo is not None:
            result = result.astimezone().replace(
                tzinfo=None
            )

        return result.date()

    @staticmethod
    def parse_appointment_date(value):
        """
        Chuyển appointmentDate từ API thành datetime.
        """

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

    @staticmethod
    def get_related_id(value, id_field):
        """
        API có thể trả ID theo hai dạng:
        - Object, ví dụ: {"patientId": 7, ...}
        - Số ID trực tiếp.
        """

        if isinstance(value, dict):
            return value.get(id_field)

        return value

    def get_available_future_schedules(self, doctor_id):
        """
        Lấy tất cả ca làm việc available trong tương lai,
        sắp xếp từ gần nhất đến xa nhất.
        """

        schedules = self.get_doctor_schedules(
            doctor_id
        )

        tomorrow = (
            datetime.now() + timedelta(days=1)
        ).date()

        available_schedules = []

        for schedule in schedules:
            status = schedule.get(
                "status",
                ""
            ).lower()

            if status != "available":
                continue

            work_date = self.parse_work_date(
                schedule.get("workDate")
            )

            if work_date < tomorrow:
                continue

            available_schedules.append({
                **schedule,
                "_parsed_work_date": work_date
            })

        available_schedules.sort(
            key=lambda item: (
                item["_parsed_work_date"],
                item.get("startTime", "")
            )
        )

        assert available_schedules, (
            "Không tìm thấy ca làm việc available "
            "trong tương lai của bác sĩ."
        )

        return available_schedules

    def find_available_booking_slot(self, doctor_id):
        """
        Tìm một giờ đặt lịch hợp lệ:
        - Nằm trong ca làm việc available.
        - Không trùng lịch hiện có.
        - Cách lịch hiện có ít nhất 30 phút.
        """

        schedules = self.get_available_future_schedules(
            doctor_id
        )

        appointments = self.get_appointments_by_doctor(
            doctor_id
        )

        occupied_times = []

        for appointment in appointments:
            status = appointment.get(
                "status",
                ""
            ).lower()

            if status in ["cancelled", "canceled"]:
                continue

            appointment_date = appointment.get(
                "appointmentDate"
            )

            if appointment_date is None:
                continue

            occupied_times.append(
                self.parse_appointment_date(
                    appointment_date
                )
            )

        for schedule in schedules:
            work_date = schedule[
                "_parsed_work_date"
            ]

            start_time = datetime.strptime(
                schedule.get("startTime"),
                "%H:%M:%S"
            ).time()

            end_time = datetime.strptime(
                schedule.get("endTime"),
                "%H:%M:%S"
            ).time()

            candidate = datetime.combine(
                work_date,
                start_time
            )

            schedule_end = datetime.combine(
                work_date,
                end_time
            )

            while candidate < schedule_end:
                has_conflict = any(
                    abs(
                        (
                            candidate - occupied_time
                        ).total_seconds()
                    ) < 30 * 60
                    for occupied_time in occupied_times
                )

                if not has_conflict:
                    return {
                        "booking_date": candidate.strftime(
                            "%d/%m/%Y"
                        ),
                        "booking_time": candidate.strftime(
                            "%H:%M"
                        )
                    }

                candidate += timedelta(
                    minutes=30
                )

        raise AssertionError(
            "Không tìm thấy giờ đặt lịch còn trống "
            "trong các ca làm việc của bác sĩ."
        )

    def find_created_appointment(
            self,
            doctor_id,
            patient_id,
            booking_date,
            booking_time,
            notes):
        """
        Tìm lại lịch vừa tạo để lấy appointmentId.
        """

        expected_date = datetime.strptime(
            f"{booking_date} {booking_time}",
            "%d/%m/%Y %H:%M"
        )

        appointments = self.get_appointments_by_doctor(
            doctor_id
        )

        matching_appointments = []

        for appointment in appointments:
            actual_notes = (
                appointment.get("notes")
                or appointment.get("note")
                or ""
            )

            if actual_notes != notes:
                continue

            actual_patient_id = self.get_related_id(
                appointment.get("patientId"),
                "patientId"
            )

            if actual_patient_id != patient_id:
                continue

            appointment_date = appointment.get(
                "appointmentDate"
            )

            if appointment_date is None:
                continue

            actual_date = self.parse_appointment_date(
                appointment_date
            ).replace(
                second=0,
                microsecond=0
            )

            if actual_date != expected_date:
                continue

            matching_appointments.append(
                appointment
            )

        assert matching_appointments, (
            "Đã tạo lịch nhưng không tìm lại được "
            "appointmentId tương ứng."
        )

        matching_appointments.sort(
            key=lambda item: item.get(
                "appointmentId",
                0
            ),
            reverse=True
        )

        return matching_appointments[0]

    def create_appointment(
            self,
            patient_id,
            doctor_id,
            booking_date,
            booking_time,
            notes=TEST_NOTE):
        """
        Tạo lịch hẹn bằng API và trả về lịch vừa tạo.
        """

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
            "Không tạo được lịch hẹn chuẩn bị cho Selenium. "
            f"HTTP {response.status_code}: {response.text}"
        )

        return self.find_created_appointment(
            doctor_id=doctor_id,
            patient_id=patient_id,
            booking_date=booking_date,
            booking_time=booking_time,
            notes=notes
        )

    def confirm_appointment(self, appointment_id):
        """
        Chuyển lịch từ pending sang confirmed.
        """

        response = requests.put(
            f"{self.BASE_URL}/appointments/"
            f"{appointment_id}/confirm",
            timeout=10
        )

        assert response.status_code == 200, (
            "Không xác nhận được lịch hẹn chuẩn bị "
            "cho Selenium. "
            f"HTTP {response.status_code}: {response.text}"
        )
    def create_medical_record(
            self,
            appointment_id,
            diagnosis="Chẩn đoán Selenium TC-MEDICAL-007",
            treatment="Điều trị Selenium TC-MEDICAL-007"):
        """
        Tạo hồ sơ bệnh án cho lịch đã được xác nhận.
        Khi tạo thành công, lịch sẽ chuyển sang completed.
        """

        response = requests.post(
            f"{self.BASE_URL}/medical-records",
            json={
                "appointmentId": str(appointment_id),
                "diagnosis": diagnosis,
                "treatment": treatment
            },
            timeout=10
        )

        assert response.status_code == 201, (
            "Không tạo được hồ sơ bệnh án chuẩn bị "
            "cho Selenium. "
            f"HTTP {response.status_code}: {response.text}"
        )

    def get_medical_record_by_appointment(
            self,
            appointment_id):
        """
        Lấy hồ sơ bệnh án theo appointmentId.
        """

        response = requests.get(
            f"{self.BASE_URL}/medical-records/"
            f"appointment/{appointment_id}",
            timeout=10
        )

        assert response.status_code == 200, (
            "Không lấy được hồ sơ bệnh án. "
            f"HTTP {response.status_code}: {response.text}"
        )

        return response.json()

    def get_appointment_by_id(
            self,
            doctor_id,
            appointment_id):
        """
        Tìm lịch theo appointmentId trong danh sách
        lịch của bác sĩ.
        """

        appointments = self.get_appointments_by_doctor(
            doctor_id
        )

        for appointment in appointments:
            actual_appointment_id = appointment.get(
                "appointmentId"
            )

            if actual_appointment_id == appointment_id:
                return appointment

        return None

    def assert_appointment_status(
            self,
            doctor_id,
            appointment_id,
            expected_status):
        """
        Kiểm tra lịch đã chuyển đúng trạng thái.
        """

        appointment = self.get_appointment_by_id(
            doctor_id,
            appointment_id
        )

        assert appointment is not None, (
            f"Không tìm thấy lịch ID {appointment_id}."
        )

        actual_status = appointment.get(
            "status",
            ""
        ).lower()

        assert actual_status == expected_status.lower(), (
            "Trạng thái lịch không đúng. "
            f"Mong đợi: {expected_status}, "
            f"thực tế: {actual_status}"
        )

    def find_reusable_appointment(
            self,
            doctor_id,
            patient_id,
            notes=TEST_NOTE):
        """
        Tìm dữ liệu Selenium đã tạo ở lần chạy trước.

        Chỉ sử dụng lại lịch khi:
        - Đúng bác sĩ.
        - Đúng bệnh nhân.
        - Đúng ghi chú Selenium.
        - Lịch đã hoàn thành.
        """

        appointments = self.get_appointments_by_doctor(
            doctor_id
        )

        matching_appointments = []

        for appointment in appointments:
            actual_notes = (
                appointment.get("notes")
                or appointment.get("note")
                or ""
            )

            if actual_notes != notes:
                continue

            status = appointment.get(
                "status",
                ""
            ).lower()

            if status != "completed":
                continue

            actual_patient_id = self.get_related_id(
                appointment.get("patientId"),
                "patientId"
            )

            if actual_patient_id != patient_id:
                continue

            matching_appointments.append(
                appointment
            )

        if not matching_appointments:
            return None

        matching_appointments.sort(
            key=lambda item: item.get(
                "appointmentId",
                0
            ),
            reverse=True
        )

        return matching_appointments[0]

    def prepare_completed_medical_record(
            self,
            patient_id,
            doctor_id,
            notes,
            diagnosis,
            treatment):
        """
        Chuẩn bị một lịch đã hoàn thành và có hồ sơ bệnh án.
        Nếu dữ liệu đã tồn tại thì sử dụng lại.
        """

        reusable_appointment = (
            self.find_reusable_appointment(
                doctor_id=doctor_id,
                patient_id=patient_id,
                notes=notes
            )
        )

        if reusable_appointment is not None:
            return reusable_appointment[
                "appointmentId"
            ]

        booking_slot = (
            self.find_available_booking_slot(
                doctor_id
            )
        )

        appointment = self.create_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            booking_date=booking_slot[
                "booking_date"
            ],
            booking_time=booking_slot[
                "booking_time"
            ],
            notes=notes
        )

        appointment_id = appointment[
            "appointmentId"
        ]

        self.confirm_appointment(
            appointment_id
        )

        self.assert_appointment_status(
            doctor_id=doctor_id,
            appointment_id=appointment_id,
            expected_status="confirmed"
        )

        self.create_medical_record(
            appointment_id=appointment_id,
            diagnosis=diagnosis,
            treatment=treatment
        )

        self.assert_appointment_status(
            doctor_id=doctor_id,
            appointment_id=appointment_id,
            expected_status="completed"
        )

        return appointment_id

    def prepare_tc7_data(
            self,
            patient_id,
            doctor_id):
        return self.prepare_completed_medical_record(
            patient_id=patient_id,
            doctor_id=doctor_id,
            notes="SELENIUM-TC-MEDICAL-007",
            diagnosis=(
                "Chẩn đoán Selenium TC-MEDICAL-007"
            ),
            treatment=(
                "Điều trị Selenium TC-MEDICAL-007"
            )
        )

    def prepare_tc5_data(
            self,
            patient_id,
            doctor_id):
        return self.prepare_completed_medical_record(
            patient_id=patient_id,
            doctor_id=doctor_id,
            notes="SELENIUM-TC-MEDICAL-005",
            diagnosis=(
                "Đau lưng do ngồi lâu"
            ),
            treatment=(
                "Nghỉ ngơi và hạn chế vận động mạnh"
            )
        )

    def prepare_tc6_data(
            self,
            patient_id,
            doctor_id):
        return self.prepare_completed_medical_record(
            patient_id=patient_id,
            doctor_id=doctor_id,
            notes="SELENIUM-TC-MEDICAL-006",
            diagnosis=(
                "Chẩn đoán ban đầu TC-MEDICAL-006"
            ),
            treatment=(
                "Hướng điều trị ban đầu TC-MEDICAL-006"
            )
        )

    def prepare_tc9_data(
            self,
            patient_id,
            doctor_id):
        return self.prepare_completed_medical_record(
            patient_id=patient_id,
            doctor_id=doctor_id,
            notes="SELENIUM-TC-MEDICAL-009",
            diagnosis=(
                "Chẩn đoán ban đầu TC-MEDICAL-009"
            ),
            treatment=(
                "Hướng điều trị ban đầu TC-MEDICAL-009"
            )
        )

    def find_confirmed_appointment(
            self,
            doctor_id,
            patient_id,
            notes):
        """
        Tìm lịch đã xác nhận để có thể khám bệnh.
        """

        appointments = (
            self.get_appointments_by_doctor(
                doctor_id
            )
        )

        for appointment in appointments:
            patient = appointment.get(
                "patientId"
            )

            if isinstance(patient, dict):
                appointment_patient_id = (
                    patient.get("patientId")
                )
            else:
                appointment_patient_id = patient

            if (
                appointment_patient_id == patient_id
                and appointment.get("notes") == notes
                and appointment.get("status")
                == "confirmed"
            ):
                return appointment

        return None

    def prepare_confirmed_appointment(
            self,
            patient_id,
            doctor_id,
            notes):
        """
        Chuẩn bị lịch đã xác nhận,
        chưa có hồ sơ bệnh án.
        """

        appointment = (
            self.find_confirmed_appointment(
                doctor_id=doctor_id,
                patient_id=patient_id,
                notes=notes
            )
        )

        if appointment is not None:
            return appointment["appointmentId"]

        booking_slot = (
            self.find_available_booking_slot(
                doctor_id
            )
        )

        appointment = self.create_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            booking_date=booking_slot[
                "booking_date"
            ],
            booking_time=booking_slot[
                "booking_time"
            ],
            notes=notes
        )

        appointment_id = appointment[
            "appointmentId"
        ]

        self.confirm_appointment(
            appointment_id
        )

        self.assert_appointment_status(
            doctor_id=doctor_id,
            appointment_id=appointment_id,
            expected_status="confirmed"
        )

        return appointment_id

    def prepare_tc1_data(
            self,
            patient_id,
            doctor_id):
        return self.prepare_confirmed_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            notes="SELENIUM-TC-MEDICAL-001"
        )

    def prepare_tc2_data(
            self,
            patient_id,
            doctor_id):
        return self.prepare_confirmed_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            notes="SELENIUM-TC-MEDICAL-002"
        )

    def prepare_tc3_data(
            self,
            patient_id,
            doctor_id):
        return self.prepare_confirmed_appointment(
            patient_id=patient_id,
            doctor_id=doctor_id,
            notes="SELENIUM-TC-MEDICAL-003"
        )

    def prepare_tc4_data(
            self,
            patient_id,
            doctor_id):
        return self.prepare_completed_medical_record(
            patient_id=patient_id,
            doctor_id=doctor_id,
            notes="SELENIUM-TC-MEDICAL-004",
            diagnosis=(
                "Chẩn đoán TC-MEDICAL-004"
            ),
            treatment=(
                "Hướng điều trị TC-MEDICAL-004"
            )
        )

    def prepare_tc8_data(
            self,
            patient_id,
            doctor_id):
        return self.prepare_completed_medical_record(
            patient_id=patient_id,
            doctor_id=doctor_id,
            notes="SELENIUM-TC-MEDICAL-008",
            diagnosis=(
                "Chẩn đoán TC-MEDICAL-008"
            ),
            treatment=(
                "Hướng điều trị TC-MEDICAL-008"
            )
        )