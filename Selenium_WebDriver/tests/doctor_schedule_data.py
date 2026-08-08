import pytest

from api.DoctorScheduleApi import DoctorScheduleApi


ADMIN_USERNAME = "admin_system"
ADMIN_PASSWORD = "Abc@123"


@pytest.fixture
def doctor_schedule_tc2_data():
    schedule_api = DoctorScheduleApi()

    token = schedule_api.get_token(
        ADMIN_USERNAME,
        ADMIN_PASSWORD
    )

    doctor_name = "Tran Binh"
    work_date = "2026-08-08"
    shift = "morning"

    # Dọn lịch cũ trước khi chạy TC002
    schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    )

    yield {
        "doctor_name": doctor_name,
        "work_date_api": work_date,
        "work_date_list": "08/08/2026",
        "work_date_week": "8/8/2026",
        "shift_value": shift,
        "shift_name": "Ca sáng",
        "shift_form": "Ca sáng: 07:00 - 11:30",
        "status_form": "Có lịch làm việc",
        "status_display": "Có lịch",
        "note": "Ca sáng"
    }

    # Dọn lịch TC002 sau khi test kết thúc
    schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    )
@pytest.fixture
def doctor_schedule_tc3_data():
    schedule_api = DoctorScheduleApi()

    token = schedule_api.get_token(
        ADMIN_USERNAME,
        ADMIN_PASSWORD
    )

    doctor_name = "Tran Binh"
    work_date = "2026-08-08"
    shift = "evening"

    # Dọn lịch cũ trước khi chạy TC003
    schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    )

    yield {
        "doctor_name": doctor_name,
        "work_date_list": "08/08/2026",
        "shift_name": "Ca tối",
        "shift_form": "Ca tối: 17:30 - 21:00",
        "status_form": "Không làm việc",
        "status_display": "Không làm",
        "note": "Không trực"
    }

    # Dọn lịch TC003 sau khi test kết thúc
    schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    )
@pytest.fixture
def doctor_schedule_tc4_data():
    schedule_api = DoctorScheduleApi()

    token = schedule_api.get_token(
        ADMIN_USERNAME,
        ADMIN_PASSWORD
    )

    doctor_name = "Tran Binh"
    work_date = "2026-08-08"
    shift = "evening"

    schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    )

    yield {
        "doctor_name": doctor_name,
        "work_date_list": "08/08/2026",
        "shift_name": "Ca tối",
        "shift_form": "Ca tối: 17:30 - 21:00",
        "status_form": "Có lịch làm việc",
        "status_display": "Có lịch",
        "note": ""
    }

    schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    )
@pytest.fixture
def doctor_schedule_tc7_data():
    schedule_api = DoctorScheduleApi()

    token = schedule_api.get_token(
        ADMIN_USERNAME,
        ADMIN_PASSWORD
    )

    doctor_name = "Tran Binh"
    work_date = "2026-08-01"
    shift = "morning"

    while schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    ):
        pass

    yield {
        "doctor_name": doctor_name,
        "work_date_list": "01/08/2026",
        "shift_name": "Ca sáng",
        "status_display": "Có lịch",
        "note": "Ca sáng"
    }

    while schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    ):
        pass

@pytest.fixture
def doctor_schedule_tc8_data():
    schedule_api = DoctorScheduleApi()

    token = schedule_api.get_token(
        ADMIN_USERNAME,
        ADMIN_PASSWORD
    )

    doctor_name = "Tran Binh"
    work_date = "2026-08-08"
    shift = "evening"

    while schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    ):
        pass

    yield {
        "schedule_api": schedule_api,
        "doctor_name": doctor_name,
        "work_date_api": work_date,
        "work_date_list": "08/08/2026",
        "shift_form": "Ca tối: 17:30 - 21:00",
        "status_form": "Có lịch làm việc",
        "note": "Ca tối"
    }

    while schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    ):
        pass

