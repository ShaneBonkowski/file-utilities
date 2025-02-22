import functools
from pathlib import Path
from PIL import Image as PILImage
from typing import Union, Tuple, Optional

from file_utilities.file.file import File, CallableNoReturn

SUPPORTED_IMAGE_EXTENSIONS = [
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".tiff",
    ".webp",
    ".ico",
]


class UnsupportedImageExtensionError(Exception):
    """Exception for when an unsupported image extension is provided."""

    def __init__(self, ext: str):
        super().__init__(
            f"{ext} is not a supported extension! Supported extensions are as follows: "
            f"{SUPPORTED_IMAGE_EXTENSIONS}"
        )


class UnmatchingOutputExtensionError(Exception):
    """Exception for when output file extension does not match source file."""

    def __init__(self, out_ext: str, source_ext: str):
        super().__init__(
            f"Provided output path extension: {out_ext} does not match source "
            f"image extension: {source_ext} "
        )


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
            raise UnsupportedImageExtensionError(ext)

    def resize(
        self,
        width: int,
        height: int,
        output_path: Optional[Union[str, Path]] = None,
        keep_aspect: bool = False,
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
            Whether to preserve the aspect ratio (default: False).

        """

        output_path = Path(output_path) if output_path is not None else None

        if output_path is not None:
            if output_path.suffix.lower() != self.path.suffix.lower():
                raise UnmatchingOutputExtensionError(
                    output_path.suffix, self.path.suffix
                )

        # Modifies the image in place and then saves it out to the provided path.
        # Note that .save() has a decorator that reloads the image after saving,
        # so that if we did not intend to modify the image in place, self.image
        # stays accurate.
        if keep_aspect:
            # thumbnail() modifies the image in place
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
            The new format (e.g., 'png', 'jpeg', 'webp', 'ico').
        output_path:
            Optional path to save the image to. If not provided, will save with
            same name and directory as the existing Image file.
        lossless:
            Whether to use lossless compression (True) or lossy compression (False)
            if applicable.
        """

        new_format = new_format.upper()
        output_path = Path(output_path) if output_path is not None else self.path

        # Ensure outpath extension is the provided format so that PIL knows to convert.
        if output_path.is_file() or output_path.suffix:
            output_path = output_path.with_suffix(f".{new_format.lower()}")
        else:
            output_path = output_path / f"{self.path.stem}.{new_format.lower()}"

        # Convert and save the image in the new format
        save_kwargs = {}
        if new_format.upper() == "ICO":
            # Default to 32x32 to ico
            save_kwargs["sizes"] = [(32, 32)]

        if lossless is not None:
            save_kwargs["lossless"] = lossless

        self.save(output_path, **save_kwargs)

    @update_image
    def save(
        self,
        output_path: Optional[Union[str, Path]] = None,
        *args,
        **kwargs,
    ):
        """
        Saves the image to the file, ensuring it handles the format correctly.

        Parameters
        ----------
        output_path:
            Optional path to save the image to. If not provided, will overwrite the
            existing Image file.
        """

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
