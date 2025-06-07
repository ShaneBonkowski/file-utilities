# file-utilities

**File Utilities** is a collection of Python tools I built to simplify various file-related tasks. I often found myself searching for things like "PNG to WebP converter," only to end up on slow, ad-ridden web pages. So, I decided to create my own tools (with a lot of help from existing libraries). The following README is written with the intention of allowing anyone with minimal coding experience to get set up and use the tools for themselves.

## Initial Setup (one-time steps)

### 1. Install Python

If Python is not already installed:

- Go to https://www.python.org/downloads/ and download the most recent version of Python.
- When it is downloading, check the box to add it to your PATH. This will ensure that you can `pip` install and use python from the PowerShell in Windows. Note: steps may be different for Mac or Linux.
- If `pip install` is not working as intended, you likely do not have Python downloaded, or do not have it being referenced in your PATH.

### 2. Install virtualenv library

```bash
pip install virtualenv
```

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/ShaneBonkowski/file-utilities.git
cd file-utilities
```

### 2. (Optional) Create + activate a virtual environment:

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

macOS/Linux

```bash
source venv/bin/activate
```

### 3. Install python dependencies:

Since all dependencies are specified in pyproject.toml, simply from the root directory of this project call:

```bash
pip install .
```

This will install the entire package and all dependencies.

## Development

### Activating the Virtual Environment

Windows

```bash
venv\Scripts\activate
```

macOS/Linux

```bash
source venv/bin/activate
```

### Pip installing in editable mode

```bash
pip install -e /path/to/file-utilities
```

This allows for any changes made to the code to instantly take effect without
needing to re-install. This is especially useful when working on new tests or
command line functionality, since it eliminates the need for pip installing
multiple times while rapidly prototyping.

### Release

#### 1. Update Version:

- Open the pyproject.toml file and increment the version number under [project].
- Use semantic versioning (e.g., 0.1.1 → 0.2.0).

#### 2. Commit Changes:

Ensure all changes are committed to the `main` branch.

#### 3. Create a Release Page on GitHub:

- Go to the `Releases` tab of the GitHub repository.
- Click on `Draft a new release`.
- Create a tag for `v<new_version>` off of the `main` branch that was just pushed.
- Provide a release title and description.
- Publish the release.

### Deploying Using pyproject.toml

Follow the above `Release` steps before deploying!

#### 1. (Optional) Ensure you have build installed:

```bash
pip install build
```

#### 2. Checkout the latest release tag:

```bash
git checkout tags/v<new_version>
```

#### 3. Build the package:

```bash
python -m build
```

This generates a `dist/` directory containing `.tar.gz` and `.whl` files.

#### 4. (Optional) Install twine for publishing:

```bash
pip install twine
```

#### 5. (Optional) Upload the package to PyPI:

```bash
twine upload dist/*
```

## Usage

Resize an image:

```python
from file_utilities.image.image import ImageFile

image = ImageFile("/path/to/picture.png")
image.resize(400, 200)
```

Convert to another image type:

```python
from file_utilities.image.image import ImageFile

image = ImageFile("/path/to/picture.png")
image.convert_format("webp")
```

Use the Command Line Interface (CLI) to convert an image type.

```bash
image_convert tests/test_data/image_test_data/test_image.png .webp -o .
```

Use the Command Line Interface (CLI) to convert image size.

```bash
image_resize tests/test_data/image_test_data/test_image.png 10 10 -o ./test_image_resized.png
```

## Style Guide

### Formatting

All code follows the [PEP-8](https://peps.python.org/pep-0008/) standard. To make this easier, the `black` formatter is used to automatically format to this standard.

### Documentation

The [Numpy](https://numpydoc.readthedocs.io/en/latest/format.html) format is used for documentation. In addition, type hints from the `typing` library are used. It looks as follows:

```python
def add(number1: int, number2: int) -> int:
    """
    This function adds two numbers together.

    Parameters
    ----------
    number1 : type
        Description of number1.
    number2 : type
        Description of number2.

    Returns
    -------
    int
        The sum of number1 and number2.
    """

    return number1 + number2

```
