import argparse
from pathlib import Path
from typing import Optional, Union

from file_utilities.image.image import ImageFile


def resize_image(
    image_filepath: Union[str, Path],
    width: int,
    height: int,
    save_path: Optional[Union[str, Path]] = None,
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
    save_path:
        Optional path to save the resized image. If None, the image will overwrite the original.
    """

    image_filepath = Path(image_filepath)

    if not image_filepath.is_file():
        raise FileNotFoundError(
            f"The provided file '{image_filepath}' is not a valid file "
            "(likely wrong filepath)."
        )

    image = ImageFile(image_filepath)
    image.resize(width, height, save_path=save_path)
    print(f"Resized {image_filepath} to {width}x{height}.")


def main():
    parser = argparse.ArgumentParser(
        description="Resize images to the specified dimensions using ImageFile."
    )
    parser.add_argument(
        "image_filepath",
        type=str,
        required=True,
        help="Path to the image file to be resized.",
    )
    parser.add_argument(
        "--width",
        type=int,
        required=True,
        help="Width to resize the image to in px.",
    )
    parser.add_argument(
        "--height",
        type=int,
        required=True,
        help="Height to resize the image to in px.",
    )
    parser.add_argument(
        "--save_path",
        type=str,
        default=None,
        help=(
            "Optional path to save the resized image. Defaults to None, "
            "overwriting the original."
        ),
    )

    args = parser.parse_args()
    resize_image(args.image_filepath, args.width, args.height, save_path=args.save_path)


if __name__ == "__main__":
    main()
