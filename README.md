# \# SpringMediCareWeb - Selenium Automation Testing

# 

# \## Giới thiệu

# 

# Repository này được xây dựng phục vụ đồ án ngành:

# 

# \*\*“Kiểm thử tự động cho hệ thống quản lý đặt lịch khám bệnh dùng Selenium WebDriver”\*\*

# 

# SpringMediCareWeb là hệ thống quản lý đặt lịch khám bệnh do cá nhân xây dựng và được sử dụng làm \*\*đối tượng kiểm thử (System Under Test - SUT)\*\* trong đồ án.

# 

# Trọng tâm của project là hoạt động \*\*Software Testing\*\*, bao gồm thiết kế test case, thực hiện kiểm thử chức năng, xây dựng bộ kiểm thử tự động giao diện bằng Selenium WebDriver, ghi nhận kết quả, theo dõi lỗi, retest và thực thi bộ kiểm thử tự động trên GitHub Actions.

# 

# \---

# 

# \## Mục tiêu của project

# 

# \- Khảo sát và xác định các chức năng cần kiểm thử của SpringMediCareWeb.

# \- Thiết kế test case cho các nghiệp vụ của hệ thống.

# \- Thực hiện kiểm thử chức năng và ghi nhận kết quả kiểm thử.

# \- Tự động hóa kiểm thử giao diện web bằng Selenium WebDriver.

# \- Tổ chức mã kiểm thử theo Page Object Model (POM).

# \- Quản lý dữ liệu kiểm thử bằng các file CSV và thành phần hỗ trợ.

# \- Theo dõi lỗi và thực hiện retest sau khi chỉnh sửa.

# \- Sinh báo cáo kết quả theo từng nhóm chức năng và báo cáo tổng hợp.

# \- Thực thi toàn bộ Selenium Test Suite trên môi trường CI bằng GitHub Actions.

# 

# \---

# 

# \## Phạm vi kiểm thử

# 

# Bộ kiểm thử tự động hiện gồm:

# 

# \- \*\*125 test case\*\*

# \- \*\*14 nhóm chức năng\*\*

# \- \*\*120 PASS\*\*

# \- \*\*5 XFAIL\*\*

# \- \*\*0 FAIL\*\*

# 

# Các nhóm chức năng được kiểm thử:

# 

# 1\. Login

# 2\. Register

# 3\. Booking

# 4\. Appointment

# 5\. Doctor Schedule Admin

# 6\. My Appointment

# 7\. Medical

# 8\. Medical History

# 9\. Doctor Work Schedule

# 10\. Notification

# 11\. Doctor

# 12\. Specialty

# 13\. Drug Category

# 14\. Statistics

# 

# Các test case bao phủ các tình huống như:

# 

# \- Luồng nghiệp vụ hợp lệ.

# \- Validation dữ liệu đầu vào.

# \- Kiểm tra các trường dữ liệu bắt buộc.

# \- Kiểm tra quyền truy cập.

# \- Kiểm tra các ràng buộc nghiệp vụ.

# \- Kiểm tra luồng xử lý giữa Patient, Doctor và Admin.

# \- Retest sau khi lỗi được xử lý.

# 

# Các trường hợp còn tồn tại lỗi chức năng đã biết được giữ lại trong bộ kiểm thử và đánh dấu `XFAIL`, giúp kết quả test phản ánh đúng trạng thái hiện tại của hệ thống thay vì loại bỏ các test case này.

# 

# \---

# 

# \## Công nghệ sử dụng

# 

# \### Kiểm thử tự động

# 

# \- Python

# \- Selenium WebDriver

# \- Pytest

# \- Page Object Model (POM)

# \- CSV Test Data

# \- Requests

# \- python-docx

# \- OpenPyXL

# 

# \### Hệ thống được kiểm thử

# 

# \- React

# \- Spring MVC

# \- Java 17

# \- Hibernate

# \- MySQL

# \- Tomcat

# 

# \### Continuous Integration

# 

# \- Git

# \- GitHub

# \- GitHub Actions

# \- Headless Chrome

# 

# \---

# 

# \## Cấu trúc repository

# 

# ```text

# SpringMediCareWeb-Selenium-Testing/

# │

# ├── .github/

# │   └── workflows/

# │       └── selenium-ci.yml

# │

# ├── Selenium\_WebDriver/

# │   ├── api/

