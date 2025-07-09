from pathlib import Path
from typing import List, Dict, Any, Union, Optional
from docx import Document
from docx.shared import WD_PARAGRAPH_ALIGNMENT
from docx.text.paragraph import Paragraph

from file_utilities.file.file import File


class SimpleDocx:
    """
    Simple DOCX object that loads in a DOCX file and preserves basic formatting
    like bold, italics, alignment, and paragraphs.

    Parameters
    ----------
    file:
        A path to a .docx file.
    """

    def __init__(self, path: Union[str, Path]):

        self.file = File(path)

        if not str(self.file.path).lower().endswith(".docx"):
            raise ValueError(f"File must be a .docx file: {self.file.path}")

        self.document = Document(self.file.path)

    def load_content(self) -> List[Dict[str, Any]]:
        """
        Load and parse the document content with formatting preserved.

        Returns
        -------
        content:
            A list of dictionaries representing the document content with
            formatting.
        """
        content = []

        for paragraph in self.document.paragraphs:
            paragraph_data = self._parse_paragraph(paragraph)
            content.append(paragraph_data)

        return content

    def _parse_paragraph(self, paragraph: Paragraph) -> Dict[str, Any]:
        """
        Parse a paragraph and extract text with formatting.

        Parameters
        ----------
        paragraph:
            A docx Paragraph object.

        Returns
        -------
        paragraph_data:
            A dictionary representing the paragraph with formatting.
        """
        runs_data = []

        for run in paragraph.runs:
            run_data = {
                "text": run.text,
                "bold": run.bold or False,
                "italic": run.italic or False,
            }
            runs_data.append(run_data)

        # Get paragraph alignment
        alignment = self._get_alignment(paragraph.alignment)

        return {
            "type": "paragraph",
            "alignment": alignment,
            "runs": runs_data,
            "text": paragraph.text,
            "is_empty": len(paragraph.text.strip()) == 0,
        }

    def _get_alignment(self, alignment: Optional[WD_PARAGRAPH_ALIGNMENT]) -> str:
        """
        Convert docx alignment to string.

        Parameters
        ----------
        alignment:
            A WD_PARAGRAPH_ALIGNMENT value or None.

        Returns
        -------
        alignment_str:
            A string representing the alignment ("left", "center", "right",
            "justified").
        """
        alignment_map = {
            WD_PARAGRAPH_ALIGNMENT.LEFT: "left",
            WD_PARAGRAPH_ALIGNMENT.CENTER: "center",
            WD_PARAGRAPH_ALIGNMENT.RIGHT: "right",
            WD_PARAGRAPH_ALIGNMENT.JUSTIFY: "justified",
            None: "left",
        }
        return alignment_map.get(alignment, "left")
