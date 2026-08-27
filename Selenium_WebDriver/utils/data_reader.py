import csv
from pathlib import Path


NOTIFICATION_TEST_DATA_CSV = (
    Path(__file__).resolve().parents[1]
    / "test_data"
    / "notification_test_data.csv"
)


def get_test_data_csv(file_path, test_case_id):
    with open(
        file_path,
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            if row["test_case_id"] == test_case_id:
                return row

    raise ValueError(
        f"Không tìm thấy test case trong CSV: {test_case_id}"
    )