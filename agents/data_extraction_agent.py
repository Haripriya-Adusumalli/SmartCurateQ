import PyPDF2
import json
import os
import re
from typing import Dict, Any
from config import Config

# Cloud-safe imports
try:
    import vertexai
    from vertexai.generative_models import GenerativeModel
    VERTEX_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] Vertex AI not available: {e}")
    vertexai = None
    GenerativeModel = None
    VERTEX_AVAILABLE = False

class DataExtractionAgent:
    def __init__(self):
        print(f"[INFO] Initializing DataExtractionAgent...")
        self.model = None
        self.vertex_initialized = False
        
        if not VERTEX_AVAILABLE:
            print("[WARNING] Vertex AI not available - using fallback mode")
            return
            
        try:
            # Initialize Vertex AI with proper error handling
            vertexai.init(project=Config.PROJECT_ID, location=Config.LOCATION)
            self.model = GenerativeModel('gemini-2.5-pro')  # Use available model
            self.vertex_initialized = True
            print("[SUCCESS] Vertex AI initialized")
        except Exception as e:
            print(f"[ERROR] Vertex AI init failed: {e}")
            self.model = None
            self.vertex_initialized = False
    
    def extract_from_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """Extract text from PDF pitch deck"""
        print(f"[INFO] ===== PDF EXTRACTION START =====")
        print(f"[INFO] Processing PDF: {os.path.basename(pdf_path)}")
        print(f"[INFO] VERTEX_AVAILABLE: {VERTEX_AVAILABLE}")
        print(f"[INFO] Model initialized: {self.model is not None}")
        print(f"[INFO] Vertex initialized: {getattr(self, 'vertex_initialized', False)}")
        
        try:
            # Extract text from PDF
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for i, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                        print(f"[DEBUG] Page {i+1}: {len(page_text)} chars")
            
            filename = os.path.basename(pdf_path)
            company_name = self._clean_filename(filename)
            
            print(f"[INFO] Total extracted: {len(text)} chars from {len(reader.pages)} pages")
            print(f"[INFO] Company name from filename: {company_name}")
            print(f"[DEBUG] Text preview: {text[:300]}...")
            
            # If minimal text, return fallback
            if len(text.strip()) < 50:
                print("[WARNING] Minimal text extracted - using fallback")
                print(f"[DEBUG] Text content: '{text.strip()}'")
                return self._create_fallback_result(company_name)
            
            # Try AI extraction if available
            if VERTEX_AVAILABLE and self.model:
                print("[INFO] ===== USING AI EXTRACTION =====")
                result = self._extract_with_ai(text, company_name)
                print(f"[SUCCESS] AI extraction result: {result}")
                return result
            else:
                print("[INFO] ===== USING RULE-BASED EXTRACTION =====")
                print(f"[DEBUG] VERTEX_AVAILABLE: {VERTEX_AVAILABLE}, model: {self.model is not None}")
                result = self._extract_with_rules(text, company_name)
                print(f"[SUCCESS] Rule-based extraction result: {result}")
                return result
                
        except Exception as e:
            print(f"[ERROR] PDF processing failed: {e}")
            import traceback
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            return self._create_fallback_result("Unknown")
    
    def _extract_with_ai(self, text: str, company_name: str) -> Dict[str, Any]:
        """Extract using Vertex AI"""
        print(f"[AI] Starting AI extraction for: {company_name}")
        try:
            prompt = f"""Analyze this startup pitch deck and extract detailed information:

{text[:15000]}

Extract and return ONLY valid JSON:
{{
  "company_name": "{company_name or 'Unknown'}",
  "problem_statement": "What specific problem does this startup solve?",
  "solution": "How does the startup solve this problem? What is their product/service?",
  "founders": [
    {{
      "name": "Full founder name",
      "background": "Previous experience, education, expertise",
      "experience_years": 5,
      "domain_expertise": "Relevant domain",
      "previous_exits": 0
    }}
  ]
}}

Look for:
- Founder names, titles, backgrounds
- Previous companies, education
- Years of experience
- Domain expertise
- Any exits or achievements

Return only the JSON object."""

            print(f"[AI] Sending prompt to Vertex AI (length: {len(prompt)} chars)")
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            print(f"[AI] Raw response: {result_text}")
            
            # Clean JSON from response
            if '```' in result_text:
                start = result_text.find('{')
                end = result_text.rfind('}') + 1
                if start != -1 and end > start:
                    result_text = result_text[start:end]
                    print(f"[AI] Cleaned JSON: {result_text}")
            
            result = json.loads(result_text)
            print(f"[AI] Parsed JSON successfully: {result}")
            
            result.update({
                "market_size": 1000000000,
                "revenue": 0,
                "employees": len(result.get('founders', [])) or 1,
                "funding_stage": "Seed"
            })
            
            print(f"[SUCCESS] AI extraction completed for {result.get('company_name')}")
            return result
            
        except Exception as e:
            print(f"[ERROR] AI extraction failed: {e}")
            import traceback
            print(f"[ERROR] AI extraction traceback: {traceback.format_exc()}")
            print(f"[FALLBACK] Switching to rule-based extraction")
            return self._extract_with_rules(text, company_name)
    
    def _extract_with_rules(self, text: str, company_name: str) -> Dict[str, Any]:
        """Rule-based extraction fallback"""
        # Simple keyword-based extraction
        problem_keywords = ['problem', 'challenge', 'issue', 'pain point']
        solution_keywords = ['solution', 'solve', 'address', 'platform']
        
        problem = "Business problem identified in pitch deck"
        solution = "Technology solution described in pitch deck"
        
        # Try to find problem/solution in text
        text_lower = text.lower()
        for keyword in problem_keywords:
            if keyword in text_lower:
                # Extract sentence containing keyword
                sentences = text.split('.')
                for sentence in sentences:
                    if keyword in sentence.lower():
                        problem = sentence.strip()[:200]
                        break
                break
        
        return {
            "company_name": company_name or "Company from PDF",
            "problem_statement": problem,
            "solution": solution,
            "market_size": 1000000000,
            "revenue": 0,
            "employees": 3,
            "funding_stage": "Seed",
            "founders": [{"name": "Founder", "background": "Entrepreneur"}]
        }
    
    def _create_fallback_result(self, company_name: str) -> Dict[str, Any]:
        return {
            "company_name": company_name or "Unknown Company",
            "problem_statement": "Please review pitch deck manually",
            "solution": "Please review pitch deck manually", 
            "market_size": 1000000000,
            "revenue": 0,
            "employees": 1,
            "funding_stage": "Seed",
            "founders": [{"name": "Founder", "background": "Entrepreneur"}]
        }
    
    def extract_from_form(self, form_data: Dict) -> Dict[str, Any]:
        return form_data
    
    def _clean_filename(self, filename: str) -> str:
        """Clean filename to extract company name"""
        name = filename.replace('.pdf', '').replace('.PDF', '')
        
        # Remove temp prefix
        if name.startswith('temp_'):
            name = name[5:]
        elif name.startswith('temp '):
            name = name[5:]
        
        # Remove numbers and dots at the beginning (e.g., "01. ")
        name = re.sub(r'^\d+\.?\s*', '', name)
        
        # Remove common patterns
        name = re.sub(r'(detailed|deck|pitch|20\d{2})', '', name, flags=re.IGNORECASE)
        name = name.replace('_', ' ').replace('-', ' ')
        name = ' '.join(name.split())
        
        return name.strip() if name.strip() else None