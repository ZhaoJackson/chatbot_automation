# src/data_processing.py
from src.commonconst import *

def extract_sub_outputs(file_path, sheet_names):
    """Extract sub-output entries from the specified sheets."""
    combined = []
    xls = pd.read_excel(file_path, sheet_name=sheet_names)

    for sheet in sheet_names:
        df = xls[sheet]
        sub_col = next((c for c in df.columns if "sub-output" in c.lower()), None)
        if sub_col:
            entries = df[sub_col].dropna().astype(str)
            entries = entries[entries.str.len() > 10]
            combined.extend(entries.tolist())
    return combined

def build_prompt(theme, sub_outputs):
    bullets = "\n".join(f"- {item}" for item in sub_outputs[:50])
    return O1_PROMPT_TEMPLATE.format(theme=theme, bullets=bullets)