import re
from typing import Dict

class SectionParser:
    SECTIONS = [
        "EDUCATION",
        "SKILLS", 
        "TOOLS",
        "LANGUAGE",
        "PROJECTS",
        "ACHIEVEMENTS & CERTIFICATES"
    ]
    
    @staticmethod
    def parse(text: str) -> Dict[str, str]:
        sections = {}
        lines = text.split("\n")
        
        # Find header end (before first section or after contact info)
        header_end = 0
        name_found = False
        
        for i, line in enumerate(lines):
            upper = line.upper().strip()
            
            # Check if this is a section header
            if upper in SectionParser.SECTIONS:
                header_end = i
                break
            
            # Look for "Business Analyst Intern" or similar job title
            if "INTERN" in upper or "ANALYST" in upper or "DEVELOPER" in upper:
                name_found = True
            
            # If we found name/title and see "About Me", header ends here
            if name_found and "ABOUT ME" in upper:
                header_end = i
                break
        
        # Extract header
        sections["HEADER"] = "\n".join(lines[:header_end]).strip()
        
        # Parse remaining sections
        current_section = None
        buffer = []
        
        for i in range(header_end, len(lines)):
            line = lines[i]
            upper = line.upper().strip()
            
            # Check for section headers
            found_section = None
            if upper in SectionParser.SECTIONS:
                found_section = upper
            elif upper == "ABOUT ME":
                found_section = "ABOUT_ME"
            
            if found_section:
                # Save previous section
                if current_section:
                    sections[current_section] = "\n".join(buffer).strip()
                current_section = found_section
                buffer = []
            else:
                buffer.append(line)
        
        # Save last section
        if current_section:
            sections[current_section] = "\n".join(buffer).strip()
        
        return sections