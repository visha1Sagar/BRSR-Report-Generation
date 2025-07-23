from crewai import Agent, Task
import os
import requests
import json

class QAAgent:
    """
    crewAI-powered agent for quality assurance on the generated report content using Gemini LLM.
    """
    def __init__(self, gemini_api_key: str = None):
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.agent = Agent(
            role="BRSR QA Agent",
            goal="Validate the generated BRSR report content for consistency, correctness, and completeness."
        )

    def validate_content_tool(self, report_content: dict) -> dict:
        prompt = (
            "You are an expert in BRSR (Business Responsibility and Sustainability Report) compliance and quality assurance. "
            "Given the following generated report content, check for consistency, correctness, and completeness. "
            "Return your answer as a JSON object with a boolean key 'valid' (true if the content passes QA, false otherwise) "
            "and an optional 'message' key with feedback or errors.\n\n"
            f"Report Content (JSON):\n{json.dumps(report_content)[:4000]}\n\n"
            "Respond ONLY with the JSON object."
        )
        headers = {"Content-Type": "application/json"}
        params = {"key": self.gemini_api_key}
        data = {"contents": [{"parts": [{"text": prompt}]}]}
        response = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent",
            headers=headers, params=params, json=data
        )
        if response.status_code == 200:
            try:
                result = response.json().get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '{}')
                qa_result = json.loads(result)
                return qa_result
            except Exception as e:
                print("Error parsing Gemini response:", e)
                return {"valid": False, "message": str(e)}
        else:
            print("Gemini API error:", response.status_code, response.text)
            return {"valid": False, "message": response.text}

    def get_task(self, report_content: dict) -> Task:
        """
        Returns a crewAI Task for validating the generated report content.
        """
        return Task(
            description="Validate the generated BRSR report content for consistency, correctness, and completeness.",
            agent=self.agent,
            expected_output="A JSON object with a boolean key 'valid' and an optional 'message' key.",
            func=lambda: self.validate_content_tool(report_content)
        ) 