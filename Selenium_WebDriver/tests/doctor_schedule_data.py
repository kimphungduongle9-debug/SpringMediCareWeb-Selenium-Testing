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