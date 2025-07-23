import sys
import os
from dotenv import load_dotenv
from brsr_generator.workflows.brsr_workflow import BRSRWorkflow

# Load environment variables from .env
load_dotenv()

# Example file paths (replace with your actual files)
PREVIOUS_REPORT_PATH = '../uploads/previous_brsr_report.docx'
DATA_FILE_PATH = '../uploads/this_year_data.xlsx'
TEMPLATE_PATH = '../templates/brsr_template.docx'
OUTPUT_PATH = '../uploads/generated_brsr_report.docx'

# Optionally, get Gemini API key from environment
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Orchestrate using the crewAI-powered workflow class
workflow = BRSRWorkflow(GEMINI_API_KEY)

if __name__ == '__main__':
    print('--- BRSR Report Generation Sample Run (crewAI) ---')
    try:
        result = workflow.run(
            previous_report_path=PREVIOUS_REPORT_PATH,
            data_file_path=DATA_FILE_PATH,
            template_path=TEMPLATE_PATH,
            output_path=OUTPUT_PATH
        )
        print(result)
    except Exception as e:
        print('Error during workflow:', e) 