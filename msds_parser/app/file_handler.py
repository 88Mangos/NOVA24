import PyPDF2
import io
from typing import Dict, Any
from pathlib import Path

class MSDSFileHandler:
    """Handles different MSDS file formats"""
    
    @staticmethod
    def read_pdf(file) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(file.read()))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Error reading PDF: {str(e)}")
    
    @staticmethod
    def read_text(file) -> str:
        """Read text/markdown file"""
        try:
            return file.read().decode('utf-8')
        except Exception as e:
            raise ValueError(f"Error reading text file: {str(e)}")
    
    @staticmethod
    def process_file(file) -> str:
        """Process uploaded file based on type"""
        file_extension = Path(file.name).suffix.lower()
        
        if file_extension == '.pdf':
            return MSDSFileHandler.read_pdf(file)
        elif file_extension in ['.txt', '.md']:
            return MSDSFileHandler.read_text(file)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")