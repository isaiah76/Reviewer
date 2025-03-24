#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

echo "========================================="
echo "      REVIEWER - Linux Installer"
echo "========================================="
echo

# Check for python installation and version
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed or not in PATH."
    echo "Please install Python 3.8 or higher using your distribution's package manager."
    echo "For example: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

# Verify python version is >= 3.8
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if [[ "$(printf '%s\n' "3.8" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.8" ]]; then
    echo "Python 3.8 or higher is required. Your version is $PYTHON_VERSION."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install required packages
if [ -f requirements.txt ]; then
    echo "Installing packages from requirements.txt..."
    pip install --upgrade pip
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Installing default packages..."
    pip install --upgrade pip
    pip install python-dotenv langchain langchain-google-genai google-generativeai PyPDF2 python-pptx pyfiglet pytesseract pdf2image Pillow
fi

# Check for Tesseract OCR installation
if ! command -v tesseract &> /dev/null; then
    echo
    echo "Tesseract OCR is required for OCR functionality but was not found."
    echo "Please install Tesseract OCR using your distribution's package manager."
    echo "For Ubuntu/Debian: sudo apt install tesseract-ocr"
    echo "For Fedora: sudo dnf install tesseract"
    echo "For Arch: sudo pacman -S tesseract"
    echo
fi

# Check for Poppler (for pdf2image)
echo "Checking for Poppler (needed for PDF image extraction)..."
if ! command -v pdftoppm &> /dev/null; then
    echo "Poppler utilities not found. These are required for PDF image extraction."
    echo "Please install Poppler using your distribution's package manager:"
    echo "For Ubuntu/Debian: sudo apt install poppler-utils"
    echo "For Fedora: sudo dnf install poppler-utils"
    echo "For Arch: sudo pacman -S poppler"
    echo
fi

# Check for LibreOffice (for PPT conversion)
echo "Checking for LibreOffice (needed for PPT conversion)..."
if ! command -v soffice &> /dev/null; then
    echo "LibreOffice not found. This is required for PPT to PPTX conversion."
    echo "Please install LibreOffice using your distribution's package manager:"
    echo "For Ubuntu/Debian: sudo apt install libreoffice"
    echo "For Fedora: sudo dnf install libreoffice"
    echo "For Arch: sudo pacman -S libreoffice-still"
    echo
fi

# Create .env file for API key if it doesnt exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat <<EOF > .env
# Gemini API key
GEMINI_API_KEY=your_api_key_here
EOF
    echo
    echo "Please edit the .env file and add your Gemini API key."
fi

if [ -f reviewer.py ]; then
    chmod +x reviewer.py
fi

echo
echo "========================================="
echo "Installation Completed!"
echo
echo "To Run The Program:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the script: python3 main.py"
echo
echo "Note: Make sure to edit the .env file with your Gemini API key."
echo "========================================="

