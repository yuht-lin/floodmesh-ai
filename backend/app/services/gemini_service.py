import os
import re
import json
from google import genai
from google.genai import types


class GeminiService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.client = None
        if self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"[Gemini Auth Notice]: {e}")

    def _local_fallback_extraction(self, text: str) -> dict:
        text_lower = text.lower()

        # Extract number of people affected
        numbers = re.findall(r"(\d+)\s*(?:people|persons|victims|trapped|stuck|stranded|affected|members)?", text_lower)
        people_count = 1
        if numbers:
            try:
                valid_nums = [int(n) for n in numbers if int(n) > 0]
                if valid_nums:
                    people_count = max(valid_nums)
            except ValueError:
                people_count = 1

        # Extract urgency based on keywords or population size
        if people_count >= 50 or any(w in text_lower for w in ["critical", "dying", "head injury", "unconscious", "pregnant", "medicine", "medical"]):
            urgency = "critical"
        elif people_count >= 15 or any(w in text_lower for w in ["urgent", "danger", "rising rapidly", "roof", "trapped", "boat", "food"]):
            urgency = "high"
        else:
            urgency = "medium"

        isolation = "high" if any(w in text_lower for w in ["cut off", "no road", "isolated", "island"]) else "medium"

        return {
            "people_affected": people_count,
            "medical_urgency": urgency,
            "isolation_level": isolation,
            "latitude": None,
            "longitude": None,
        }

    async def extract_incident_info(self, raw_text: str) -> dict:
        if not self.client and os.getenv("GEMINI_API_KEY"):
            try:
                self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
            except Exception:
                self.client = None

        if not self.client:
            return self._local_fallback_extraction(raw_text)

        prompt = f"""
        Extract disaster details from the following distress message in JSON format.
        Distress Message: "{raw_text}"
        
        Respond ONLY with a JSON object containing:
        - people_affected: (integer)
        - medical_urgency: ("critical", "high", "medium", "low")
        - isolation_level: ("high", "medium", "low")
        - latitude: (float or null)
        - longitude: (float or null)
        """

        try:
            response = self.client.models.generate_content(
                model="gemini-3.7-flash",
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json"),
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"[Gemini API Fallback]: {e}")
            return self._local_fallback_extraction(raw_text)


gemini_service = GeminiService()
