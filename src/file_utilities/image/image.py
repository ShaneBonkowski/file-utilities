import functools
from pathlib import Path
from PIL import Image as PILImage
from typing import Union, Tuple, Optional

from file_utilities.file.file import File, CallableNoReturn

SUPPORTED_IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"]


class ImageFile(File):
    """
    Image file class.

    Provides additional functionality for image manipulation such as resizing,
    format conversion, and retrieving image properties.

    Parameters
    ----------
    path:
        Path to the image file.
    """

    def __init__(self, path: Union[str, Path]):
        super().__init__(path)
        self._load_image()

    @staticmethod
    def update_image(method: CallableNoReturn) -> CallableNoReturn:
        """Decorator to update the Image after a method is called."""

        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            result = method(self, *args, **kwargs)
            self._load_image()
            return result

        return wrapper

    @property
    def dimensions(self) -> Tuple[int, int]:
        """Returns the (width, height) of the image in px."""
        return self.image.size

    def _load_image(self):
        """Loads (or reloads) the image, updating the image attr."""
        self.is_supported_extension(self.path.suffix.lower())
        self.image = PILImage.open(self.path)

    @staticmethod
    def is_supported_extension(ext: str):
        """
        Check if the provided extension is supported. Raise an exception
        if it is not supported.
        """
        if ext not in SUPPORTED_IMAGE_EXTENSIONS:
            raise Exception(
                f"{ext} is not a supported extension! Supported extensions "
                f"are as follows: {SUPPORTED_IMAGE_EXTENSIONS}"
            )

    def resize(
        self,
        width: int,
        height: int,
        output_path: Optional[Union[str, Path]] = None,
        keep_aspect: bool = True,
    ):
        """
        Resizes the image to the given width and height.

        Parameters
        ----------
        width:
            The target width in px.
        height:
            The target height in px.
        output_path:
            Optional path to save the image to. If not provided, will overwrite the
            existing Image file.
        keep_aspect:
            Whether to preserve the aspect ratio (default: True).

        """
        if keep_aspect:
            self.image.thumbnail((width, height))
        else:
            self.image = self.image.resize((width, height))

        self.save(output_path)

    def convert_format(
        self,
        new_format: str,
        output_path: Optional[Union[str, Path]] = None,
        lossless: Optional[bool] = None,
    ):
        """
        Saves the image to a different format.

        Parameters
        ----------
        new_format:
            The new format (e.g., 'png', 'jpeg', 'webp').
        output_path:
            Optional path to save the image to. If not provided, will overwrite the
            existing Image file.
        lossless:
            Whether to use lossless compression (True) or lossy compression (False)
            if applicable.
        """

        new_format = new_format.lower()

        # Convert and save the image in the new format
        if lossless is not None:
            self.save(output_path, format=new_format.upper(), lossless=lossless)
        else:
            self.save(output_path, format=new_format.upper())

    @update_image
    def save(self, output_path: Optional[Union[str, Path]] = None, *args, **kwargs):
        """
        Saves the image to the file, ensuring it handles the format correctly.

        Parameters
        ----------
        output_path:
            Optional path to save the image to. If not provided, will overwrite the
            existing Image file.
        """

        # Overwrite existing path if new format is provided, and no output_path
        # is provided, meaning the file will be overwritten with a new name.
        # Do not update the path to this file if another output_path is provided,
        # since this is a sort of save-as operation to a separate output file.
        new_format = kwargs.get("format")
        if output_path is None and new_format is not None:
            self.path = self.path.with_suffix(f".{new_format}")

        output_path = Path(output_path) if output_path is not None else self.path
        self.is_supported_extension(output_path.suffix.lower())

        self.image.save(output_path, *args, **kwargs)

    def show(self):
        """Opens the image using the default image viewer."""
        self.image.show()

    def write(self, data: Optional[bytes] = None):
        """Override `File` write method for `ImageFile`"""
        raise NotImplementedError(
            "The 'write' method is not supported in the ImageFile class."
        )

    def __repr__(self) -> str:
        width, height = self.dimensions
        return (
            f"ImageFile(path={self.path}, size={self.size} bytes, "
            f"dimensions={width}x{height})"
        )
