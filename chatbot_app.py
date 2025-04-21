# JWP/chatbot_app.py
import streamlit as st
import os
from src.commonconst import *

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)

# Helper to load text output
@st.cache_data
def load_model_output(theme):
    filepath = os.path.join(O1_OUTPUT_DIR, f"{theme}_Output.txt")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    return "(No model output found for this theme.)"

# Helper to load raw data summary
@st.cache_data
def summarize_excel_data(theme):
    config = THEME_CONFIGS.get(theme)
    if not config:
        return "Theme not found."
    try:
        df_all = []
        data = pd.read_excel(config['file'], sheet_name=config['sheets'])
        for sheet_name, df in data.items():
            df_all.append(f"\n--- {sheet_name} ---\n")
            sample = df.head(3).to_string(index=False)
            df_all.append(sample)
        return "\n".join(df_all)
    except Exception as e:
        return f"Error reading data: {e}"

# Build hybrid prompt
def build_combined_prompt(theme, model_summary, data_snippet, user_question):
    return f"""
You are an AI assistant answering questions based on UN INFO 2024 programming data in Africa.

Theme: {theme}

Context from model analysis:
{model_summary}

Context from raw sub-output data:
{data_snippet}

Now answer the following question clearly and concisely:
Q: {user_question}
A:"""

# Streamlit UI
st.set_page_config(page_title="UN INFO Data Chatbot", layout="wide")
st.title("JWP UN INFO Chatbot — Thematic Data Assistant")

selected_theme = st.selectbox("Select a Theme", list(THEME_CONFIGS.keys()))
user_query = st.text_area("Ask your question about this theme:", height=120)

if st.button("Submit Query") and user_query:
    with st.spinner("Processing with o1 model..."):
        model_output = load_model_output(selected_theme)
        data_snippet = summarize_excel_data(selected_theme)
        prompt = build_combined_prompt(selected_theme, model_output, data_snippet, user_query)

        try:
            response = client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            st.success("✅ Response from o1 model:")
            st.write(response.choices[0].message.content)
        except Exception as e:
            st.error(f"❌ Error during o1 processing: {e}")