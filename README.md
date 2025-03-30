# Album Manager CLI

Welcome to Album Manager CLI 🎉

This project offers a sleek set of scripts to manage and organize your photo albums stored locally. Whether you need to split folders of images into organized albums by date, or you’re just tired of scrolling aimlessly through chaotic directories — Album Manager CLI is here to save the day.

---

## 📚 Table of Contents
1. [Motivation](#-motivation)
2. [Project Setup](#️-project-setup)
3. [Scripts Currently Developed](#-scripts-currently-developed)
    - [Group Photos](#group-photos)
4. [Continuous Integration / Development](
  #-continuous-integration--development)

---

## 🚀 Motivation
Managing photo albums can be a hassle. Do you have images dumped into one folder, named cryptically as IMG_XXXX.jpg with no rhyme or reason? You’re not alone. Album Manager CLI was created to tame that chaos—making it effortless to sort photos into albums using dates, while also letting you name albums on the go.  
Goodbye, photo mess; hello, organized bliss!

## 🛠️ Project Setup
Ready to get started? Here’s how you can set up Album Manager CLI on your local machine.  
Follow these steps to get everything up and running:

1. Clone the Repository  
  Start by cloning this repository to your local system using git.

  ```bash
  git clone https://github.com/your-username/album-manager-cli.git
  cd album-manager-cli
  ```

2. Ensure Python 3.8 is Installed  
  Make sure you have Python 3.8 installed. If not, you can grab it from [python.org]().

3. Install Poetry  
  Poetry is used for managing dependencies and environments. You can install Poetry via the official installer:

  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```

  Alternatively, refer to the [Poetry Documentation](https://python-poetry.org/docs/) for platform-specific instructions.

4. Install Project Dependencies  
  Use Poetry to install all dependencies specified in the pyproject.toml file:

  ```bash
  poetry install
  ```

  This will create a virtual environment and install all the necessary packages for you to run and develop the Album Manager CLI.

## 📜 Scripts Currently Developed
The following section describes the various scripts which have been developed so far.  
In the future we expect for further scripts to be developed as needs arise.

### Group Photos
Group Photos is a script that organizes a folder full of images into multiple folders (albums) based on their dates. This makes it super easy to create separate albums while giving you the flexibility to view images and even provide custom names for your new albums. Here's how it works:

#### Usage Example
```bash
python -m src.entrypoints.group_photos
```

#### What it Does 
The script reads through the images in the given folder.
It organizes images into subfolders based on the date (e.g., 2024-10-15, etc.).
You'll be prompted to name each album, making it a quick way to personalize your photo collections.

## 🔧 Continuous Integration / Development

### Code Quality Validation
This project ensures high code quality and adherence to best practices using:
- Ruff for linting 🧹
- Mypy for static type checking 🧐

On every push to the main branch, automated checks run to validate code quality, catching errors before they become problems. This keeps the project clean, maintainable, and less likely to break your heart (or codebase).

