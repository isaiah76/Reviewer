@echo off
REM =========================================
REM      REVIEWER - Windows Installer
REM =========================================
echo.

:: Check for Python installation and version
python --version >NUL 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python is not installed. Downloading installer...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe' -OutFile 'python-installer.exe'}"
    
    echo Installing Python...
    start /wait python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
    
    del python-installer.exe
    python --version >NUL 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo Python installation failed. Please install it manually from https://www.python.org/downloads/
        pause
        exit /b 1
    )
    echo Python installed successfully!
)

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

:: Install required packages
if exist requirements.txt (
    echo Installing packages from requirements.txt...
    pip install --upgrade pip
    pip install -r requirements.txt
) else (
    echo Installing required packages...
    pip install --upgrade pip
    pip install python-dotenv langchain langchain-google-genai google-generativeai PyPDF2 python-pptx pyfiglet pytesseract pdf2image Pillow
)
if %ERRORLEVEL% NEQ 0 (
    echo Package installation failed.
    pause
    exit /b 1
)

:: Check if Tesseract OCR is installed
where tesseract >NUL 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Tesseract OCR is required for OCR functionality but was not found.
    echo Please install Tesseract OCR from https://github.com/UB-Mannheim/tesseract/wiki
    echo Make sure to add it to your PATH after installation.
    echo.
)

:: Create .env file for API key if it doesn't exist
if not exist .env (
    echo Creating .env file...
    (
        echo # Gemini API key
        echo GEMINI_API_KEY=your_api_key_here
    ) > .env
    echo.
    echo Please edit the .env file and add your Gemini API key.
)

echo.
echo =========================================
echo Installation Completed!
echo.
echo To Run The Program:
echo 1. Activate the virtual environment: "venv\Scripts\activate"
echo 2. Run the script: "python reviewer.py"
echo.
echo Note: Make sure to edit the .env file with your Gemini API key.
echo =========================================
echo.
pause

