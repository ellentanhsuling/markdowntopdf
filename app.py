import streamlit as st
import markdown
import base64
import tempfile
import os
from weasyprint import HTML

def markdown_to_html(markdown_text):
    """Convert markdown text to HTML."""
    extensions = [
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.nl2br',
        'mdx_math'
    ]
    html = markdown.markdown(markdown_text, extensions=extensions)
    return html

def html_to_pdf(html_content):
    """Convert HTML to PDF using WeasyPrint."""
    # Create a temporary HTML file
    with tempfile.NamedTemporaryFile(suffix='.html', delete=False) as f:
        f.write(html_content.encode('utf-8'))
        temp_html_path = f.name
    
    # Convert HTML to PDF
    pdf_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    pdf_file.close()
    
    # Basic CSS for better PDF formatting
    css = """
    body { font-family: Arial, sans-serif; margin: 20px; }
    h1 { color: #2c3e50; }
    h2 { color: #3498db; }
    h3 { color: #2980b9; }
    code { background-color: #f8f8f8; padding: 2px 4px; border-radius: 4px; }
    pre { background-color: #f8f8f8; padding: 10px; border-radius: 4px; overflow-x: auto; }
    blockquote { border-left: 4px solid #ccc; padding-left: 15px; color: #555; }
    table { border-collapse: collapse; width: 100%; }
    th, td { border: 1px solid #ddd; padding: 8px; }
    th { background-color: #f2f2f2; }
    """
    
    # Create PDF with WeasyPrint
    HTML(temp_html_path).write_pdf(pdf_file.name, stylesheets=[CSS(string=css)])
    
    # Clean up the temporary HTML file
    os.unlink(temp_html_path)
    
    return pdf_file.name

def get_binary_file_downloader_html(bin_file, file_label='File'):
    """Generate a download link for a binary file."""
    with open(bin_file, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{file_label}.pdf">Download {file_label}</a>'

def main():
    st.set_page_config(
        page_title="Markdown to PDF Converter",
        page_icon="📝",
        layout="wide"
    )
    
    st.title("Markdown to PDF Converter")
    st.write("Upload, edit, preview, and convert markdown files to PDF")
    
    # Initialize session state for markdown content
    if 'markdown_content' not in st.session_state:
        st.session_state.markdown_content = "# Hello, World!\n\nThis is a sample markdown document."
    
    # File uploader
    uploaded_file = st.file_uploader("Upload a markdown file", type=['md', 'markdown'])
    if uploaded_file is not None:
        st.session_state.markdown_content = uploaded_file.getvalue().decode('utf-8')
    
    # Create two columns for editor and preview
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Markdown Editor")
        new_content = st.text_area("Edit your markdown here:", st.session_state.markdown_content, height=400)
        if new_content != st.session_state.markdown_content:
            st.session_state.markdown_content = new_content
    
    with col2:
        st.subheader("Preview")
        html_content = markdown_to_html(st.session_state.markdown_content)
        st.markdown(html_content, unsafe_allow_html=True)
    
    # Convert to PDF and provide download link
    if st.button("Generate PDF"):
        with st.spinner("Generating PDF..."):
            # Convert markdown to HTML
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>Markdown to PDF</title>
            </head>
            <body>
                {markdown_to_html(st.session_state.markdown_content)}
            </body>
            </html>
            """
            
            # Convert HTML to PDF
            pdf_path = html_to_pdf(html_content)
            
            # Create download link
            st.success("PDF generated successfully!")
            st.markdown(get_binary_file_downloader_html(pdf_path, "markdown_document"), unsafe_allow_html=True)

if __name__ == "__main__":
    from streamlit.web.bootstrap import run
    
    # Fix for WeasyPrint CSS
    class CSS:
        def __init__(self, string=None):
            self.string = string
    
    main()