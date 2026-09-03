from datetime import datetime
from pathlib import Path
import re

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt


PROJECT_ROOT = Path(__file__).resolve().parents[1]


# ============================================================
# TEST EXECUTION DATA
# ============================================================

_test_steps = []
_test_results = {}
_test_cases = {}


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

    Có kiểm tra duplicate để một Step FAIL
    không bị ghi hai lần.
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
# REGISTER TEST CASE
# ============================================================

def register_test_case(
        test_case_id,
        feature_name,
        description=""
):
    """
    Lưu thông tin Test Case để dùng cho report tổng.
    """

    clean_description = description or ""

    description_lines = clean_description.splitlines()

    # Docstring hiện tại thường có:
    #
    # TC-NOTIFICATION-001
    # Kiểm tra Patient...
    #
    # Vì report đã có cột Test Case nên bỏ dòng TC ID
    # khỏi phần Description để tránh hiển thị lặp.
    if (
        description_lines
        and description_lines[0].strip() == test_case_id
    ):
        clean_description = "\n".join(
            description_lines[1:]
        ).strip()

    _test_cases[test_case_id] = {
        "feature": feature_name,
        "description": clean_description
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
    _test_cases.clear()


# ============================================================
# WORD REPORT - REPORT RIÊNG TỪNG CHỨC NĂNG
# ============================================================

def generate_word_report(
        output_path="reports/Notification_Test_Report.docx",
        feature_name="THÔNG BÁO",
        test_case_prefix=None
):
    """
    Xuất báo cáo Word cho một chức năng.

    Nếu có test_case_prefix:
    - Chỉ lấy Test Case thuộc đúng chức năng đó.
    - Chỉ lấy Step thuộc đúng chức năng đó.

    Ví dụ:
    - TC-NOTIFICATION-
    - TC-LOGIN-
    - TC-MEDICAL-
    """

    output_path = Path(output_path)

    if not output_path.is_absolute():
        output_path = PROJECT_ROOT / output_path

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # ========================================================
    # FILTER DATA BY FEATURE
    # ========================================================

    if test_case_prefix:
        filtered_results = {
            test_case_id: result
            for test_case_id, result in _test_results.items()
            if test_case_id.startswith(test_case_prefix)
        }

        filtered_steps = [
            step
            for step in _test_steps
            if step["test_case_id"].startswith(
                test_case_prefix
            )
        ]
    else:
        filtered_results = _test_results
        filtered_steps = _test_steps

    print(
        f"\nREPORT DATA | "
        f"Feature = {feature_name} | "
        f"Total TC = {len(filtered_results)} | "
        f"TC = {sorted(filtered_results.keys())}"
    )

    document = Document()

    # ========================================================
    # TITLE
    # ========================================================

    title = document.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    title_run = title.add_run(
        "BÁO CÁO KẾT QUẢ KIỂM THỬ TỰ ĐỘNG\n"
        f"CHỨC NĂNG {feature_name}"
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
    # 1. SUMMARY
    # ========================================================

    total = len(filtered_results)

    passed = sum(
        1
        for result in filtered_results.values()
        if result["status"] == "PASSED"
    )

    failed = sum(
        1
        for result in filtered_results.values()
        if result["status"] == "FAILED"
    )

    xfailed = sum(
        1
        for result in filtered_results.values()
        if result["status"] == "XFAILED"
    )

    skipped = sum(
        1
        for result in filtered_results.values()
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
    # 2. TEST CASE SUMMARY
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

    for test_case_id in sorted(
        filtered_results.keys()
    ):
        result = filtered_results[
            test_case_id
        ]

        row = result_table.add_row().cells

        row[0].text = test_case_id
        row[1].text = result["status"]
        row[2].text = result["time"]

        duration = result["duration"]

        if duration is None:
            row[3].text = ""
        else:
            row[3].text = f"{duration:.2f}"

        row[4].text = clean_xml_text(
            result["screenshot"]
        )

        row[5].text = clean_xml_text(
            result["detail"]
        )

    document.add_paragraph()

    # ========================================================
    # 3. STEP DETAILS
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

    for step in filtered_steps:
        row = step_table.add_row().cells

        row[0].text = step["test_case_id"]
        row[1].text = str(
            step["step_number"]
        )
        row[2].text = step["status"]
        row[3].text = step["time"]

        row[4].text = clean_xml_text(
            step["description"]
        )

        row[5].text = clean_xml_text(
            step["detail"]
        )

    # ========================================================
    # SAVE REPORT
    # ========================================================

    document.save(
        output_path
    )

    print(
        "\n============================================================"
    )

    print(
        f"WORD TEST REPORT GENERATED | {feature_name}"
    )

    print(
        output_path.resolve()
    )

    print(
        "============================================================"
    )

    return output_path


# ============================================================
# OVERALL TEST REPORT
# ============================================================

def generate_overall_report(
        output_path="reports/Overall_Test_Report.docx"
):
    """
    Xuất báo cáo tổng hợp toàn bộ Selenium Test Suite.

    Report chỉ gồm:
    - Tổng số TC và trạng thái.
    - Tổng hợp theo chức năng.
    - Danh sách TC + mô tả + kết quả.
    - Không hiển thị từng Step.
    """

    output_path = Path(output_path)

    if not output_path.is_absolute():
        output_path = PROJECT_ROOT / output_path

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
        "BÁO CÁO TỔNG HỢP KẾT QUẢ KIỂM THỬ TỰ ĐỘNG\n"
        "SELENIUM TEST SUITE"
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
    # 1. OVERALL SUMMARY
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
    # GROUP TEST CASE BY FEATURE
    # ========================================================

    feature_tests = {}

    for test_case_id, test_case_info in _test_cases.items():

        feature_name = test_case_info["feature"]

        if feature_name not in feature_tests:
            feature_tests[feature_name] = []

        feature_tests[feature_name].append(
            test_case_id
        )

    # ========================================================
    # 2. FEATURE SUMMARY
    # ========================================================

    document.add_heading(
        "2. Tổng hợp theo chức năng",
        level=1
    )

    feature_table = document.add_table(
        rows=1,
        cols=6
    )

    feature_table.style = "Table Grid"

    headers = feature_table.rows[0].cells

    headers[0].text = "Chức năng"
    headers[1].text = "Tổng TC"
    headers[2].text = "Passed"
    headers[3].text = "Failed"
    headers[4].text = "XFailed"
    headers[5].text = "Skipped"

    for feature_name in sorted(
        feature_tests.keys()
    ):
        test_case_ids = feature_tests[
            feature_name
        ]

        feature_results = [
            _test_results[test_case_id]
            for test_case_id in test_case_ids
            if test_case_id in _test_results
        ]

        feature_passed = sum(
            1
            for result in feature_results
            if result["status"] == "PASSED"
        )

        feature_failed = sum(
            1
            for result in feature_results
            if result["status"] == "FAILED"
        )

        feature_xfailed = sum(
            1
            for result in feature_results
            if result["status"] == "XFAILED"
        )

        feature_skipped = sum(
            1
            for result in feature_results
            if result["status"] == "SKIPPED"
        )

        row = feature_table.add_row().cells

        row[0].text = feature_name
        row[1].text = str(
            len(feature_results)
        )
        row[2].text = str(
            feature_passed
        )
        row[3].text = str(
            feature_failed
        )
        row[4].text = str(
            feature_xfailed
        )
        row[5].text = str(
            feature_skipped
        )

    document.add_paragraph()

    # ========================================================
    # 3. TEST CASE DETAILS BY FEATURE
    # ========================================================

    document.add_heading(
        "3. Chi tiết Test Case theo chức năng",
        level=1
    )

    for feature_name in sorted(
        feature_tests.keys()
    ):
        test_case_ids = sorted(
            feature_tests[feature_name]
        )

        document.add_heading(
            feature_name,
            level=2
        )

        feature_results = [
            _test_results[test_case_id]
            for test_case_id in test_case_ids
            if test_case_id in _test_results
        ]

        feature_passed = sum(
            1
            for result in feature_results
            if result["status"] == "PASSED"
        )

        feature_failed = sum(
            1
            for result in feature_results
            if result["status"] == "FAILED"
        )

        feature_xfailed = sum(
            1
            for result in feature_results
            if result["status"] == "XFAILED"
        )

        feature_skipped = sum(
            1
            for result in feature_results
            if result["status"] == "SKIPPED"
        )

        document.add_paragraph(
            f"Tổng Test Case: {len(feature_results)} | "
            f"Passed: {feature_passed} | "
            f"Failed: {feature_failed} | "
            f"XFailed: {feature_xfailed} | "
            f"Skipped: {feature_skipped}"
        )

        table = document.add_table(
            rows=1,
            cols=4
        )

        table.style = "Table Grid"

        headers = table.rows[0].cells

        headers[0].text = "Test Case"
        headers[1].text = "Mô tả"
        headers[2].text = "Kết quả"
        headers[3].text = "Ghi chú"

        for test_case_id in test_case_ids:

            if test_case_id not in _test_results:
                continue

            result = _test_results[
                test_case_id
            ]

            test_case_info = _test_cases.get(
                test_case_id,
                {}
            )

            row = table.add_row().cells

            row[0].text = test_case_id

            row[1].text = clean_xml_text(
                test_case_info.get(
                    "description",
                    ""
                )
            )

            row[2].text = result["status"]

            if result["status"] in (
                "FAILED",
                "XFAILED",
                "SKIPPED"
            ):
                row[3].text = clean_xml_text(
                    result["detail"]
                )
            else:
                row[3].text = ""

        document.add_paragraph()

    # ========================================================
    # SAVE OVERALL REPORT
    # ========================================================

    document.save(
        output_path
    )

    print(
        "\n============================================================"
    )

    print(
        "OVERALL TEST REPORT GENERATED:"
    )

    print(
        output_path.resolve()
    )

    print(
        "============================================================"
    )

    return output_path


# ============================================================
# TEST CASE START
# ============================================================

def report_test_case_start(
        test_case_id,
        description
):
    print()
    print("=" * 70)
    print(test_case_id)
    print(description)
    print("=" * 70)