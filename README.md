# Reviewer

Reviewer is a Python program that extracts text from PDF and PowerPoint documents (.pdf, .pptx, .ppt) and summarizes it into key points and concise summaries. This program uses **LangChain** and **Google's Gemini**.

## Features

- Extract text from PDF and PowerPoint files.
 -Automatically convert .ppt files to .pptx format when needed.
- Summarize extracted text into bullet points.
- Easy integration with **LangChain** and **Google's Gemini** for efficient summarization.

## Requirements

- Python 3.7 or higher
- `dotenv`
- `langchain-google-genai`
- `PyPDF2`
- `python-pptx`
- Optional tools for .ppt to .pptx conversion:
  - Windows OS: `Microsoft PowerPoint`
  - Linux /Mac OS: `LibreOffice`

_It is recommended to install `unoconv` or `unoserver` aside from `LibreOffice` for better performance._

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Isaiah512/Reviewer.git
   cd reviewer
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables:
- Create a .env file in the root directory of the project and add your Gemini API key:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
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

To exit the program, press `Ctrl + C`. Or, if you are prompted to enter a path, type `exit` and press `Enter`.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for discussion.
