# file-utilities

**File Utilities** is a collection of Python tools for handling files efficiently. It includes utilities for reading, writing, organizing, and converting various file types.

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

### Release

#### 1. Commit Changes:

Ensure all changes are committed to the `main` branch.

#### 2. Update Version:

- Open the pyproject.toml file and increment the version number under [project].
- Use semantic versioning (e.g., 0.1.1 → 0.2.0).

#### 3. Tag the Release off of the `main` branch:

```bash
git tag -a v<new_version> -m "Release <new_version>"
git push origin v<new_version>
```

#### 4. Create a Release Page on GitHub:

- Go to the `Releases` tab of the GitHub repository.
- Click `Draft a new release`, select the tag that was just pushed, and provide a release title and description.
- Publish the release.

### Deploying Using pyproject.toml

Follow the above `Release` steps before deploying!

#### 1. Ensure you have build installed:

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

#### 5. Upload the package to PyPI:

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
image_convert tests/test_data/image_test_data/test_image.png .webp --o .
```

Use the Command Line Interface (CLI) to convert image size.

```bash
image_resize tests/test_data/image_test_data/test_image.png 10 10 --o ./test_image_resized.png
```