@pytest.fixture
def doctor_schedule_tc9_data():
    schedule_api = DoctorScheduleApi()

    token = schedule_api.get_token(
        ADMIN_USERNAME,
        ADMIN_PASSWORD
    )

    doctor_name = "Tran Binh"
    work_date = "2026-08-08"

    for shift in ["afternoon", "evening"]:
        while schedule_api.delete_matching_schedule(
            doctor_name=doctor_name,
            work_date=work_date,
            shift=shift,
            token=token
        ):
            pass

    yield {
        "schedule_api": schedule_api,
        "doctor_name": doctor_name,
        "work_date_api": work_date,
        "work_date_list": "08/08/2026",
        "status_form": "Có lịch làm việc",
        "status_display": "Có lịch"
    }

    for shift in ["afternoon", "evening"]:
        while schedule_api.delete_matching_schedule(
            doctor_name=doctor_name,
            work_date=work_date,
            shift=shift,
            token=token
        ):
            pass

@pytest.fixture
def doctor_schedule_tc10_data():
    schedule_api = DoctorScheduleApi()

    token = schedule_api.get_token(
        ADMIN_USERNAME,
        ADMIN_PASSWORD
    )

    work_date = "2026-08-08"
    shift = "morning"

    doctors = [
        "Tran Binh",
        "Ly Minh"
    ]

    for doctor_name in doctors:
        while schedule_api.delete_matching_schedule(
            doctor_name=doctor_name,
            work_date=work_date,
            shift=shift,
            token=token
        ):
            pass

    yield {
        "schedule_api": schedule_api,
        "work_date_api": work_date,
        "work_date_list": "08/08/2026",
        "work_date_week": "8/8/2026",
        "shift_name": "Ca sáng",
        "shift_form": "Ca sáng: 07:00 - 11:30",
        "status_form": "Có lịch làm việc",
        "status_display": "Có lịch"
    }

    for doctor_name in doctors:
        while schedule_api.delete_matching_schedule(
            doctor_name=doctor_name,
            work_date=work_date,
            shift=shift,
            token=token
        ):
            pass
@pytest.fixture
def doctor_schedule_tc11_data():
    schedule_api = DoctorScheduleApi()

    token = schedule_api.get_token(
        ADMIN_USERNAME,
        ADMIN_PASSWORD
    )

    doctor_name = "Tran Binh"
    work_date = "2026-08-08"
    shift = "morning"

    while schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    ):
        pass

    yield {
        "schedule_api": schedule_api,
        "doctor_name": doctor_name,
        "work_date_api": work_date,
        "work_date_list": "08/08/2026",
        "shift_form": "Ca sáng: 07:00 - 11:30",
        "shift_name": "Ca sáng"
    }

    while schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    ):
        pass

@pytest.fixture
def doctor_schedule_tc12_data():
    schedule_api = DoctorScheduleApi()

    token = schedule_api.get_token(
        ADMIN_USERNAME,
        ADMIN_PASSWORD
    )

    doctor_name = "Tran Binh"
    work_date = "2026-08-08"
    shift = "afternoon"

    while schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    ):
        pass

    yield {
        "schedule_api": schedule_api,
        "doctor_name": doctor_name,
        "work_date_api": work_date,
        "work_date_list": "08/08/2026",
        "shift_form": "Ca chiều: 13:00 - 17:00",
        "shift_name": "Ca chiều",
        "status_form": "Có lịch làm việc",
        "status_display": "Có lịch",
        "note": "TC12 click nhiều lần"
    }

    while schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    ):
        pass

@pytest.fixture
def doctor_schedule_tc13_data():
    schedule_api = DoctorScheduleApi()

    token = schedule_api.get_token(
        ADMIN_USERNAME,
        ADMIN_PASSWORD
    )

    doctor_name = "Pham Dung"
    work_date = "2026-08-08"
    shift = "evening"

    while schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    ):
        pass

    yield {
        "schedule_api": schedule_api,
        "doctor_name": doctor_name,
        "work_date_api": work_date,
        "work_date_list": "08/08/2026",
        "shift_form": "Ca tối: 17:30 - 21:00",
        "shift_name": "Ca tối",
        "status_form": "Không làm việc",
        "status_display": "Không làm",
        "note": "TC13 kiểm tra reset form"
    }

    while schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    ):
        pass

