# src/commonconst.py
from openai import AzureOpenAI
import pandas as pd
import re
import os

# Azure OpenAI Credentials
AZURE_OPENAI_API_KEY = "4gM2HRtaDIsFbDjfQQl1DAO1RzN4l2TfAcmkIuC0KgcEjmsEOS9yJQQJ99BBACHYHv6XJ3w3AAAAACOGpcKh"
AZURE_OPENAI_ENDPOINT = "https://ppbai6350320563.openai.azure.com"
AZURE_OPENAI_API_VERSION = "2024-12-01-preview"
AZURE_OPENAI_DEPLOYMENT = "o1"

# Output directory
O1_OUTPUT_DIR = "src/o1_outputs"

# Theme file configuration
THEME_CONFIGS = {
    "Youth": {
        "file": "src/data/Youth - jeunesse - export_250416.xlsx",
        "sheets": ["Youth - Pivot Table", "Youth - SubOutputs"]
    },
    "Crime": {
        "file": "src/data/Crime - Criminalité-export_250416.xlsx",
        "sheets": ["Crime - Pivot Table", "Crime - SubOutputs"]
    },
    "Digital": {
        "file": "src/data/Digital - numérique - export_250416.xlsx",
        "sheets": ["Digital - Pivot Table", "Digital - SubOutputs"]
    },
    "Education": {
        "file": "src/data/Education-éducation-all-countries-export_250416.xlsx",
        "sheets": ["Education - Pivote Table", "Education - SubOutputs"]
    },
    "Mining": {
        "file": "src/data/Mining-Mine_export_250416.xlsx",
        "sheets": ["Mining - Pivot Table", "Mining - SubOutputs"]
    },
    "Illicit": {
        "file": "src/data/Illicit - illicite - export_250416.xlsx",
        "sheets": ["Illicit - Pivot Table", "Illicit - SubOutputs"]
    },
    "IFF": {
        "file": "src/data/IFF - export_250416.xlsx",
        "sheets": ["IFF - Pivot Table", "IFF - SubOutputs"]
    }
}

O1_PROMPT_TEMPLATE = """
You are an AI assistant analyzing UN INFO Cooperation Framework (CF JWP) data from 2024.

Theme: {theme}

Based on the following extracted sub-output entries from UN country programming in Africa, please answer:

1. What are the 4 main areas of focus for {theme} in Africa where the UN is supporting (2024)? For each area, identify the main theme (e.g., Economic Empowerment, Education Access, Health Systems) and briefly illustrate the specific focus within that theme using 1–2 sentences.
2. What are potential challenges or gaps in support?

Data:
{bullets}

Please return:
- A list of 4 main areas of focus, each with a theme label and 1–2 sentence illustration
- 2–3 sentences summarizing key challenges/gaps
"""