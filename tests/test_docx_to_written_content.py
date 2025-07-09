import pytest
from pathlib import Path

from file_utilities.shane_bonkowski_dot_com.docx_to_written_content import (
    convert_docx_to_written_content,
)
from conftest import TEST_DATA_DIR


DOCX_TEST_DATA_DIR = TEST_DATA_DIR / "docx_test_data"
DOCX_TEST_OUTPUT_DATA_DIR = TEST_DATA_DIR / "docx_output_data"


class TestDocxToWrittenContent:

    # Ensure test data dirs exist
    Path(TEST_DATA_DIR).mkdir(parents=True, exist_ok=True)
    Path(DOCX_TEST_DATA_DIR).mkdir(parents=True, exist_ok=True)
    Path(DOCX_TEST_OUTPUT_DATA_DIR).mkdir(parents=True, exist_ok=True)

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown for each test"""

        yield

        # Teardown: Remove all output files generated during tests
        for filepath in Path(DOCX_TEST_OUTPUT_DATA_DIR).iterdir():
            if filepath.is_file():
                filepath.unlink()

    @pytest.mark.parametrize(
        "input_docx_path, output_written_content_path, expected_written_content_path",
        [
            # Test case with paragraphs that are not separated by empty spaces.
            # Each "enter" is a new paragraph.
            (
                DOCX_TEST_DATA_DIR / "input_p_no_empty_spaces.docx",
                DOCX_TEST_OUTPUT_DATA_DIR / "output_p_no_empty_spaces.txt",
                DOCX_TEST_DATA_DIR / "expected_output_p_no_empty_spaces.txt",
            ),
            # Test case with paragraphs separated by empty spaces. Therefore,
            # has paragraphs that need <br></br> to separate them.
            (
                DOCX_TEST_DATA_DIR / "input_p_empty_spaces.docx",
                DOCX_TEST_OUTPUT_DATA_DIR / "output_p_empty_spaces.txt",
                DOCX_TEST_DATA_DIR / "expected_output_p_empty_spaces.txt",
            ),
        ],
    )
    def test_convert_docx_to_written_content(
        self,
        input_docx_path,
        output_written_content_path,
        expected_written_content_path,
    ):
        """Test that DOCX conversion produces expected JSX output."""

        with open(expected_written_content_path, "r", encoding="utf-8") as f:
            expected_jsx = f.read().strip()

        # Convert DOCX to JSX
        actual_jsx = convert_docx_to_written_content(
            docx_filepath=input_docx_path,
            output_path=output_written_content_path,
        ).strip()

        # Compare outputs (returned string AND content of output file)
        assert actual_jsx == expected_jsx, "Generated JSX doesn't match expected output"

        with open(output_written_content_path, "r", encoding="utf-8") as f:
            output_file_content = f.read().strip()
        assert (
            output_file_content == expected_jsx
        ), "Output file content doesn't match expected output"

    def test_invalid_output_extension(self):
        """Test that non-.txt output extension raises error."""
        with pytest.raises(ValueError, match="Output path must have a .txt extension"):
            convert_docx_to_written_content(
                docx_filepath=DOCX_TEST_DATA_DIR / "input_p_no_empty_spaces.docx",
                output_path="output.html",
            )

    def test_missing_docx_file(self):
        """Test that missing DOCX file raises appropriate error."""
        with pytest.raises(FileNotFoundError):
            convert_docx_to_written_content(docx_filepath="nonexistent.docx")
