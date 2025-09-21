import PyPDF2
import json
from typing import Dict, Any
from config import Config

try:
    from google.cloud import vision
    VISION_AVAILABLE = True
except ImportError:
    VISION_AVAILABLE = False
    vision = None

try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False
    vertexai = None
    GenerativeModel = None

class DataExtractionAgent:
    def __init__(self):
        if VERTEX_AI_AVAILABLE and Config.USE_VERTEX_AI:
            vertexai.init(project=Config.PROJECT_ID, location=Config.LOCATION)
            self.model = GenerativeModel('gemini-pro')
            self.use_vertex = True
        else:
            self.model = None
            self.use_vertex = False
        self.vision_client = vision.ImageAnnotatorClient() if VISION_AVAILABLE else None
    
    def extract_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Extract text from PDF pitch deck"""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
        
        # Debug: Print first 500 chars to see what we're getting
        print(f"PDF Text Preview: {text[:500]}")
        
        return self._analyze_pitch_content(text)
    
    def extract_from_form(self, form_data: Dict) -> Dict[str, Any]:
        """Process Google Form responses"""
        try:
            if self.use_vertex and self.model:
                prompt = f"""
                Analyze this startup form data and extract key information:
                {json.dumps(form_data, indent=2)}
                
                Extract and structure:
                - Company name and description
                - Founder backgrounds
                - Problem and solution
                - Market size claims
                - Revenue and metrics
                - Funding requirements
                
                Return as JSON.
                """
                
                response = self.model.generate_content(prompt)
                return json.loads(response.text)
            else:
                # Return the form data as-is when AI is not available
                return form_data
        except:
            # Return the form data as-is for testing
            return form_data
    
    def _analyze_pitch_content(self, content: str) -> Dict[str, Any]:
        """Analyze pitch deck content using Gemini AI"""
        if self.use_vertex and self.model:
            prompt = f"""
            Extract startup information from this pitch deck content:
            
            {content[:4000]}
            
            Please extract and return ONLY a valid JSON object with these fields:
            - company_name: The actual company/startup name
            - problem_statement: The problem they are solving
            - solution: Their solution to the problem
            - founder_name: Name of the founder/CEO
            - founder_background: Founder's background/experience
            
            Return format:
            {{
                "company_name": "actual company name",
                "problem_statement": "problem description",
                "solution": "solution description",
                "market_size": 2000000000,
                "revenue": 250000,
                "employees": 8,
                "funding_stage": "Seed",
                "founders": [{{"name": "founder name", "background": "founder background", "experience_years": 6, "previous_exits": 0, "domain_expertise": "Business"}}]
            }}
            """
            
            try:
                response = self.model.generate_content(prompt)
                # Clean the response to extract JSON
                response_text = response.text.strip()
                if '```json' in response_text:
                    response_text = response_text.split('```json')[1].split('```')[0]
                elif '```' in response_text:
                    response_text = response_text.split('```')[1]
                
                result = json.loads(response_text.strip())
                return result
            except Exception as e:
                print(f"Gemini extraction failed: {e}")
        
        # Simple extraction from actual PDF content
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # Find company name - first substantial line
        company_name = lines[0] if lines else "PDF Company"
        
        # Find problem - look for text after "problem" keyword
        problem = "Problem from PDF"
        for i, line in enumerate(lines):
            if 'problem' in line.lower():
                # Take next non-empty line
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j] and len(lines[j]) > 10:
                        problem = lines[j]
                        break
                break
        
        # Find solution - look for text after "solution" keyword
        solution = "Solution from PDF"
        for i, line in enumerate(lines):
            if 'solution' in line.lower():
                # Take next non-empty line
                for j in range(i+1, min(i+5, len(lines))):
                    if lines[j] and len(lines[j]) > 10:
                        solution = lines[j]
                        break
                break
        
        # Find founder name
        founder_name = "PDF Founder"
        for line in lines:
            if any(word in line.lower() for word in ['founder', 'ceo']):
                # Extract name from the line
                parts = line.split()
                for i, part in enumerate(parts):
                    if part.lower() in ['founder', 'ceo'] and i+1 < len(parts):
                        founder_name = parts[i+1]
                        break
                break
        
        print(f"Extracted - Company: {company_name}, Problem: {problem[:50]}, Solution: {solution[:50]}, Founder: {founder_name}")
        
        return {
            "company_name": company_name,
            "problem_statement": problem,
            "solution": solution,
            "market_size": 2000000000,
            "revenue": 250000,
            "employees": 8,
            "funding_stage": "Seed",
            "founders": [{
                "name": founder_name,
                "background": "Experienced entrepreneur",
                "experience_years": 6,
                "previous_exits": 0,
                "domain_expertise": "Business"
            }]
        }