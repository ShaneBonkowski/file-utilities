import pytest
from PIL import Image as PILImage
from pathlib import Path

from conftest import TEST_DATA_DIR
from file_utilities.core.image import ImageFile


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

        # Setup: Create/re-create test source and expected data.
        # This is necc. because some of the tests modify the image files in place!
        source_img = PILImage.new("RGB", (100, 100), color="red")
        source_img.save(self.source_img_path, "PNG")

        expected_resized_img = PILImage.new("RGB", (50, 50), color="red")
        expected_resized_img.save(self.expected_resized_img_path, "PNG")

        expected_converted_img = PILImage.new("RGB", (100, 100), color="red")
        expected_converted_img.save(self.expected_converted_img_path, "WEBP")

        # Create a fake extension file
        Path(IMG_TEST_DATA_DIR / "unsupported_extension.fake").touch()

        yield

        # Teardown: Remove all test data and output files generated during tests
        for filepath in Path(IMG_TEST_DATA_DIR).iterdir():
            if filepath.is_file():
                filepath.unlink()

        for filepath in Path(IMG_TEST_OUTPUT_DATA_DIR).iterdir():
            if filepath.is_file():
                filepath.unlink()

    @pytest.mark.parametrize(
        "image_path",
        [
            ("/non/existent/path/image.png"),
            ("/another/non/existent/path/image.png"),
        ],
    )
    def test_init_missing_image_path(self, image_path):
        """
        Test that an incorrect path raises an expected error when initializing
        the ImageFile class.
        """
        with pytest.raises(FileNotFoundError):
            ImageFile(image_path)

    @pytest.mark.parametrize(
        "image_path",
        [
            # File exists, but not supported extension
            (IMG_TEST_DATA_DIR / "unsupported_extension.fake"),
            # Path exists, but its to a directory, not a file.
            (IMG_TEST_DATA_DIR),
        ],
    )
    def test_init_unsupported_image_extension(self, image_path):
        """
        Test that an unsupported image extension will raise an expected error
        when initializing the ImageFile class.
        """
        with pytest.raises(ValueError):
            ImageFile(image_path)

    def test_save_unsupported_output_path_extension(self):
        """
        Test that an unsupported output path extension will raise an expected
        error on save().
        """
        image = ImageFile(self.source_img_path)

        with pytest.raises(ValueError):
            image.save(output_path="path/to/image.wrong_extension")

    def test_resize_non_matching_output_path_extension(self):
        """
        Test that an output path extension that does not match the source image
        path extension will raise an error for resize().
        """
        image = ImageFile(self.source_img_path)
        with pytest.raises(ValueError):
            image.resize(50, 50, output_path="path/to/image.wrong_extension")

    def test_resize(self, compare_file_bytes):
        """Test resizing functionality."""
        image = ImageFile(self.source_img_path)
        image.resize(
            50,
            50,
            output_path=IMG_TEST_OUTPUT_DATA_DIR / "resized_test.png",
        )

        # Expected path should be the original path since we do not update the
        # original path to the file if another output_path is provided.
        assert image.path == self.source_img_path
        assert compare_file_bytes(
            IMG_TEST_OUTPUT_DATA_DIR / "resized_test.png",
            self.expected_resized_img_path,
        )

        # Original should be unchanged and not resized!
        assert not compare_file_bytes(image.path, self.expected_resized_img_path)

    def test_resize_no_output_path(self, compare_file_bytes):
        """
        Test that resizing w/o an output path works as expected. This should
        overwrite the original image file.
        """
        image = ImageFile(self.source_img_path)
        image.resize(50, 50)

        assert image.path == self.source_img_path
        assert compare_file_bytes(image.path, self.expected_resized_img_path)

    def test_convert_format(self, compare_file_bytes):
        """Test converting image format (e.g., PNG to WEBP)."""
        image = ImageFile(self.source_img_path)
        image.convert_format(
            "webp", output_path=IMG_TEST_OUTPUT_DATA_DIR / "converted_test.webp"
        )

        # Expected path should be the original path since we do not update the
        # original path to the file if another output_path is provided.
        assert image.path == self.source_img_path
        assert compare_file_bytes(
            IMG_TEST_OUTPUT_DATA_DIR / "converted_test.webp",
            self.expected_converted_img_path,
        )

        # Original should be unchanged and not new format!
        assert not compare_file_bytes(image.path, self.expected_resized_img_path)

    def test_convert_format_no_output_path(self, compare_file_bytes):
        """
        Test format conversion w/o an output path. This should result in a converted
        image in the same dir as the original.
        """
        image = ImageFile(self.source_img_path)
        image.convert_format("webp")

        # Should create a file with the same name as the original, but with the new extension.
        assert image.path.stem == image.path.with_suffix(".webp").stem
        assert compare_file_bytes(
            image.path.with_suffix(".webp"), self.expected_converted_img_path
        )

        # Cleanup: Remove the converted file since its in the `image_test_data` folder
        # and its technically `image_output_data`. This happens because since this writes
        # if no output dir is provided, it will write "in place" with a new extension.
        # We don't want to keep this file around.
        image.path.with_suffix(".webp").unlink()
