# app/parser.py
from typing import Dict, Any, List
from openai import OpenAI
import json

class MSDSParser:
    def __init__(self, api_key: str):
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://nova-litellm-proxy.onrender.com"
        )
        
    def parse_msds(self, msds_text: str) -> Dict[str, Any]:
        """Parse MSDS text and return structured data."""
        
        system_prompt = """You are a specialized MSDS analysis system. Extract key safety information 
        from the provided MSDS and format it according to the specified structure. Only include 
        information that is explicitly stated in the MSDS. Do not leave any field blank.
        Use "Not specified" for missing information."""
        
        user_prompt = f"""Analyze this MSDS and extract key information:

        {msds_text}
        
        Format the response as a JSON object with the following structure:
        {{
            "chemical_name": string,
            "cas_number": string,
            "hazard_summary": {{
                "ghs_classification": string[],
                "signal_word": string,
                "primary_hazards": string[]
            }},
            "safety_requirements": {{
                "ppe_required": {{
                    "eye_protection": string,
                    "hand_protection": string,
                    "respiratory_protection": string,
                    "body_protection": string
                }},
                "storage_requirements": {{
                    "temperature": string,
                    "conditions": string[],
                    "incompatible_materials": string[]
                }}
            }},
            "emergency_procedures": {{
                "first_aid": {{
                    "inhalation": string,
                    "skin_contact": string,
                    "eye_contact": string,
                    "ingestion": string
                }},
                "fire_measures": {{
                    "suitable_extinguishing_media": string[],
                    "special_hazards": string[]
                }},
                "spill_response": string[]
            }}
        }}"""
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.1
            )
            
            parsed_response = json.loads(response.choices[0].message.content)
            
            if self.validate_response(parsed_response):
                return parsed_response
            else:
                raise ValueError("Invalid response structure")
                
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed",
                "original_text": msds_text[:100] + "..."
            }
    
    def validate_response(self, response: Dict[str, Any]) -> bool:
        """Validate that all required fields are present."""
        required_fields = [
            "chemical_name",
            "cas_number",
            "hazard_summary",
            "safety_requirements",
            "emergency_procedures"
        ]
        
        return all(field in response for field in required_fields)

class UniversityLabMSDSParser(MSDSParser):
    def parse_msds(self, msds_text: str) -> Dict[str, Any]:
        """Extended parser with university-specific requirements."""
        base_result = super().parse_msds(msds_text)
        
        # Add university-specific fields
        university_extensions = {
            "lab_specific_info": {
                "waste_disposal": self._extract_waste_disposal(msds_text),
                "storage_location": self._determine_storage_location(base_result),
                "training_required": self._determine_training_requirements(base_result),
                "student_restrictions": self._determine_student_restrictions(base_result)
            },
            "emergency_contacts": {
                "lab_manager": "Enter your lab manager contact",
                "safety_officer": "Enter safety officer contact",
                "poison_control": "1-800-222-1222"
            },
            "quick_reference": self._generate_quick_reference(base_result)
        }
        
        return {**base_result, **university_extensions}
    
    def _determine_storage_location(self, parsed_data: Dict) -> str:
        """Determine appropriate storage location based on hazards."""
        hazards = parsed_data.get("hazard_summary", {}).get("primary_hazards", [])
        
        if any("flammable" in hazard.lower() for hazard in hazards):
            return "Flammable Storage Cabinet"
        elif any("corrosive" in hazard.lower() for hazard in hazards):
            return "Corrosive Storage Cabinet"
        # Add more conditions as needed
        return "General Chemical Storage"
    
    def _determine_training_requirements(self, parsed_data: Dict) -> List[str]:
        """Determine required training based on hazards."""
        hazards = parsed_data.get("hazard_summary", {}).get("primary_hazards", [])
        training = ["Basic Lab Safety"]
        
        if any("flammable" in hazard.lower() for hazard in hazards):
            training.append("Fire Safety")
        if any("corrosive" in hazard.lower() for hazard in hazards):
            training.append("Corrosive Materials Handling")
            
        return training
    
    def _generate_quick_reference(self, parsed_data: Dict) -> Dict[str, str]:
        """Generate a quick reference card for lab users."""
        return {
            "minimum_ppe": ", ".join(
                filter(None, [
                    parsed_data.get("safety_requirements", {})
                    .get("ppe_required", {})
                    .get(ppe_type, "")
                    for ppe_type in ["eye_protection", "hand_protection"]
                ])
            ),
            "storage": self._determine_storage_location(parsed_data),
            "incompatible_with": ", ".join(
                parsed_data.get("safety_requirements", {})
                .get("storage_requirements", {})
                .get("incompatible_materials", ["None specified"])
            ),
            "emergency_response": "1. " + (
                parsed_data.get("emergency_procedures", {})
                .get("first_aid", {})
                .get("eye_contact", "Seek medical attention")
            )
        }

# Example usage, Univ parser.
# if __name__ == "__main__":
#     parser = UniversityLabMSDSParser(api_key=API_KEY)
#     result = parser.parse_msds(sample_msds)
#     print(json.dumps(result, indent=2))

# # Example usage, regular parser
# if __name__ == "__main__":
#     parser = MSDSParser(api_key=API_KEY)
    
#     # Example MSDS text (shortened for demonstration)
#     sample_msds = """[Your MSDS text would go here]"""
    
#     result = parser.parse_msds(sample_msds)
    
#     if parser.validate_response(result):
#         print(json.dumps(result, indent=2))
#     else:
#         print("Failed to extract all required information")