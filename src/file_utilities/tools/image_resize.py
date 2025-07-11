import argparse
from pathlib import Path
from typing import Optional, Union

from file_utilities.core.image import ImageFile


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

    image = ImageFile(image_filepath)
    image.resize(width, height, output_path=output_path, keep_aspect=keep_aspect)


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