@pytest.fixture
def doctor_schedule_tc18_data():
    schedule_api = DoctorScheduleApi()

    token = schedule_api.get_token(
        ADMIN_USERNAME,
        ADMIN_PASSWORD
    )

    doctor_name = "Tran Binh"
    work_date = "2026-08-09"
    shift = "evening"

    while schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    ):
        pass

    schedule_api.create_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        start_time="17:30:00",
        end_time="21:00:00",
        status="available",
        note="TC18 trước cập nhật",
        token=token
    )

    created_schedule = schedule_api.find_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift
    )

    assert created_schedule is not None

    yield {
        "schedule_api": schedule_api,
        "schedule_id": created_schedule[
            "scheduleId"
        ],
        "doctor_name": doctor_name,
        "work_date_api": work_date,
        "work_date_list": "09/08/2026",
        "work_date_week": "9/8/2026",
        "shift_value": shift,
        "shift_name": "Ca tối",
        "shift_form": "Ca tối: 17:30 - 21:00",

        "status_before_form": "Có lịch làm việc",
        "status_before_display": "Có lịch",
        "note_before": "TC18 trước cập nhật",

        "status_after_form": "Không làm việc",
        "status_after_display": "Không làm",
        "note_after": "Nghỉ"
    }

    while schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    ):
        pass

@pytest.fixture
def doctor_schedule_tc19_data():
    schedule_api = DoctorScheduleApi()

    token = schedule_api.get_token(
        ADMIN_USERNAME,
        ADMIN_PASSWORD
    )

    doctor_name = "Tran Binh"
    work_date = "2026-08-10"
    shift = "afternoon"

    while schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    ):
        pass

    schedule_api.create_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        start_time="13:00:00",
        end_time="17:00:00",
        status="available",
        note="TC19 trước hủy",
        token=token
    )

    created_schedule = schedule_api.find_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift
    )

    assert created_schedule is not None

    yield {
        "schedule_api": schedule_api,
        "schedule_id": created_schedule[
            "scheduleId"
        ],

        "doctor_name": doctor_name,
        "work_date_api": work_date,
        "work_date_list": "10/08/2026",

        "shift_value": shift,
        "shift_name": "Ca chiều",
        "shift_form": "Ca chiều: 13:00 - 17:00",

        "status_before_form": "Có lịch làm việc",
        "status_before_display": "Có lịch",
        "note_before": "TC19 trước hủy",

        "status_changed_form": "Không làm việc",
        "note_changed": "TC19 thay đổi chưa lưu"
    }

    while schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    ):
        pass

@pytest.fixture
def doctor_schedule_tc20_data():
    schedule_api = DoctorScheduleApi()

    token = schedule_api.get_token(
        ADMIN_USERNAME,
        ADMIN_PASSWORD
    )

    doctor_name = "Pham Dung"
    work_date = "2026-08-11"
    shift = "morning"

    while schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    ):
        pass

    schedule_api.create_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        start_time="07:00:00",
        end_time="11:30:00",
        status="available",
        note="TC20 xóa lịch",
        token=token
    )

    created_schedule = schedule_api.find_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift
    )

    assert created_schedule is not None

    yield {
        "schedule_api": schedule_api,
        "token": token,

        "schedule_id": created_schedule[
            "scheduleId"
        ],

        "doctor_name": doctor_name,
        "work_date_api": work_date,
        "work_date_list": "11/08/2026",
        "work_date_week": "11/8/2026",

        "shift_value": shift,
        "shift_name": "Ca sáng",

        "status_display": "Có lịch",
        "note": "TC20 xóa lịch"
    }
    while schedule_api.delete_matching_schedule(
        doctor_name=doctor_name,
        work_date=work_date,
        shift=shift,
        token=token
    ):
        pass