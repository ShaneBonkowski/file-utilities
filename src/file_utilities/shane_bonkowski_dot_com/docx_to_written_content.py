import argparse
import re
from pathlib import Path
from typing import Union, Optional

from file_utilities.file.docx import SimpleDocx


def convert_docx_to_written_content(
    docx_filepath: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
):
    """
    Converts a DOCX file to WrittenContent JSX format for shane-bonkowski-dot-com.

    Parameters
    ----------
    docx_filepath:
        Path to the DOCX file to convert.
    output_path:
        Optional path to save the JSX output. If None, saves as
        "{filename}_written_content.txt".
    """

    # Load the DOCX file
    docx = SimpleDocx(docx_filepath)
    content = docx.load_content()

    # Process paragraphs
    jsx_paragraphs = []

    for paragraph_data in content:
        if paragraph_data["is_empty"]:
            continue  # Skip empty paragraphs

        # Determine if entire paragraph is italic
        all_italic = all(
            run["italic"] for run in paragraph_data["runs"] if run["text"].strip()
        )
        font_style = "italic" if all_italic else "normal"

        # Convert alignment
        text_align = paragraph_data["alignment"]

        # Process text with formatting
        processed_text = _process_paragraph_text(paragraph_data["runs"])

        # Create JSX element
        jsx_element = f"""          <WrittenContentParagraphElement
            fontStyle="{font_style}"
            textAlign="{text_align}"
          >
            {processed_text}
          </WrittenContentParagraphElement>"""

        jsx_paragraphs.append(jsx_element)

    # Create the full JSX template
    jsx_output = f"""<WrittenContentLoader {{...storyData}}>
        <WrittenContentParagraphGroup>
{chr(10).join(jsx_paragraphs)}
        </WrittenContentParagraphGroup>
      </WrittenContentLoader>"""

    # Determine output path
    if output_path is None:
        input_path = Path(docx_filepath)
        output_path = input_path.parent / f"{input_path.stem}_written_content.txt"

    # Write to file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(jsx_output)

    print(f"Converted DOCX to WrittenContent JSX: {output_path}")


def _process_paragraph_text(runs) -> str:
    """Process text runs and apply formatting while normalizing quotes."""
    processed_parts = []

    for run in runs:
        text = run["text"]

        # Normalize quotes and apostrophes
        text = _normalize_quotes(text)

        # Apply formatting for individual words/phrases (not whole paragraph)
        if run["italic"] and not _is_whole_paragraph_italic(runs):
            text = f"<em>{text}</em>"
        if run["bold"]:
            text = f"<strong>{text}</strong>"

        processed_parts.append(text)

    return "".join(processed_parts)


def _is_whole_paragraph_italic(runs) -> bool:
    """
    Check if the entire paragraph should be considered italic.

    Parameters
    ----------
    runs:
        List of text runs in the paragraph.
    """
    non_empty_runs = [run for run in runs if run["text"].strip()]
    return all(run["italic"] for run in non_empty_runs) if non_empty_runs else False


def _normalize_quotes(text: str) -> str:
    """
    Normalize various quote and apostrophe characters.

    Parameters
    ----------
    text:
        The text to normalize.

    Returns
    -------
    text:
        The normalized text.
    """
    # Smart quotes to regular quotes
    # TODO: add all the weird ticks to this
    text = re.sub(r'["""]', "&quot;", text)
    # text = re.sub(r'[''']', '&apos;', text)
    text = re.sub(r"`", "&apos;", text)

    # Handle other special characters that might cause JSX issues
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")

    return text


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Convert DOCX file to WrittenContent JSX format for "
            "shane-bonkowski-dot-com"
        )
    )
    parser.add_argument(
        "docx_file",
        type=str,
        help="Path to the DOCX file to convert",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="Output path for the JSX output (optional)",
    )

    args = parser.parse_args()

    convert_docx_to_written_content(
        docx_filepath=args.docx_file, output_path=args.output
    )


if __name__ == "__main__":
    main()
