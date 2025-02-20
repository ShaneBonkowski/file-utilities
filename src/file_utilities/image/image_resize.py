import argparse
from pathlib import Path
from typing import Optional, Union

from file_utilities.image.image import ImageFile


def resize_image(
    image_filepath: Union[str, Path],
    width: int,
    height: int,
    keep_aspect: bool = False,
    output_path: Optional[Union[str, Path]] = None,
):
    """
    Resizes the provided image to the desired width and height using the ImageFile class.

    Parameters
    ----------
    image_filepath:
        String representation of the path to the image file to be resized.
    width:
        The width to resize the image to in px.
    height:
        The height to resize the image to in px.
    keep_aspect:
        Whether or not to preserve the aspect ratio on resize. Defaults to False.
    output_path:
        Optional path to save the resized image. Must include the new name
        of the file with the correct extension! If None, the resized image will
        overwrite the original.
    """

    image_filepath = Path(image_filepath)

    if not image_filepath.is_file():
        raise FileNotFoundError(
            f"The provided file '{image_filepath}' is does not exist"
        )

    # If output_path is provided, ensure it's a valid file with the correct extension
    provided_img_extension = image_filepath.suffix.lower()
    if output_path is not None:
        output_path = Path(output_path)
        if not output_path.is_file() and not output_path.suffix:
            raise ValueError(
                f"The provided output path '{output_path}' is not a valid file path. "
                "It must include the new name of the file with the correct extension."
            )

        if output_path.suffix.lower() != provided_img_extension:
            raise ValueError(
                f"The provided output path '{output_path}' does not have the same "
                f"extension as the input image file '{image_filepath}'."
            )

    image = ImageFile(image_filepath)
    image.resize(width, height, output_path=output_path, keep_aspect=keep_aspect)
    print(f"Resized {image_filepath} to {width}x{height}.")


def main():
    parser = argparse.ArgumentParser(
        description="Resize images to the specified dimensions using ImageFile."
    )
    parser.add_argument(
        "image_filepath",
        type=str,
        help="Path to the image file to be resized.",
    )
    parser.add_argument(
        "width",
        type=int,
        help="Width to resize the image to in px.",
    )
    parser.add_argument(
        "height",
        type=int,
        help="Height to resize the image to in px.",
    )
    parser.add_argument(
        "-k",
        "--keep_aspect",
        type=bool,
        default=False,
        help="Whether or not to preserve the aspect ratio on resize. Defaults to False.",
    )
    parser.add_argument(
        "-o",
        "--output_path",
        type=str,
        default=None,
        help=(
            "Optional path to save the resized image. Must include the new name "
            "of the file with the correct extension! e.g. `/path/to/img.png`. "
            "Defaults to None, overwriting the original."
        ),
    )

    args = parser.parse_args()
    resize_image(
        args.image_filepath,
        args.width,
        args.height,
        keep_aspect=args.keep_aspect,
        output_path=args.output_path,
    )


if __name__ == "__main__":
    main()
