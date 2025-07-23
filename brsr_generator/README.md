# BRSR Multi-Agent Report Generator

This project automates the generation of BRSR (Business Responsibility and Sustainability Report) documents using a multi-agent system. Given a previous year's BRSR report and this year's data, it generates a new report with the same template, updating only the necessary sections.

## Folder Structure

```
brsr-generator/
├── agents/         # Autonomous agents for analysis, data extraction, content generation, QA, and assembly
├── tools/          # Utility modules for document, Excel, content, and validation operations
├── workflows/      # Orchestration logic for agent collaboration
├── api/            # (Future) API endpoints for user interaction
├── templates/      # Report templates (Word, PDF, etc.)
├── uploads/        # User-uploaded files (previous reports, data)
├── config/         # Configuration files
├── tests/          # Unit and integration tests
```

## Main Components
- **agents/**: Specialized agents for each stage of report generation
- **tools/**: Helper functions for file handling, content processing, and validation
- **workflows/**: Defines the workflow and agent collaboration
- **api/**: (Planned) FastAPI endpoints for file upload, report generation, and download
- **templates/**: Store reusable report templates
- **uploads/**: Store user-uploaded files
- **config/**: Configuration and settings
- **tests/**: Automated tests

## Supported File Formats
- Word (.docx)
- PDF (.pdf)
- Excel (.xlsx, .xls)
- CSV (.csv)
- Plain text (.txt)

---

## Getting Started
1. Place previous BRSR report and new data files in `uploads/`.
2. Run the workflow to generate a new report in the same template.
3. (API coming soon) 

A `requirements.txt` file has been created with the essential packages for your multi-agent BRSR generator:

- `requests` (for Gemini API calls)
- `python-dotenv` (for loading environment variables from `.env`)
- `python-docx` (for Word document assembly)
- `PyPDF2` (for PDF text extraction)
- `openpyxl` (for Excel file handling)

---

**Next Steps:**
- You can install all dependencies with:
  ```
  pip install -r requirements.txt
  ```
- Would you like a sample workflow script, or should we implement the document extraction logic in `tools/document_tools.py` next? 