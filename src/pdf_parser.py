import os
import re
import logging
from dataclasses import dataclass
import pdfminer.high_level

@dataclass
class DocumentSection:
    filename: str
    title: str
    page: int
    text: str

class DocumentParser:
    def __init__(self):
        self.title_pattern = re.compile(
            r'^(?:(?:[A-Z][a-z]*\b\s*)+|(?:[A-Z]+\b\s*)+)$'
        )
    
    def process_document(self, filepath: str) -> list:
        if not os.path.exists(filepath):
            logging.warning(f"File not found: {filepath}")
            return []
        
        try:
            raw_text = pdfminer.high_level.extract_text(filepath)
            pages = raw_text.split("\f")
            sections = self._split_into_sections(pages, os.path.basename(filepath))
            return sections
        except Exception as e:
            logging.error(f"Error processing {filepath}: {str(e)}")
            return []
    
    def _split_into_sections(self, pages: list, filename: str) -> list:
        sections = []
        current_title = "Introduction"
        current_page = 1
        buffer = []
        
        for page_num, page_content in enumerate(pages, start=1):
            lines = page_content.splitlines()
            for line in lines:
                stripped = line.strip()
                
                # Check if line is a section heading
                if self._is_heading(stripped):
                    if buffer:
                        sections.append(self._create_section(
                            filename, current_title, current_page, buffer
                        ))
                        buffer = []
                    current_title = stripped
                    current_page = page_num
                elif stripped:
                    buffer.append(stripped)
            
            # Handle page breaks within sections
            if buffer and buffer[-1] != "":
                buffer.append("")
        
        # Add final section
        if buffer:
            sections.append(self._create_section(
                filename, current_title, current_page, buffer
            ))
        
        return sections or [self._create_fallback_section(filename, pages)]
    
    def _is_heading(self, text: str) -> bool:
        if len(text) < 6 or len(text) > 120:
            return False
        if not self.title_pattern.match(text):
            return False
        return len(text.split()) < 8
    
    def _create_section(self, filename, title, page, buffer):
        return DocumentSection(
            filename=filename,
            title=title,
            page=page,
            text="\n".join(buffer).strip()
        )
    
    def _create_fallback_section(self, filename, pages):
        full_text = " ".join(p.strip() for p in pages if p.strip())
        return DocumentSection(
            filename=filename,
            title=os.path.basename(filename),
            page=1,
            text=full_text
        )