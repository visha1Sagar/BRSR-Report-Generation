from crewai import Crew
from agents.analyzer_agent import AnalyzerAgent
from agents.data_agent import DataAgent
from agents.content_agent import ContentAgent
from agents.qa_agent import QAAgent
from agents.assembly_agent import AssemblyAgent

class BRSRWorkflow:
    """
    Orchestrates the multi-agent workflow for BRSR report generation using crewAI Crew.
    """
    def __init__(self, gemini_api_key=None):
        self.analyzer = AnalyzerAgent(gemini_api_key)
        self.data_agent = DataAgent(gemini_api_key)
        self.content_agent = ContentAgent(gemini_api_key)
        self.qa_agent = QAAgent(gemini_api_key)
        self.assembly_agent = AssemblyAgent(gemini_api_key)

    def run(self, previous_report_path: str, data_file_path: str, template_path: str, output_path: str):
        # Step 1: Analyze previous report
        analyzer_task = self.analyzer.get_task(previous_report_path)
        reusable_sections = analyzer_task.run()

        # Step 2: Extract and clean new data
        data_task = self.data_agent.get_task(data_file_path)
        new_data = data_task.run()

        # Step 3: Generate new content
        content_task = self.content_agent.get_task(reusable_sections, new_data)
        report_content = content_task.run()

        # Step 4: Validate content
        qa_task = self.qa_agent.get_task(report_content)
        qa_result = qa_task.run()
        if not (isinstance(qa_result, dict) and qa_result.get('valid', False)):
            raise ValueError(f"Report content validation failed: {qa_result.get('message', 'Unknown error')}")

        # Step 5: Assemble final report
        assembly_task = self.assembly_agent.get_task(report_content, template_path, output_path)
        result = assembly_task.run()
        return result 