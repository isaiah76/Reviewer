# Reviewer

Reviewer is a document processing tool that extracts text from PDF and PowerPoint documents (.pdf, .pptx, .ppt) and summarizes it using LangChain and Google's Gemini AI. This project supports OCR based extraction and image based PDF's.

## Features

- Extract text from PDF and PPT/PPTX files.
- Uses OCR Tesseract to extract text from images within PDF's and PowerPoint slides.
- Summarizes into a clear overview.
- Answers user questions based on the document.
- Maintains conversation context and memory.
- Uses LangChain and Google's Gemini API.
- Supports large documents by chunking the document before processing. 

## Project Structure
```
Reviewer/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── .env                       # Environment file
├── config/
│   └── settings.py            # Configuration settings
├── core/
│   ├── __init__.py
│   ├── document_processor.py  # Document text extraction
│   ├── text_chunker.py        # Text chunking utilities
│   ├── ai_service.py          # LLM model integration
│   └── cli.py                 # User interface functions
└── utils/
    ├── __init__.py
    ├── file_helpers.py        # File validation utilities
    └── converters.py          # Conversion utilities
```

## Requirements

- Python 3.8 or higher
- Tesseract OCR
- Poppler
- LibreOffice (Optional)

_It is recommended to install `unoconv` or `unoserver` aside from `LibreOffice` for better performance._

## Installation

Clone the repository:

```bash
git clone https://github.com/Isaiah512/Reviewer.git
cd reviewer
```

## Linux Installation

Run the provided installation script:

```sh 
chmod +x install.sh && ./install.sh
```

## Windows Installation

Run the provided batch script:

```sh 
install.bat
```

## Dependencies

**Ensure the following dependencies are installed before running the program**

#### Tesseract OCR

Linux:

- Debian/Ubuntu:
    ```sh 
    sudo apt install tesseract-ocr
    ```
- Arch Linux:
    ```sh 
    sudo pacman -S tesseract 
    ```
- Fedora:
    ```sh 
    sudo dnf install tesseract
    ```

macOS:

    ```sh 
    brew install tesseract
    ```

Windows: Download and install from [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki). Ensure the installation path is added to your system PATH.

#### Poppler

Linux:

- Debian/Ubuntu:
    ```sh 
    sudo apt install poppler-utils
    ```
- Arch Linux:
    ```sh 
    sudo pacman -S poppler
    ```
- Fedora:
    ```sh 
    sudo dnf install poppler-utils
    ```

macOS:

    ```sh 
    brew install poppler
    ```

Windows: Download from [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases) and add it to the system PATH.

#### LibreOffice or unoconv/unoserver (Optional tools for .ppt to .pptx conversion):

Linux:

- Debian/Ubuntu:
    ```sh 
    sudo apt install libreoffice unoconv
    ```
- Arch Linux:
    ```sh 
    sudo pacman -S libreoffice-fresh
    ```
- Fedora:
    ```sh 
    sudo dnf install libreoffice unoconv
    ```

macOS:

    ```sh 
    brew install libreoffice
    ```

for `unoserver`:

    ```sh 
    pip install unoserver
    ```

#### If the installation script didn't process the packages correctly, you can install them directly:

```sh 
pip install -r requirements.txt
```

Or if the `requirements.txt` is missing, install the required packages manually:

```sh 
pip install python-dotenv langchain langchain-google-genai google-generativeai PyPDF2 python-pptx pyfiglet pytesseract pdf2image Pillow
```

## Environment Variables

Before running the program, create a `.env` file in your root project (or use the provided `.env.example` as a guide).
Include your Gemini API key:

```sh 
GEMINI_API_KEY=your_api_key_here
```

_Optionally; set the Tesseract command if it not in your PATH:_

```sh 
TESSERACT_CMD=/path/to/tesseract  # Linux/macOS
TESSERACT_CMD=C:\\Program Files\\Tesseract-OCR\\tesseract.exe  # Windows
```

## Usage

Currently there are two options to choose from for usage:
1. Provide the path in CLI Arugments
```bash
python3 main.py path/to/file
```
2. Enter the path when prompted
```bash
python3 main.py
```
and then enter the path when prompted:
```bash
Please enter the path to your file (.pdf, .pptx, or .ppt): path/to/file
```
_Currently only 1 file can be processed at a time._

To exit the program, press `Ctrl + C`. Or, if you are prompted, type `exit` and press `Enter`.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for discussion.
