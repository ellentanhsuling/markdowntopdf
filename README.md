# Markdown to PDF Converter

A Streamlit application that allows users to upload, edit, preview, and convert markdown files to PDF.

## Features

- Upload markdown files
- Edit markdown content in the browser
- Live preview of rendered markdown
- Convert markdown to PDF
- Download the generated PDF

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/ellentanhsuling/markdowntopdf.git
   cd markdowntopdf
   ```

2. Install wkhtmltopdf (required for PDF generation):
   - **Windows**: Download and install from [wkhtmltopdf downloads](https://wkhtmltopdf.org/downloads.html)
   - **macOS**: `brew install wkhtmltopdf`
   - **Ubuntu/Debian**: `sudo apt-get install wkhtmltopdf`
   - **CentOS/RHEL**: `sudo yum install wkhtmltopdf`

3. Install the required Python dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   streamlit run app.py
   ```

   If you encounter issues with wkhtmltopdf, try the alternative version:
   ```
   streamlit run app_alternative.py
   ```

## Usage

1. Upload a markdown file using the file uploader
2. Edit the markdown content in the editor
3. Preview the rendered markdown in real-time
4. Click "Generate PDF" to convert the markdown to PDF
5. Download the generated PDF using the provided link

## Requirements

- Python 3.7+
- Streamlit
- wkhtmltopdf (for app.py) or fpdf2 (for app_alternative.py)
- Markdown

## License

MIT