# │   │   ├── AppointmentApi.py

# │   │   ├── DoctorScheduleApi.py

# │   │   └── MedicalRecordApi.py

# │   │

# │   ├── pages/

# │   │   ├── BasePage.py

# │   │   ├── LoginPage.py

# │   │   ├── RegisterPage.py

# │   │   ├── BookingPage.py

# │   │   ├── DoctorPage.py

# │   │   ├── MedicalRecordPage.py

# │   │   ├── NotificationPage.py

# │   │   └── ...

# │   │

# │   ├── tests/

# │   │   ├── appointment/

# │   │   ├── booking/

# │   │   ├── doctor/

# │   │   ├── doctor\_schedule\_admin/

# │   │   ├── drug\_category/

# │   │   ├── login/

# │   │   ├── medical/

# │   │   ├── medical\_history/

# │   │   ├── my\_appointment/

# │   │   ├── notification/

# │   │   ├── register/

# │   │   ├── specialty/

# │   │   ├── statistics/

# │   │   ├── work\_schedule/

# │   │   └── conftest.py

# │   │

# │   ├── test\_data/

# │   │   ├── appointment\_test\_data.csv

# │   │   ├── booking\_test\_data.csv

# │   │   ├── login\_test\_data.csv

# │   │   ├── medical\_test\_data.csv

# │   │   ├── notification\_test\_data.csv

# │   │   └── ...

# │   │

# │   ├── utils/

# │   │   ├── data\_reader.py

# │   │   ├── pytest\_report\_hooks.py

# │   │   └── test\_reporter.py

# │   │

# │   ├── reports/

# │   │   ├── Booking\_Test\_Report.docx

# │   │   ├── Login\_Test\_Report.docx

# │   │   ├── Notification\_Test\_Report.docx

# │   │   ├── Overall\_Test\_Report.docx

# │   │   └── ...

# │   │

# │   ├── pytest.ini

# │   └── requirements.txt

# │

# ├── SpringMediCareWeb/

# │   ├── HibernateDemoMedicCare/

# │   ├── SpringMediCareApp/

# │   ├── medicareweb/

# │   └── medicare\_db.sql

# │

# ├── TestCases/

# │   ├── Appointment\_TestCase.xlsx

# │   ├── Booking\_TestCase.xlsx

# │   ├── Login\_TestCase.xlsx

# │   ├── Medical\_TestCase.xlsx

# │   ├── Notification\_TestCase.xlsx

# │   ├── SpringMediCareWeb\_Test\_Report.xlsx

# │   └── ...

# │

# ├── docs/

# │   └── WeeklyReports/

# │       ├── BaoCaoTienDoTuan01\_DoAnNganh\_DuongLeKimPhung.docx

# │       ├── ...

# │       └── BaoCaoTienDoTuan10\_DoAnNganh\_DuongLeKimPhung.docx

# │

# └── README.md

# ```

# 

# \### Các thành phần chính

# 

# \- \*\*`Selenium\_WebDriver/tests/`\*\*: chứa các test script Selenium được tổ chức theo từng nhóm chức năng.

# \- \*\*`Selenium\_WebDriver/pages/`\*\*: chứa các Page Object, locator và phương thức thao tác với giao diện.

# \- \*\*`Selenium\_WebDriver/test\_data/`\*\*: chứa dữ liệu đầu vào phục vụ các test case.

# \- \*\*`Selenium\_WebDriver/api/`\*\*: chứa các API helper được sử dụng để hỗ trợ chuẩn bị hoặc xử lý dữ liệu phục vụ quá trình kiểm thử.

# \- \*\*`Selenium\_WebDriver/utils/`\*\*: chứa các thành phần hỗ trợ đọc dữ liệu, ghi nhận kết quả và tạo báo cáo.

# \- \*\*`Selenium\_WebDriver/reports/`\*\*: chứa báo cáo kết quả được sinh sau khi chạy test.

# \- \*\*`TestCases/`\*\*: chứa các bộ test case và kết quả kiểm thử được lập bằng Excel.

# \- \*\*`SpringMediCareWeb/`\*\*: chứa mã nguồn của hệ thống được sử dụng làm đối tượng kiểm thử.

# \- \*\*`.github/workflows/selenium-ci.yml`\*\*: cấu hình GitHub Actions để thực thi Selenium Test Suite trên môi trường CI.

