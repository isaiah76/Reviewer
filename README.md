# Reviewer

Reviewer is a Python program that extracts text from PDF documents and summarizes it into key points and concise summaries. This program uses **LangChain** and **Google's Gemini**.

## Features

- Extract text from PDF documents.
- Summarize extracted text into bullet points.
- Easy integration with **LangChain** and **Google's Gemini** for efficient summarization.

## Requirements

- Python 3.7 or higher
- `dotenv`
- `langchain-google-genai`
- `PyPDF2`

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/reviewer.git
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

To use the Reviewer application, run the following command:
```bash
python3 main.py

```

You can specify the PDF file path in the script:
```bash
pdf_path = "./test.pdf"
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for discussion.
