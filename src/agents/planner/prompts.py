# src/agents/planner/prompts.py
"""Prompt templates with few-shot examples for FOA parsing."""

PROMPT_VERSION = "1.0.0"

METADATA_PROMPT = """You are an expert NIH grant analyst. Extract key FOA (Funding Opportunity Announcement) metadata from the text below.
Return ONLY valid JSON matching this exact schema:

{
  "foa_id": "string (e.g. PA-20-185 or RFA-CA-24-001)",
  "title": "string (Full FOA title)",
  "agency": "string (e.g. NIH, NCI, NIAID)",
  "activity_code": "string (e.g. R01, R21, R03)",
  "release_date": "string (YYYY-MM-DD or empty string)",
  "application_due_date": "string (YYYY-MM-DD or standard due dates)",
  "expiration_date": "string or null",
  "description": "string (brief summary of objectives)",
  "special_instructions": ["string"],
  "contact_pi_eligible": true,
  "multiple_pi_allowed": true
}

### Example:
Input:
Department of Health and Human Services
Part 1. Overview Information
Participating Organization: National Institutes of Health (NIH)
Funding Opportunity Title: Research Project Grant (Parent R01 Clinical Trial Not Allowed)
Activity Code: R01 Research Project Grant
Announcement Type: Reissue of PA-19-051
Funding Opportunity Announcement (FOA) Number: PA-20-185
Key Dates:
Posted Date: May 8, 2020
Open Date (Earliest Submission Date): September 5, 2020
Application Due Date(s): Standard dates apply (February 5, June 5, October 5)
Expiration Date: May 8, 2023

Output:
{
  "foa_id": "PA-20-185",
  "title": "Research Project Grant (Parent R01 Clinical Trial Not Allowed)",
  "agency": "NIH",
  "activity_code": "R01",
  "release_date": "2020-05-08",
  "application_due_date": "2020-09-05",
  "expiration_date": "2023-05-08",
  "description": "The NIH Research Project Grant supports a discrete, specified, circumscribed project to be performed by the named investigator(s).",
  "special_instructions": ["Clinical Trial Not Allowed"],
  "contact_pi_eligible": true,
  "multiple_pi_allowed": true
}

### Text to extract from:
{foa_text}
"""

PARSER_PROMPT = """You are an expert NIH grant analyst. Parse the Funding Opportunity Announcement text to extract structured application requirements, page limits, required attachments, format rules, and budget rules.
Return ONLY valid JSON matching this schema:

{
  "page_limits": {
    "specific_aims": 1,
    "research_strategy": 12,
    "biosketch": 5,
    "biosketch_supplement": 2,
    "budget_justification": "no_limit",
    "facilities_resources": "no_limit",
    "equipment": "no_limit",
    "data_management_sharing": 2,
    "authentication_key_biological_resources": 1,
    "human_subjects_protection": "no_limit",
    "vertebrate_animals": "no_limit",
    "select_agent_research": 1,
    "multiple_pi_leadership_plan": 3,
    "consortium_contractual": "no_limit",
    "letters_of_support": "no_limit",
    "resource_sharing_plan": 1
  },
  "required_attachments": [
    {
      "name": "specific_aims",
      "required": true,
      "page_limit": 1,
      "description": "Specific Aims (1 page)"
    },
    {
      "name": "research_strategy",
      "required": true,
      "page_limit": 12,
      "description": "Research Strategy (Significance, Innovation, Approach)"
    },
    {
      "name": "biosketch",
      "required": true,
      "page_limit": 5,
      "description": "Biographical Sketch"
    },
    {
      "name": "budget_justification",
      "required": true,
      "page_limit": "no_limit",
      "description": "Budget Justification"
    },
    {
      "name": "data_management_sharing",
      "required": true,
      "page_limit": 2,
      "description": "Data Management and Sharing Plan"
    }
  ],
  "format_rules": {
    "font_family": "Arial",
    "font_size_pt": 11,
    "margins_inches": 0.5,
    "line_spacing": "single",
    "page_numbering": "bottom-right",
    "headers": true,
    "paper_size": "letter"
  },
  "special_instructions": ["string"],
  "budget_rules": {
    "modular_budget_enabled": true,
    "modular_budget_increment": 25000,
    "modular_budget_max_direct_costs": 250000,
    "pi_minimum_effort_pct": 30,
    "foreign_travel_requires_approval": true
  }
}

### FOA Text:
{foa_text}
"""
