import re
from typing import Dict, Any, List, Optional

class FlexibleCVParser:
    """
    Parser linh hoạt có thể xử lý nhiều format CV khác nhau
    """
    
    # Các từ khóa section có thể có (tiếng Anh và tiếng Việt)
    SECTION_KEYWORDS = {
        'education': ['education', 'học vấn', 'đào tạo', 'academic'],
        'experience': ['experience', 'kinh nghiệm', 'work history', 'employment'],
        'skills': ['skills', 'kỹ năng', 'technical skills', 'competencies'],
        'projects': ['projects', 'dự án', 'personal projects'],
        'achievements': ['achievements', 'thành tích', 'awards', 'certificates', 'certifications', 'giải thưởng', 'chứng chỉ'],
        'tools': ['tools', 'công cụ', 'technologies', 'software'],
        'languages': ['languages', 'ngôn ngữ', 'language skills'],
        'about': ['about', 'summary', 'profile', 'objective', 'giới thiệu', 'tóm tắt']
    }
    
    @staticmethod
    def normalize_text(text: str) -> str:
        """Chuẩn hóa text cơ bản"""
        if not text:
            return ""
        
        # Remove các ký tự bullet đặc biệt
        text = re.sub(r"[¢•·▪■○●◦➢➤→]", "", text)
        # Remove 'e' làm bullet
        text = re.sub(r"\ne\s+", "\n", text)
        text = re.sub(r"^e\s+", "", text)
        # Normalize spaces
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        
        lines = [line.strip() for line in text.split("\n")]
        return "\n".join(lines)
    
    @staticmethod
    def detect_section(line: str) -> Optional[str]:
        """
        Phát hiện loại section dựa trên keywords
        Returns: section_type hoặc None
        """
        line_lower = line.lower().strip()
        
        # Bỏ qua nếu dòng quá dài (không phải header)
        if len(line.split()) > 6:
            return None
        
        for section_type, keywords in FlexibleCVParser.SECTION_KEYWORDS.items():
            for keyword in keywords:
                if keyword in line_lower:
                    # Kiểm tra xem có phải header không (thường ngắn, có thể in hoa)
                    if len(line) < 50:
                        return section_type
        
        return None
    
    @staticmethod
    def extract_contact_info(text: str) -> Dict[str, str]:
        """Trích xuất thông tin liên hệ từ toàn bộ CV"""
        contact = {
            'email': '',
            'phone': '',
            'address': '',
            'linkedin': '',
            'github': ''
        }
        
        # Email
        email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        if email_match:
            contact['email'] = email_match.group(0)
        
        # Phone - nhiều formats
        phone_patterns = [
            r'\+?84[\s\)]?\d[\d\s]{8,}',  # VN format
            r'\+?\d{1,3}[\s\-\.]?\(?\d{3}\)?[\s\-\.]?\d{3}[\s\-\.]?\d{4}',  # US format
            r'\d{10,11}',  # Simple format
        ]
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact['phone'] = phone_match.group(0).strip()
                break
        
        # LinkedIn
        linkedin_match = re.search(r'linkedin\.com/in/[\w\-]+', text, re.IGNORECASE)
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group(0)
        
        # GitHub
        github_match = re.search(r'github\.com/[\w\-]+', text, re.IGNORECASE)
        if github_match:
            contact['github'] = github_match.group(0)
        
        # Address - tìm dòng có địa chỉ (chứa số + tên đường/quận)
        address_patterns = [
            r'\d+[-,\s]+[^\n]*(?:Street|St|Avenue|Ave|Road|Rd|Ward|District|Quận|Phường)[^\n]*',
            r'[^\n]*(?:Ward|District|Quận|Phường)[^\n]*'
        ]
        for pattern in address_patterns:
            address_match = re.search(pattern, text, re.IGNORECASE)
            if address_match:
                contact['address'] = address_match.group(0).strip()
                break
        
        return contact
    
    @staticmethod
    def extract_name(text: str) -> str:
        """
        Thử tìm tên ứng viên
        - Thường là dòng ALL CAPS đầu tiên (2-4 từ)
        - Hoặc sau "Name:", "Họ tên:"
        """
        lines = text.split("\n")[:20]  # Chỉ xét 20 dòng đầu
        
        # Tìm pattern "Name:" hoặc "Họ tên:"
        for line in lines:
            if re.match(r'(name|họ tên|tên)[\s:]+', line, re.IGNORECASE):
                name = re.sub(r'(name|họ tên|tên)[\s:]+', '', line, flags=re.IGNORECASE).strip()
                if name:
                    return name
        
        # Tìm dòng ALL CAPS (2-4 từ, không chứa ký tự đặc biệt)
        for line in lines:
            line = line.strip()
            words = line.split()
            if (line.isupper() and 
                2 <= len(words) <= 5 and 
                re.match(r'^[A-Z\s]+$', line) and
                '@' not in line and '+' not in line):
                return line
        
        return "Unknown"
    
    @staticmethod
    def parse(raw_text: str) -> Dict[str, Any]:
        """
        Parse CV với cấu trúc linh hoạt
        """
        text = FlexibleCVParser.normalize_text(raw_text)
        lines = text.split("\n")
        
        # Extract thông tin cơ bản
        name = FlexibleCVParser.extract_name(text)
        contact = FlexibleCVParser.extract_contact_info(text)
        
        # Parse sections
        sections = {}
        current_section = None
        buffer = []
        
        for line in lines:
            if not line.strip():
                continue
            
            # Kiểm tra xem có phải section header không
            detected_section = FlexibleCVParser.detect_section(line)
            
            if detected_section:
                # Lưu section trước đó
                if current_section and buffer:
                    sections[current_section] = "\n".join(buffer).strip()
                
                current_section = detected_section
                buffer = []
            elif current_section:
                buffer.append(line)
        
        # Lưu section cuối
        if current_section and buffer:
            sections[current_section] = "\n".join(buffer).strip()
        
        # Cấu trúc output
        result = {
            'name': name,
            'contact': contact,
            'education': sections.get('education', ''),
            'experience': sections.get('experience', ''),
            'skills': FlexibleCVParser._parse_list(sections.get('skills', '')),
            'tools': FlexibleCVParser._parse_list(sections.get('tools', '')),
            'languages': FlexibleCVParser._parse_list(sections.get('languages', '')),
            'about': sections.get('about', ''),
            'projects': FlexibleCVParser._parse_projects(sections.get('projects', '')),
            'achievements': FlexibleCVParser._parse_list(sections.get('achievements', ''))
        }
        
        return result
    
    @staticmethod
    def _parse_list(text: str) -> List[str]:
        """Parse text thành list items"""
        if not text:
            return []
        
        items = []
        for line in text.split("\n"):
            line = line.strip()
            # Remove bullet characters
            line = re.sub(r'^[-•◦●○]\s*', '', line)
            if line:
                items.append(line)
        
        return items
    
    @staticmethod
    def _parse_projects(text: str) -> List[Dict[str, Any]]:
        """Parse projects section"""
        if not text:
            return []
        
        projects = []
        current_project = None
        
        for line in text.split("\n"):
            line = line.strip()
            if not line:
                continue
            
            # Kiểm tra nếu là role
            is_role = any(kw in line for kw in ['Developer', 'Engineer', 'Analyst', 'Designer', 'Leader'])
            
            # Kiểm tra nếu là link
            is_link = 'http' in line or 'github' in line.lower()
            
            # Nếu không phải role/link và chưa có project, đây là title
            if not is_role and not is_link and not current_project:
                current_project = {
                    'title': line,
                    'role': '',
                    'description': [],
                    'links': []
                }
            elif not is_role and not is_link and current_project and current_project.get('role'):
                # Nếu đã có role, đây có thể là project mới
                if len(line.split()) <= 6 and line[0].isupper():
                    projects.append(current_project)
                    current_project = {
                        'title': line,
                        'role': '',
                        'description': [],
                        'links': []
                    }
                else:
                    current_project['description'].append(line)
            elif current_project:
                if is_role and not current_project['role']:
                    current_project['role'] = line
                elif is_link:
                    url = re.search(r'https?://[^\s]+', line)
                    if url:
                        current_project['links'].append(url.group(0))
                else:
                    current_project['description'].append(line)
        
        if current_project:
            projects.append(current_project)
        
        return projects
    
    @staticmethod
    def to_json(raw_text: str) -> Dict[str, Any]:
        """
        Parse CV và trả về JSON format
        """
        return FlexibleCVParser.parse(raw_text)
    
    @staticmethod
    def to_markdown(cv_data: Dict[str, Any]) -> str:
        """Convert parsed data to markdown"""
        md = f"""# {cv_data['name']}
        ## Contact Information
        """
        contact = cv_data['contact']
        if contact['email']:
            md += f"- **Email:** {contact['email']}\n"
        if contact['phone']:
            md += f"- **Phone:** {contact['phone']}\n"
        if contact['address']:
            md += f"- **Address:** {contact['address']}\n"
        if contact['linkedin']:
            md += f"- **LinkedIn:** {contact['linkedin']}\n"
        if contact['github']:
            md += f"- **GitHub:** {contact['github']}\n"
        
        if cv_data['about']:
            md += f"\n## 💼 About Me\n{cv_data['about']}\n"
        
        if cv_data['education']:
            md += f"\n## 🎓 Education\n{cv_data['education']}\n"
        
        if cv_data['experience']:
            md += f"\n## 💼 Work Experience\n{cv_data['experience']}\n"
        
        if cv_data['skills']:
            md += "\n## 🛠 Skills\n"
            for skill in cv_data['skills']:
                md += f"- {skill}\n"
        
        if cv_data['tools']:
            md += "\n## 🧰 Tools & Technologies\n"
            for tool in cv_data['tools']:
                md += f"- {tool}\n"
        
        if cv_data['languages']:
            md += "\n## 🌍 Languages\n"
            for lang in cv_data['languages']:
                md += f"- {lang}\n"
        
        if cv_data['projects']:
            md += "\n## 🚀 Projects\n"
            for proj in cv_data['projects']:
                md += f"\n### {proj['title']}\n"
                if proj['role']:
                    md += f"*{proj['role']}*\n\n"
                for desc in proj['description']:
                    md += f"- {desc}\n"
                for link in proj['links']:
                    md += f"- **Link:** {link}\n"
        
        if cv_data['achievements']:
            md += "\n## 🏆 Achievements & Certificates\n"
            for ach in cv_data['achievements']:
                md += f"- {ach}\n"
        
        return md.strip()
