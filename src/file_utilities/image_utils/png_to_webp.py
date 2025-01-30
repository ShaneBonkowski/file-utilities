import argparse
import os
from PIL import Image
from typing import Optional

from file_utilities.image_utils.utilities import ImageConversionError


def png_to_webp(
    png_dir_or_file_path: str,
    lossless: bool = False,
    force: bool = False,
    output_dir: Optional[str] = None,
):
    """
    Converts provided .png file or a directory full of .png files to .webp format.
    All new .webp files are saved into a provided or inferred `webps` directory.

    Parameters
    ----------
    png_dir_or_file_path:
        String representation of either the path to the directory containing the
        PNG files to be converted OR the path to just a single .png file.
    lossless:
        Whether to use lossless compression, by default False (lossy compression).
    force:
        Whether to force overwrite an existing .webp file if it exists, False
        by default.
    output_dir:
        Output directory to write the .webp files to. If not provided, infer the
        location to write the .webp files to based on the location of the .png
        file(s).
    """

    if not os.path.isdir(png_dir_or_file_path) and not os.path.isfile(
        png_dir_or_file_path
    ):
        raise FileNotFoundError(
            f"The provided path '{png_dir_or_file_path}' is not a valid directory "
            "or file."
        )

    # Create the webps directory
    if output_dir is not None and isinstance(output_dir, str):
        webp_dir = output_dir
    elif os.path.isdir(png_dir_or_file_path):
        webp_dir = os.path.join(png_dir_or_file_path, "../webps")
    elif os.path.isfile(png_dir_or_file_path):
        webp_dir = os.path.join(png_dir_or_file_path, "../../webps")
    else:
        raise ImageConversionError(
            "Could not create or infer .webp directory from provided inputs. "
            f"output_dir = {output_dir}. png_dir_or_file_path = {png_dir_or_file_path}."
        )
    os.makedirs(webp_dir, exist_ok=True)

    # Convert!
    if os.path.isdir(png_dir_or_file_path):
        for filename in os.listdir(png_dir_or_file_path):
            png_path = os.path.join(png_dir_or_file_path, filename)
            convert_single_png_to_webp(png_path, webp_dir, lossless, force)
    elif os.path.isfile(png_dir_or_file_path):
        png_path = png_dir_or_file_path
        convert_single_png_to_webp(png_path, webp_dir, lossless, force)


def convert_single_png_to_webp(
    png_path: str, webp_dir: str, lossless: bool, force: bool
):
    """
    Converts a single .png file to .webp format and saves it in the specified webp_dir.

    Parameters
    ----------
    png_path:
        String representation of the path to a single .png file.
    webp_dir:
        String representation of the path to the directory where the converted
        .webp file will be saved.
    lossless:
        Whether to use lossless compression (True) or lossy compression (False).
    force:
        Whether to force overwrite an existing .webp file if it exists.
    """
    if png_path.lower().endswith(".png"):

        # Check if the .webp file already exists, and do NOT overwrite if it does...
        # Unless if force == true
        filename = os.path.basename(png_path)
        filename_no_extension = os.path.splitext(filename)[0]
        webp_filename = f"{filename_no_extension}.webp"
        webp_path = os.path.join(webp_dir, webp_filename)
        if os.path.isfile(webp_path) and not force:
            print(f".webp file for {filename} already exists. Skipping conversion.")
            return

        # Convert to webp
        with Image.open(png_path) as img:
            img.save(webp_path, "WEBP", quality=100 if lossless else 80)

            # Calculate reduction in size
            png_size = os.path.getsize(png_path)
            webp_size = os.path.getsize(webp_path)
            reduction_percent = ((png_size - webp_size) / png_size) * 100

            print(f"Converted {filename} to {webp_filename}")
            print(
                f"Original size: {png_size} bytes, New size: {webp_size} bytes, "
                f"Reduction: {reduction_percent:.2f}%"
            )


def main():
    parser = argparse.ArgumentParser(description="Convert .png files to .webp format.")
    parser.add_argument(
        "png_dir_or_file_path",
        type=str,
        help=(
            "String representation of either the path to a directory containing "
            "multiple .png files OR the path to a single .png file."
        ),
    )
    parser.add_argument(
        "--lossless",
        action="store_true",
        help="If provided, use lossless compression instead of lossy compression.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="If provided, force overwrite existing .webp files if one already exists.",
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default=None,
        help=(
            "Optional. Output directory to write the .webp files to. If not "
            " provided, infer the location to write the .webp files to based "
            "on the location of the .png file(s)."
        ),
    )

    args = parser.parse_args()

    if args.force:
        confirmation = input(
            "Are you sure you want to overwrite existing .webp files? Be careful, "
            "because some images may intentionally be lossless, and this tool by "
            "default makes images lossy compression. Type (yes/no) to proceed: "
        )
        if confirmation.lower() != "yes":
            print(
                f"Confirmation {confirmation.lower()} is not yes. Conversion aborted."
            )
            return

    png_to_webp(args.png_dir_or_file_path, args.lossless, args.force, args.output_dir)


if __name__ == "__main__":
    main()
