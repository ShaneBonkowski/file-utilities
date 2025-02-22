import argparse
from pathlib import Path
from typing import Optional, Union
from file_utilities.image.image import ImageFile, SUPPORTED_IMAGE_EXTENSIONS


def convert_images(
    image_dir_or_filepath: Union[str, Path],
    target_format: str,
    lossless: bool = False,
    force: bool = False,
    output_dir: Optional[Union[str, Path]] = None,
):
    """
    Converts provided image file(s) to a target format (e.g., .webp, .jpg, etc.).
    All new files are saved into a provided or inferred output directory.

    Parameters
    ----------
    image_dir_or_filepath:
        String representation of either the path to the directory containing the
        image files to be converted OR the path to just a single image file.
    target_format:
        The target image format to convert to (e.g., 'webp', 'jpg', 'png').
    lossless:
        Whether to use lossless compression, by default False (if applicable).
    force:
        Whether to force overwrite an existing file if it exists, False by default.
    output_dir:
        Output directory to write the converted files to. Must be a directory,
        not a file! If not provided, infer the location to write the files based
        on the location of the input file(s).
    """

    image_dir_or_filepath = Path(image_dir_or_filepath).resolve()

    # If output_dir is not provided, infer the location. Otherwise, use it.
    if output_dir is not None:
        output_dir = Path(output_dir).resolve()
    else:
        output_dir = image_dir_or_filepath.parent / "converted_images"

    # Output directory MUST be a directory, not a file.
    if output_dir.is_file() or output_dir.suffix:
        raise ValueError(
            f"The provided output directory '{output_dir}' is not a valid directory."
        )
    output_dir.mkdir(parents=True, exist_ok=True)

    # Convert!
    target_format = target_format.replace(".", "").lower()
    if image_dir_or_filepath.is_dir():
        for filepath in image_dir_or_filepath.iterdir():
            convert_single_image(filepath, target_format, output_dir, lossless, force)
    elif image_dir_or_filepath.is_file():
        convert_single_image(
            image_dir_or_filepath, target_format, output_dir, lossless, force
        )


def convert_single_image(
    image_path: Path, target_format: str, output_dir: Path, lossless: bool, force: bool
):
    """
    Converts a single image file to the target format and saves it in the
    specified output_dir.

    Parameters
    ----------
    image_path:
        Path to a single image file.
    target_format:
        The target image format to convert to (e.g., 'webp', 'jpg', 'png').
    output_dir:
        Path to the directory where the converted image will be saved.
    lossless:
        Whether to use lossless compression (True) or lossy compression (False)
        if applicable.
    force:
        Whether to force overwrite an existing image if it exists.
    """

    # Convert the image to the target format
    target_filename = f"{image_path.stem}.{target_format}"
    target_path = output_dir / target_filename

    # Skip if the target file exists and force is not enabled
    if target_path.exists() and not force:
        raise FileExistsError(f"{target_filename} already exists and force is False.")

    img = ImageFile(image_path)
    img.convert_format(target_format, target_path, lossless=lossless)


def main():
    parser = argparse.ArgumentParser(
        description="Convert image file(s) to a specified format."
    )
    parser.add_argument(
        "image_dir_or_filepath",
        type=str,
        help=(
            "Path to a directory containing image files or the path to a single "
            "image file."
        ),
    )
    parser.add_argument(
        "target_format",
        type=str,
        help=(
            "The target image format to convert to. Supported formats: "
            f"{SUPPORTED_IMAGE_EXTENSIONS}."
        ),
    )
    parser.add_argument(
        "--lossless",
        action="store_true",
        help="If provided, use lossless compression for formats that support it.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="If provided, force overwrite existing files.",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default=None,
        help=(
            "Optional. Directory to write the converted files to. Must be a "
            "directory, not a file! If not provided, infer location."
        ),
    )

    args = parser.parse_args()

    convert_images(
        args.image_dir_or_filepath,
        args.target_format,
        args.lossless,
        args.force,
        args.output_dir,
    )


if __name__ == "__main__":
    main()
