from fpdf import FPDF
import re

def clean_html_tags(text):
    """Remove HTML tags and clean up the text for PDF generation"""
    # Remove HTML tags
    clean_text = re.sub(r'<[^>]+>', '', text)
    # Remove multiple newlines
    clean_text = re.sub(r'\n\s*\n', '\n\n', clean_text)
    # Remove special characters
    clean_text = clean_text.replace('&nbsp;', ' ').replace('&amp;', '&')
    return clean_text.strip()

class ContentPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'AI - Content Generation Agent', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        # Split body into paragraphs
        paragraphs = body.split('\n\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                self.multi_cell(0, 10, paragraph.strip())
                self.ln(5)

def markdown_to_pdf(content, filename, topic):
    pdf = ContentPDF()
    pdf.add_page()
    
    # Clean and format the content
    clean_content = clean_html_tags(content)
    
    # Add title
    pdf.chapter_title(topic)
    
    # Add content
    pdf.chapter_body(clean_content)
    
    pdf.output(filename)