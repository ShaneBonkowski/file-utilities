import pytest
from PIL import Image as PILImage
from pathlib import Path

from conftest import TEST_DATA_DIR
from file_utilities.image.image import ImageFile


IMG_TEST_DATA_DIR = TEST_DATA_DIR / "image_test_data"
IMG_TEST_OUTPUT_DATA_DIR = TEST_DATA_DIR / "image_output_data"


class TestImageFile:
    source_img_path = IMG_TEST_DATA_DIR / "test_image.png"
    expected_resized_img_path = IMG_TEST_DATA_DIR / "expected_resized.png"
    expected_converted_img_path = IMG_TEST_DATA_DIR / "expected_converted.webp"

    # Ensure test data dirs exist
    Path(TEST_DATA_DIR).mkdir(parents=True, exist_ok=True)
    Path(IMG_TEST_DATA_DIR).mkdir(parents=True, exist_ok=True)
    Path(IMG_TEST_OUTPUT_DATA_DIR).mkdir(parents=True, exist_ok=True)

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown for each test"""

        # Setup: Create test source and expected data
        source_img = PILImage.new("RGB", (100, 100), color="red")
        source_img.save(self.source_img_path, "PNG")

        expected_resized_img = PILImage.new("RGB", (50, 50), color="red")
        expected_resized_img.save(self.expected_resized_img_path, "PNG")

        expected_converted_img = PILImage.new("RGB", (100, 100), color="red")
        expected_converted_img.save(self.expected_converted_img_path, "WEBP")

        yield

        # Teardown: Remove output files generated during tests
        for file_path in Path(IMG_TEST_OUTPUT_DATA_DIR).iterdir():
            if file_path.is_file():
                file_path.unlink()

    def test_resize(self, compare_file_bytes):
        """Test resizing functionality."""
        image = ImageFile(self.source_img_path)
        image.resize(
            50,
            50,
            save_path=IMG_TEST_OUTPUT_DATA_DIR / "resized_test.png",
        )

        assert compare_file_bytes(
            IMG_TEST_OUTPUT_DATA_DIR / "resized_test.png",
            self.expected_resized_img_path,
        )

    def test_convert_format(self, compare_file_bytes):
        """Test converting image format (e.g., PNG to WEBP)."""
        image = ImageFile(self.source_img_path)
        image.convert_format(
            "webp", save_path=IMG_TEST_OUTPUT_DATA_DIR / "converted_test.webp"
        )

        assert compare_file_bytes(
            IMG_TEST_OUTPUT_DATA_DIR / "converted_test.webp",
            self.expected_converted_img_path,
        )

    def test_resize_no_save_path(self, compare_file_bytes):
        """Test resizing w/o a save path (should overwrite the original)."""
        image = ImageFile(self.source_img_path)
        image.resize(50, 50)

        assert compare_file_bytes(self.source_img_path, self.expected_resized_img_path)

    def test_convert_format_no_save_path(self, compare_file_bytes):
        """Test format conversion w/o a save path (should overwrite the original)."""
        image = ImageFile(self.source_img_path)
        image.convert_format("webp")

        assert compare_file_bytes(
            self.source_img_path.with_suffix(".webp"), self.expected_converted_img_path
        )
