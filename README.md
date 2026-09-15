# SpringMediCareWeb - Selenium Automation Testing

## Giới thiệu

Repository này được xây dựng phục vụ đồ án ngành:

**Kiểm thử tự động cho hệ thống quản lý đặt lịch khám bệnh dùng Selenium WebDriver**

SpringMediCareWeb là hệ thống quản lý đặt lịch khám bệnh do cá nhân xây dựng và được sử dụng làm **đối tượng kiểm thử (System Under Test - SUT)** trong đồ án.

Trọng tâm của project là **Software Testing**, bao gồm thiết kế test case, kiểm thử chức năng, tự động hóa kiểm thử giao diện bằng Selenium WebDriver, ghi nhận kết quả, theo dõi lỗi, retest và thực thi bộ kiểm thử trên GitHub Actions.

---

## Mục tiêu của project

- Khảo sát và xác định các chức năng cần kiểm thử của SpringMediCareWeb.
- Thiết kế test case cho các nghiệp vụ của hệ thống.
- Thực hiện kiểm thử chức năng và ghi nhận kết quả.
- Tự động hóa kiểm thử giao diện bằng Selenium WebDriver.
- Tổ chức mã kiểm thử theo Page Object Model (POM).
- Quản lý dữ liệu kiểm thử bằng CSV.
- Theo dõi lỗi và thực hiện retest sau khi chỉnh sửa.
- Sinh báo cáo kiểm thử theo từng nhóm chức năng và báo cáo tổng hợp.
- Thực thi Selenium Test Suite trên GitHub Actions.

---

## Phạm vi kiểm thử

Bộ kiểm thử tự động hiện gồm:

- **125 test case**
- **14 nhóm chức năng**
- **120 PASS**
- **5 XFAIL**
- **0 FAIL**

Các nhóm chức năng được kiểm thử:

1. Login
2. Register
3. Booking
4. Appointment
5. Doctor Schedule Admin
6. My Appointment
7. Medical
8. Medical History
9. Doctor Work Schedule
10. Notification
11. Doctor
12. Specialty
13. Drug Category
14. Statistics

Các test case bao phủ:

- Luồng nghiệp vụ hợp lệ.
- Validation dữ liệu đầu vào.
- Kiểm tra dữ liệu bắt buộc.
- Kiểm tra quyền truy cập.
- Kiểm tra ràng buộc nghiệp vụ.
- Luồng xử lý giữa Patient, Doctor và Admin.
- Retest sau khi xử lý lỗi.

Các trường hợp còn tồn tại lỗi chức năng đã biết được giữ lại trong bộ kiểm thử và đánh dấu `XFAIL` để phản ánh đúng trạng thái hiện tại của hệ thống.

---

## Công nghệ sử dụng

### Kiểm thử tự động

- Python
- Selenium WebDriver
- Pytest
- Page Object Model (POM)
- CSV Test Data
- Requests
- python-docx
- OpenPyXL

### Hệ thống được kiểm thử

- React
- Spring MVC
- Java 17
- Hibernate
- MySQL
- Tomcat

### Continuous Integration

- Git
- GitHub
- GitHub Actions
- Headless Chrome

---

## Cấu trúc repository

```text
SpringMediCareWeb-Selenium-Testing/
│
├── .github/
│   └── workflows/
│       └── selenium-ci.yml
│
├── Selenium_WebDriver/
│   ├── api/
│   ├── pages/
│   ├── tests/
│   │   ├── appointment/
│   │   ├── booking/
│   │   ├── doctor/
│   │   ├── doctor_schedule_admin/
│   │   ├── drug_category/
│   │   ├── login/
│   │   ├── medical/
│   │   ├── medical_history/
│   │   ├── my_appointment/
│   │   ├── notification/
│   │   ├── register/
│   │   ├── specialty/
│   │   ├── statistics/
│   │   ├── work_schedule/
│   │   └── conftest.py
│   ├── test_data/
│   ├── utils/
│   ├── reports/
│   ├── pytest.ini
│   └── requirements.txt
│
├── SpringMediCareWeb/
│   ├── HibernateDemoMedicCare/
│   ├── SpringMediCareApp/
│   ├── medicareweb/
│   └── medicare_db.sql
│
├── TestCases/
│   ├── Appointment_TestCase.xlsx
│   ├── Booking_TestCase.xlsx
│   ├── Login_TestCase.xlsx
│   ├── Medical_TestCase.xlsx
│   ├── Notification_TestCase.xlsx
│   ├── SpringMediCareWeb_Test_Report.xlsx
│   └── ...
│
├── docs/
│   └── WeeklyReports/
│
└── README.md
```

