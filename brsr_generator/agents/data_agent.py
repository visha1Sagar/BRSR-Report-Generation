import os
import requests
import json
from crewai import Agent, Task
from tools.document_tools import load_document

class DataAgent:
    """
    crewAI-powered agent for extracting and cleaning new data for the BRSR report using Gemini LLM.
    """
    def __init__(self, gemini_api_key: str = None):
        self.gemini_api_key = gemini_api_key or os.getenv("GEMINI_API_KEY")
        self.agent = Agent(
            role="BRSR Data Extractor",
            goal="Extract and clean new data for BRSR report generation."
        )

    def extract_data_tool(self, data_file_path: str) -> dict:
        data_text = load_document(data_file_path)
        if not data_text:
            raise ValueError("Failed to load or extract text from the data file.")
        prompt = (
            "You are an expert in extracting and cleaning data for BRSR (Business Responsibility and Sustainability Report) generation. "
            "Given the following raw data, extract all relevant structured information as a JSON object. "
            "Clean the data, correct any obvious errors, and organize it by section or topic if possible.\n\n"
            f"Raw Data:\n{data_text[:4000]}\n\n"
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

    def get_task(self, data_file_path: str) -> Task:
        """
        Returns a crewAI Task for extracting and cleaning new data.
        """
        return Task(
            description="Extract and clean new data for the BRSR report.",
            agent=self.agent,
            expected_output="A dictionary of cleaned and structured data.",
            func=lambda: self.extract_data_tool(data_file_path)
        ) 