from crewai import Agent, Task
import os
import requests
import json

class ContentAgent:
    """
    crewAI-powered agent for generating new report content using reusable sections and new data, powered by Gemini LLM.
    """
    def __init__(self, gemini_api_key: str = None):
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.agent = Agent(
            role="BRSR Content Generator",
            goal="Generate updated BRSR report content using reusable sections and new data."
        )

    def generate_content_tool(self, reusable_sections: dict, new_data: dict) -> dict:
        prompt = (
            "You are an expert in generating BRSR (Business Responsibility and Sustainability Report) content. "
            "Given the following reusable sections from last year's report and the new data for this year, "
            "generate the updated report content. Use the reusable sections as-is where possible, and update only the dynamic sections with the new data. "
            "Return your answer as a JSON object with section titles as keys and their content as values.\n\n"
            f"Reusable Sections (JSON):\n{json.dumps(reusable_sections)[:2000]}\n\n"
            f"New Data (JSON):\n{json.dumps(new_data)[:2000]}\n\n"
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
                return json.loads(result)
            except Exception as e:
                print("Error parsing Gemini response:", e)
                return {}
        else:
            print("Gemini API error:", response.status_code, response.text)
            return {}

    def get_task(self, reusable_sections: dict, new_data: dict) -> Task:
        """
        Returns a crewAI Task for generating report content.
        """
        return Task(
            description="Generate updated BRSR report content using reusable sections and new data.",
            agent=self.agent,
            expected_output="A dictionary with section titles as keys and their content as values.",
            func=lambda: self.generate_content_tool(reusable_sections, new_data)
        ) 