### Các thành phần chính

- **`Selenium_WebDriver/tests/`**: chứa các test script Selenium theo từng nhóm chức năng.
- **`Selenium_WebDriver/pages/`**: chứa Page Object, locator và các phương thức thao tác với giao diện.
- **`Selenium_WebDriver/test_data/`**: chứa dữ liệu đầu vào phục vụ test case.
- **`Selenium_WebDriver/api/`**: chứa các API helper hỗ trợ chuẩn bị và xử lý dữ liệu cho Selenium test.
- **`Selenium_WebDriver/utils/`**: chứa các thành phần hỗ trợ đọc dữ liệu, ghi nhận kết quả và tạo báo cáo.
- **`Selenium_WebDriver/reports/`**: chứa các báo cáo kết quả sau khi chạy test.
- **`TestCases/`**: chứa các bộ test case và kết quả kiểm thử.
- **`SpringMediCareWeb/`**: chứa mã nguồn của hệ thống được sử dụng làm đối tượng kiểm thử.
- **`docs/WeeklyReports/`**: chứa báo cáo tiến độ đồ án theo tuần.

---

## Tổ chức bộ kiểm thử

Bộ kiểm thử áp dụng **Page Object Model (POM)** để tách thao tác với giao diện khỏi logic của test case.

Các Page Object trong `pages/` quản lý locator và thao tác trên từng màn hình. Các test script trong `tests/` sử dụng Page Object để thực hiện các bước kiểm thử và xác nhận kết quả mong đợi.

Dữ liệu kiểm thử được tách khỏi test script và lưu trong `test_data/`, giúp dữ liệu có thể được quản lý và tái sử dụng.

Các API helper trong `api/` được sử dụng để hỗ trợ chuẩn bị hoặc làm sạch dữ liệu trước và sau khi chạy Selenium test. Các helper này phục vụ UI Automation Testing và không phải phạm vi API Testing chính của project.

---

## Thực thi kiểm thử

Di chuyển vào thư mục:

```bash
cd Selenium_WebDriver
```

Cài đặt các thư viện:

```bash
pip install -r requirements.txt
```

Sau khi SpringMediCareWeb và cơ sở dữ liệu đã được khởi động, chạy toàn bộ Selenium Test Suite:

```bash
python -m pytest -s
```

Chạy riêng một nhóm chức năng, ví dụ Booking:

```bash
python -m pytest -s tests/booking
```

---

## Báo cáo kết quả kiểm thử

Kết quả của lần chạy đầy đủ gần nhất:

| Trạng thái | Số lượng |
|---|---:|
| Total | 125 |
| PASS | 120 |
| XFAIL | 5 |
| FAIL | 0 |

Các báo cáo kết quả được lưu tại:

```text
Selenium_WebDriver/reports/
```

`XFAIL` được sử dụng cho các test case tương ứng với lỗi chức năng đã được xác định nhưng chưa được xử lý tại thời điểm hoàn thành bộ kiểm thử.

---

## GitHub Actions

Project sử dụng **GitHub Actions** để tự động thiết lập môi trường và thực thi Selenium Test Suite.

Workflow:

```text
.github/workflows/selenium-ci.yml
```

Quy trình CI gồm:

1. Khởi tạo MySQL và dữ liệu kiểm thử.
2. Build và khởi động backend.
3. Khởi động frontend.
4. Thiết lập Python và Selenium.
5. Chạy Chrome ở chế độ headless.
6. Thực thi toàn bộ test suite bằng Pytest.
7. Lưu báo cáo kiểm thử dưới dạng workflow artifacts.

Bộ kiểm thử được chạy trên cả môi trường local và GitHub Actions để đối chiếu kết quả và kiểm tra tính ổn định của test suite.

---

## Ghi chú

SpringMediCareWeb được xây dựng để cung cấp hệ thống có nghiệp vụ thực tế phục vụ quá trình thực hành và triển khai kiểm thử trong đồ án.

Trong quá trình kiểm thử, các lỗi phát hiện được ghi nhận, xử lý trên hệ thống và thực hiện retest để xác nhận kết quả sau khi chỉnh sửa.

**Trọng tâm của repository là Software Testing và Selenium Automation Testing; SpringMediCareWeb đóng vai trò là hệ thống được kiểm thử (SUT).**
