import argparse
import re
from pathlib import Path
from typing import Union, Optional, List, Dict, Any

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

    docx = SimpleDocx(docx_filepath)
    content = docx.load_content()

    if output_path is not None and ".txt" not in Path(output_path).suffix.lower():
        raise ValueError("Output path must have a .txt extension.")

    # Process each paragraph into desired JSX format
    jsx_paragraphs = []

    for paragraph_data in content:
        if paragraph_data["is_empty"]:
            continue

        # Font style for the entire paragraph
        font_style = _get_paragraph_font_style(paragraph_data["runs"])

        # Text alignment for the paragraph
        text_align = paragraph_data["alignment"]
        if text_align == "justified":
            text_align = "justify"

        if text_align not in ["left", "center", "right", "justify"]:
            print(f"Unknown alignment '{text_align}', defaulting to 'left'.")
            text_align = "left"

        # Process individual text in each paragraph with formatting
        processed_text = _process_paragraph_text(paragraph_data["runs"])

        # Create the custom JSX component for each paragraph
        jsx_element = f"""          <WrittenContentParagraphElement
            fontStyle="{font_style}"
            textAlign="{text_align}"
          >
            {processed_text}
          </WrittenContentParagraphElement>"""

        jsx_paragraphs.append(jsx_element)

    # Create the full JSX template for all paragraphs together
    jsx_output = f"""<WrittenContentLoader {{...storyData}}>
        <WrittenContentParagraphGroup>
{'\n'.join(jsx_paragraphs)}
        </WrittenContentParagraphGroup>
      </WrittenContentLoader>"""

    # Write to file
    if output_path is None:
        input_path = docx.file.path
        output_path = input_path.parent / f"{input_path.stem}_written_content.txt"

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(jsx_output)

    print(f"Converted DOCX to WrittenContent JSX: {output_path}")


def _get_paragraph_font_style(runs: List[Dict[str, Any]]) -> str:
    """
    Determine the font style for the entire paragraph.

    Parameters
    ----------
    runs:
        List of text runs in the paragraph.

    Returns
    -------
    str:
        "bold", "italic", or "normal" based on whether the entire paragraph has
        consistent formatting.
    """
    non_empty_runs = [run for run in runs if run["text"].strip()]

    if not non_empty_runs:
        return "normal"

    all_bold = all(run["bold"] for run in non_empty_runs)
    all_italic = all(run["italic"] for run in non_empty_runs)

    if all_bold:
        return "bold"
    elif all_italic:
        return "italic"
    else:
        return "normal"


def _process_paragraph_text(runs: List[Dict[str, Any]]) -> str:
    """
    Process text runs and apply formatting while normalizing quotes.
    Merges consecutive runs with same formatting to avoid fragmented tags.

    Parameters
    ----------
    runs:
        List of text runs in the paragraph.

    Returns
    -------
    text:
        The processed text with formatting applied.
    """
    paragraph_font_style = _get_paragraph_font_style(runs)

    # First, normalize all text and determine which runs need individual
    # formatting. We first determine which ones need formatting so that we
    # can merge consecutive runs with the same formatting later. This avoids
    # a bunch of consecutive <em> or <b> tags for example.
    processed_runs = []
    for run in runs:
        # Normalize quotes, apostrophes, etc. to avoid JSX issues
        text = _normalize_symbols(run["text"])

        # Apply formatting for individual words/phrases only if not whole paragraph.
        # This is because `font_style` already applies to the whole paragraph if necc.
        needs_italic = run["italic"] and paragraph_font_style != "italic"
        needs_bold = run["bold"] and paragraph_font_style != "bold"

        processed_runs.append(
            {"text": text, "needs_italic": needs_italic, "needs_bold": needs_bold}
        )

    # Merge consecutive runs with same formatting
    merged_parts = []
    i = 0

    while i < len(processed_runs):
        current_run = processed_runs[i]

        # Collect consecutive runs with same formatting
        text_group = current_run["text"]
        j = i + 1

        while (
            j < len(processed_runs)
            and processed_runs[j]["needs_italic"] == current_run["needs_italic"]
            and processed_runs[j]["needs_bold"] == current_run["needs_bold"]
        ):
            text_group += processed_runs[j]["text"]
            j += 1

        # Apply formatting to the entire group
        if current_run["needs_italic"]:
            text_group = f"<em>{text_group}</em>"
        if current_run["needs_bold"]:
            text_group = f"<b>{text_group}</b>"

        merged_parts.append(text_group)
        i = j

    return "".join(merged_parts)


def _normalize_symbols(text: str) -> str:
    """
    Normalize various quote, apostrophe, etc. characters to avoid JSX issues.

    Parameters
    ----------
    text:
        The text to normalize.

    Returns
    -------
    text:
        The normalized text.
    """
    # Handle quotes and apostrophes
    text = re.sub(r'[“”"]', "&quot;", text)
    text = re.sub(r"[‘’`']", "&apos;", text)

    # Handle other common special characters that might cause JSX issues
    text = text.replace("&", "&amp;")
    text = text.replace("<", "&lt;")
    text = text.replace(">", "&gt;")
    text = text.replace("\u00a0", "&nbsp;")
    text = re.sub(r"[—–]", "&mdash;", text)

    # Uncommon symbols
    text = text.replace("©", "&copy;")
    text = text.replace("®", "&reg;")
    text = text.replace("™", "&trade;")
    text = text.replace("°", "&deg;")

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
        help="Output path to `.txt` file for the JSX output (optional)",
    )

    args = parser.parse_args()

    convert_docx_to_written_content(
        docx_filepath=args.docx_file, output_path=args.output
    )


if __name__ == "__main__":
    main()
