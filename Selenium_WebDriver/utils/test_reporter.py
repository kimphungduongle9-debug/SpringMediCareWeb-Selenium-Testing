from datetime import datetime
from pathlib import Path
import re
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt


# ============================================================
# TEST EXECUTION DATA
# ============================================================

_test_steps = []
_test_results = {}


# ============================================================
# HELPER
# ============================================================

def get_current_time():
    """
    Trả về thời gian hiện tại để ghi vào report.
    """
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def clean_xml_text(value):
    """
    Loại bỏ control characters không hợp lệ với XML/Word.
    """

    if value is None:
        return ""

    text = str(value)

    return re.sub(
        r"[\x00-\x08\x0B\x0C\x0E-\x1F]",
        "",
        text
    )
# ============================================================
# REPORT STEP
# ============================================================

def report_step(
        test_case_id,
        step_number,
        description,
        status="PASS",
        detail=None
):
    """
    Ghi nhận kết quả từng Step.

    Ví dụ:
    TC-NOTIFICATION-001 | STEP 1 | PASS | Patient đặt lịch hợp lệ
    """

    recorded_at = get_current_time()

    message = (
        f"\n{test_case_id} | "
        f"STEP {step_number} | "
        f"{status} | "
        f"{description}"
    )

    if detail:
        message += f" | {detail}"

    print(message)

    _test_steps.append({
        "test_case_id": test_case_id,
        "step_number": step_number,
        "status": status,
        "description": description,
        "detail": detail or "",
        "time": recorded_at
    })


# ============================================================
# REPORT FAILED STEP
# ============================================================

def report_failed_step(
        test_case_id,
        step_number,
        detail
):
    """
    Ghi tự động Step bị FAIL.

    Hàm này được gọi từ conftest.py khi pytest phát hiện
    một Notification Test Case bị lỗi.

    Có kiểm tra duplicate để một Step FAIL không bị ghi 2 lần.
    """

    already_exists = any(
        step["test_case_id"] == test_case_id
        and str(step["step_number"]) == str(step_number)
        and step["status"] == "FAIL"
        for step in _test_steps
    )

    if already_exists:
        return

    report_step(
        test_case_id=test_case_id,
        step_number=step_number,
        description=f"Step {step_number} thực thi thất bại",
        status="FAIL",
        detail=detail
    )


# ============================================================
# SAVE TEST CASE RESULT
# ============================================================

def save_test_result(
        test_case_id,
        status,
        detail=None,
        duration=None,
        screenshot=None
):
    """
    Lưu kết quả cuối cùng của Test Case.

    status:
    - PASSED
    - FAILED
    - XFAILED
    - SKIPPED
    """

    _test_results[test_case_id] = {
        "status": status,
        "detail": detail or "",
        "duration": duration,
        "screenshot": screenshot or "",
        "time": get_current_time()
    }


# ============================================================
# RESET REPORT DATA
# ============================================================

def reset_test_report():
    """
    Xóa dữ liệu report cũ trước một test session mới.
    """

    _test_steps.clear()
    _test_results.clear()


# ============================================================
# WORD REPORT
# ============================================================

def generate_word_report(
        output_path="reports/Notification_Test_Report.docx"
):
    """
    Xuất báo cáo kết quả kiểm thử Notification ra file Word.
    """

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    document = Document()

    # ========================================================
    # TITLE
    # ========================================================

    title = document.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    title_run = title.add_run(
        "BÁO CÁO KẾT QUẢ KIỂM THỬ TỰ ĐỘNG\n"
        "CHỨC NĂNG THÔNG BÁO"
    )

    title_run.bold = True
    title_run.font.size = Pt(16)

    generated_time = document.add_paragraph()
    generated_time.alignment = WD_ALIGN_PARAGRAPH.CENTER
    generated_time.add_run(
        f"Thời gian tạo báo cáo: {get_current_time()}"
    )

    document.add_paragraph()

    # ========================================================
    # SUMMARY
    # ========================================================

    total = len(_test_results)

    passed = sum(
        1
        for result in _test_results.values()
        if result["status"] == "PASSED"
    )

    failed = sum(
        1
        for result in _test_results.values()
        if result["status"] == "FAILED"
    )

    xfailed = sum(
        1
        for result in _test_results.values()
        if result["status"] == "XFAILED"
    )

    skipped = sum(
        1
        for result in _test_results.values()
        if result["status"] == "SKIPPED"
    )

    document.add_heading(
        "1. Tổng quan kết quả",
        level=1
    )

    summary_table = document.add_table(
        rows=1,
        cols=2
    )

    summary_table.style = "Table Grid"

    summary_table.rows[0].cells[0].text = "Nội dung"
    summary_table.rows[0].cells[1].text = "Kết quả"

    summary_data = [
        ("Tổng số Test Case", str(total)),
        ("Passed", str(passed)),
        ("Failed", str(failed)),
        ("XFailed", str(xfailed)),
        ("Skipped", str(skipped))
    ]

    for label, value in summary_data:
        row = summary_table.add_row().cells
        row[0].text = label
        row[1].text = value

    document.add_paragraph()

    # ========================================================
    # TEST CASE SUMMARY
    # ========================================================

    document.add_heading(
        "2. Kết quả từng Test Case",
        level=1
    )

    result_table = document.add_table(
        rows=1,
        cols=6
    )

    result_table.style = "Table Grid"

    headers = result_table.rows[0].cells

    headers[0].text = "Test Case"
    headers[1].text = "Kết quả"
    headers[2].text = "Thời gian"
    headers[3].text = "Duration (s)"
    headers[4].text = "Screenshot"
    headers[5].text = "Ghi chú"

    for test_case_id in sorted(_test_results.keys()):
        result = _test_results[test_case_id]

        row = result_table.add_row().cells

        row[0].text = test_case_id
        row[1].text = result["status"]
        row[2].text = result["time"]

        duration = result["duration"]

        if duration is None:
            row[3].text = ""
        else:
            row[3].text = f"{duration:.2f}"

        row[4].text = clean_xml_text(result["screenshot"])
        row[5].text = clean_xml_text(result["detail"])

    document.add_paragraph()

    # ========================================================
    # STEP DETAILS
    # ========================================================

    document.add_heading(
        "3. Chi tiết thực thi từng Step",
        level=1
    )

    step_table = document.add_table(
        rows=1,
        cols=6
    )

    step_table.style = "Table Grid"

    headers = step_table.rows[0].cells

    headers[0].text = "Test Case"
    headers[1].text = "Step"
    headers[2].text = "Kết quả"
    headers[3].text = "Thời gian"
    headers[4].text = "Mô tả"
    headers[5].text = "Chi tiết"

    for step in _test_steps:
        row = step_table.add_row().cells

        row[0].text = step["test_case_id"]
        row[1].text = str(step["step_number"])
        row[2].text = step["status"]
        row[3].text = step["time"]
        row[4].text = clean_xml_text(step["description"])
        row[5].text = clean_xml_text(step["detail"])

    document.save(output_path)

    print(
        "\n============================================================"
    )
    print("WORD TEST REPORT GENERATED:")
    print(output_path.resolve())
    print(
        "============================================================"
    )

    return output_path