from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt


# ============================================================
# TEST EXECUTION DATA
# Lưu kết quả các Step trong quá trình pytest thực thi.
# ============================================================

_test_steps = []

_test_results = {}


# ============================================================
# REPORT STEP
# Vừa in kết quả ra terminal,
# vừa lưu lại để cuối phiên test xuất Word.
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
        "detail": detail or ""
    })


# ============================================================
# SAVE TEST CASE RESULT
# Được gọi từ conftest.py sau khi pytest chạy xong từng TC.
# ============================================================

def save_test_result(
        test_case_id,
        status,
        detail=None
):
    """
    Lưu kết quả cuối cùng của một Test Case.

    status:
    - PASSED
    - FAILED
    - XFAILED
    - SKIPPED
    """

    _test_results[test_case_id] = {
        "status": status,
        "detail": detail or ""
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
        cols=3
    )

    result_table.style = "Table Grid"

    headers = result_table.rows[0].cells

    headers[0].text = "Test Case"
    headers[1].text = "Kết quả"
    headers[2].text = "Ghi chú"

    for test_case_id in sorted(_test_results.keys()):
        result = _test_results[test_case_id]

        row = result_table.add_row().cells

        row[0].text = test_case_id
        row[1].text = result["status"]
        row[2].text = result["detail"]

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
        cols=5
    )

    step_table.style = "Table Grid"

    headers = step_table.rows[0].cells

    headers[0].text = "Test Case"
    headers[1].text = "Step"
    headers[2].text = "Kết quả"
    headers[3].text = "Mô tả"
    headers[4].text = "Chi tiết"

    for step in _test_steps:
        row = step_table.add_row().cells

        row[0].text = step["test_case_id"]

        row[1].text = str(
            step["step_number"]
        )

        row[2].text = step["status"]

        row[3].text = step["description"]

        row[4].text = step["detail"]

    document.save(
        output_path
    )

    print(
        "\n============================================================"
    )

    print(
        "WORD TEST REPORT GENERATED:"
    )

    print(
        output_path.resolve()
    )

    print(
        "============================================================"
    )

    return output_path