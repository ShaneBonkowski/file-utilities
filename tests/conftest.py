import pytest
from pathlib import Path
from typing import Union


TEST_DATA_DIR = Path(__file__).parent / "test_data"


@pytest.fixture
def compare_file_bytes():
    """Fixture for comparing two files by their byte data."""

    def _compare(filepath_1: Union[str, Path], filepath_2: Union[str, Path]) -> bool:
        filepath_1 = Path(filepath_1)
        filepath_2 = Path(filepath_2)
        with open(filepath_1, "rb") as file_1, open(filepath_2, "rb") as file_2:
            return file_1.read() == file_2.read()

    return _compare
