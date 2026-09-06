from pathlib import Path
from uuid import uuid4

from utils.data_reader import (
    get_test_data_csv,
    REGISTER_TEST_DATA_CSV
)


def get_register_test_data(test_case_id):
    return get_test_data_csv(
        REGISTER_TEST_DATA_CSV,
        test_case_id
    )


def get_avatar_path(file_name):
    return str(
        Path(__file__).resolve().parents[2]
        / "test_data"
        / file_name
    )


def create_unique_value(prefix):
    return f"{prefix}{uuid4().hex[:8]}"