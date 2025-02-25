import functools
import shutil
from pathlib import Path
from typing import Optional, Union, Callable, TypeVar

CallableNoReturn = TypeVar("F", bound=Callable[..., None])


class File:
    """
    Generic File class.

    Parameters
    ----------
    path:
        Path to the file.
    """

    def __init__(self, path: Union[str, Path]):
        self.path = Path(path).resolve()

        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {self.path}")

    @property
    def size(self) -> Optional[int]:
        """Returns the size of the File."""
        if self.path.exists():
            return self.path.stat().st_size
        else:
            return 0

    @property
    def modified_at(self) -> Optional[float]:
        """Returns the modified_at time of the File."""
        if self.path.exists():
            return self.path.stat().st_mtime
        else:
            return None

    @property
    def created_at(self) -> Optional[float]:
        """Returns the created_at time of the File."""
        if self.path.exists():
            return getattr(self.path.stat(), "st_birthtime", None)
        else:
            return None

    def read(self) -> bytes:
        """Reads the file and returns its contents as bytes."""
        with self.path.open("rb") as f:
            return f.read()

    def write(
        self,
        data: Optional[bytes] = None,
    ):
        """
        Writes data to the file.

        Parameters
        ----------
        data:
            The data to write to the file. If None, the current file contents
            are saved (updating its metadata).
        """
        with self.path.open("wb") as f:
            f.write(data if data is not None else self.read())

    def copy(self, destination_path: Union[str, Path]):
        """Copies the file to the given destination."""
        shutil.copy(self.path, Path(destination_path).resolve())

    def rename(self, new_name: str):
        """Renames the file without changing its directory."""

        if not new_name.endswith(self.path.suffix):
            new_name += self.path.suffix

        new_path = self.path.parent / new_name
        self.move(new_path)

    def move(self, destination_path: Union[str, Path]):
        """Moves the file to the given destination."""
        shutil.move(self.path, Path(destination_path).resolve())
        self.path = Path(destination_path).resolve()

    def delete(self) -> None:
        """Deletes the file."""
        Path(self.path).unlink()

    def __repr__(self) -> str:
        return f"File(path={self.path}, size={self.size} bytes, modified={self.modified_at})"