# \- \*\*`docs/WeeklyReports/`\*\*: chứa các báo cáo tiến độ thực hiện đồ án theo tuần.

# 

# \---

# 

# \## Tổ chức bộ kiểm thử

# 

# Bộ kiểm thử áp dụng \*\*Page Object Model (POM)\*\* để tách phần thao tác với giao diện khỏi logic của test case.

# 

# Các Page Object trong thư mục `pages/` quản lý locator và các thao tác trên từng màn hình. Các test script trong `tests/` sử dụng những Page Object này để thực hiện từng bước kiểm thử và xác nhận kết quả mong đợi.

# 

# Dữ liệu kiểm thử được tách khỏi test script và lưu trong `test\_data/`, giúp dữ liệu có thể được quản lý và tái sử dụng mà không cần viết trực tiếp vào từng test case.

# 

# Một số API helper trong `api/` được sử dụng để hỗ trợ chuẩn bị hoặc làm sạch trạng thái dữ liệu trước và sau khi chạy Selenium test. Các helper này phục vụ cho quá trình UI Automation Testing và không phải là phạm vi kiểm thử API chính của project.

# 

# \---

# 

# \## Thực thi kiểm thử

# 

# Từ thư mục `Selenium\_WebDriver`, cài đặt các thư viện cần thiết:

# 

# ```bash

# pip install -r requirements.txt

# ```

# 

# Sau khi hệ thống SpringMediCareWeb và cơ sở dữ liệu đã được khởi động, chạy toàn bộ Selenium Test Suite:

# 

# ```bash

# python -m pytest -s

# ```

# 

# Có thể chạy riêng một nhóm chức năng, ví dụ Booking:

# 

# ```bash

# python -m pytest -s tests/booking

# ```

# 

# Hoặc chạy một test case cụ thể:

# 

# ```bash

# python -m pytest -s tests/booking/test\_booking\_01\_basic.py::test\_tc\_booking\_001\_success

# ```

# 

# \---

# 

# \## Báo cáo kết quả kiểm thử

# 

# Sau quá trình thực thi, kết quả kiểm thử được tổng hợp thành các báo cáo theo từng nhóm chức năng và báo cáo tổng thể.

# 

# ```text

# Selenium\_WebDriver/reports/

# ```

# 

# Kết quả của lần kiểm thử đầy đủ gần nhất:

# 

# | Trạng thái | Số lượng |

# |---|---:|

# | Total | 125 |

# | PASS | 120 |

# | XFAIL | 5 |

# | FAIL | 0 |

# 

# `XFAIL` được sử dụng cho các test case tương ứng với lỗi chức năng đã được xác định và chưa được xử lý tại thời điểm hoàn thành bộ kiểm thử.

# 

# \---

# 

# \## GitHub Actions

# 

# Project sử dụng \*\*GitHub Actions\*\* để tự động thiết lập môi trường và chạy Selenium Test Suite.

# 

# Workflow chính:

# 

# ```text

# .github/workflows/selenium-ci.yml

# ```

# 

# Quy trình CI bao gồm:

# 

# 1\. Khởi tạo MySQL và dữ liệu kiểm thử.

# 2\. Build và khởi động backend.

# 3\. Khởi động frontend.

# 4\. Thiết lập Python và các thư viện Selenium.

# 5\. Chạy Chrome ở chế độ headless.

# 6\. Thực thi toàn bộ test suite bằng Pytest.

# 7\. Lưu các báo cáo kiểm thử dưới dạng workflow artifacts.

# 

# Bộ kiểm thử được sử dụng để đối chiếu kết quả giữa môi trường local và CI, hỗ trợ kiểm tra tính ổn định của các test case sau khi có thay đổi trong project.

# 

# \---

# 

# \## Ghi chú

# 

# SpringMediCareWeb được xây dựng để cung cấp một hệ thống có nghiệp vụ thực tế phục vụ quá trình thực hành và triển khai kiểm thử trong đồ án.

# 

# Trong quá trình kiểm thử, khi phát hiện lỗi thuộc hệ thống, lỗi được ghi nhận, xử lý trên mã nguồn của hệ thống và thực hiện retest để xác nhận kết quả sau khi chỉnh sửa.

# 

# \*\*Trọng tâm của repository là Software Testing và Selenium Automation Testing; mã nguồn SpringMediCareWeb đóng vai trò là hệ thống được kiểm thử (SUT).\*\*

