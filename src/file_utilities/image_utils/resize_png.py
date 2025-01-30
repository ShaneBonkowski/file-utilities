import argparse
import os
from PIL import Image


def resize_png(
    png_filepath: str,
    x: int,
    y: int,
):
    """
    Resizes provided .png to desired x and y size.

    Parameters
    ----------
    png_filepath:
        String representation of the path to the .png file to be resized.
    x:
        The width to resize the image to.
    y:
        The height to resize the image to.
    """

    if not os.path.isfile(png_filepath):
        raise FileNotFoundError(
            f"The provided png '{png_filepath}' is not a valid file "
            "(likely wrong filepath)."
        )

    # Resize the image to the desired size
    with Image.open(png_filepath) as img:
        x_orig, y_orig = img.size
        img = img.resize((x, y))
        img.save(png_filepath, "png")
        print(f"Converted {png_filepath} from size ({x_orig}, {y_orig}) to ({x}, {y})")


def main():
    parser = argparse.ArgumentParser(description="Resize .png files.")
    parser.add_argument(
        "png_filepath",
        type=str,
        help="String representation of the path to the .png file to be resized.",
    )
    parser.add_argument(
        "--width",
        type=int,
        help="Width to resize images to.",
    )
    parser.add_argument(
        "--height",
        type=int,
        help="Height to resize images to.",
    )

    args = parser.parse_args()
    resize_png(args.png_filepath, args.width, args.height)


if __name__ == "__main__":
    main()
