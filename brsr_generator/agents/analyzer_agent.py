import os
import requests
import json
from crewai import Agent, Task
from tools.document_tools import load_document

class AnalyzerAgent:
    """
    crewAI-powered agent for analyzing previous BRSR reports to extract reusable and dynamic sections using Gemini LLM.
    """
    def __init__(self, gemini_api_key: str = None):
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.agent = Agent(
            role="BRSR Report Analyzer",
            goal="Analyze previous BRSR reports and extract reusable/static and dynamic sections for report generation."
        )

    def analyze_report_tool(self, previous_report_path: str) -> dict:
        document_text = load_document(previous_report_path)
        if not document_text:
            raise ValueError("Failed to load or extract text from the previous report.")
        prompt = (
            "You are an expert in analyzing BRSR (Business Responsibility and Sustainability Report) documents. "
            "Given the following report, extract its sections and classify each as either 'static' (reusable every year) "
            "or 'dynamic' (needs updating with new data). Return your answer as a JSON object with two keys: "
            "'static_sections' and 'dynamic_sections', each containing a list of section titles and their content.\n\n"
            f"Report Content:\n{document_text[:4000]}\n\n"
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

    def get_task(self, previous_report_path: str) -> Task:
        """
        Returns a crewAI Task for analyzing the previous report.
        """
        return Task(
            description="Analyze the previous BRSR report and extract reusable/static and dynamic sections.",
            agent=self.agent,
            expected_output="A dictionary with 'static_sections' and 'dynamic_sections' as keys.",
            func=lambda: self.analyze_report_tool(previous_report_path)
        ) 