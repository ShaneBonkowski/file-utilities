import pytest
from pathlib import Path
from typing import Union


TEST_DATA_DIR = Path(__file__).parent / "test_data"


@pytest.fixture
def compare_file_bytes():
    """Fixture for comparing two files by their byte data."""

    def _compare(file_path_1: Union[str, Path], file_path_2: Union[str, Path]) -> bool:
        file_path_1 = Path(file_path_1)
        file_path_2 = Path(file_path_2)
        with open(file_path_1, "rb") as file_1, open(file_path_2, "rb") as file_2:
            return file_1.read() == file_2.read()

    return _compare
