import streamlit as st
import markdown
import base64
import tempfile
import os
from fpdf import FPDF, HTMLMixin

class HTML2PDF(FPDF, HTMLMixin):
    pass

def markdown_to_html(markdown_text):
    """Convert markdown text to HTML."""
    extensions = [
        'markdown.extensions.tables',
        'markdown.extensions.fenced_code',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
        'markdown.extensions.nl2br',
    ]
    html = markdown.markdown(markdown_text, extensions=extensions)
    return html

def html_to_pdf(html_content):
    """Convert HTML to PDF using FPDF."""
    # Create a PDF document
    pdf = HTML2PDF()
    pdf.add_page()
    pdf.write_html(html_content)
    
    # Save to a temporary file
    pdf_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
    pdf_file.close()
    pdf.output(pdf_file.name)
    
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
            html_content = markdown_to_html(st.session_state.markdown_content)
            
            # Convert HTML to PDF
            pdf_path = html_to_pdf(html_content)
            
            # Create download link
            st.success("PDF generated successfully!")
            st.markdown(get_binary_file_downloader_html(pdf_path, "markdown_document"), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
