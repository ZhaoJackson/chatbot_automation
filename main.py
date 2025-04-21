# JWP/chatbot_app.py
from src.commonconst import *
from src.data_processing import extract_sub_outputs, build_prompt

# Initialize Azure client
client = AzureOpenAI(
    api_key=AZURE_OPENAI_API_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
)

# Output directory
os.makedirs(O1_OUTPUT_DIR, exist_ok=True)

def analyze_theme(theme, config):
    print(f"\n🔍 Processing theme: {theme}")
    try:
        sub_outputs = extract_sub_outputs(config['file'], config['sheets'])
    except Exception as e:
        print(f"❌ Error reading data for {theme}: {e}")
        return

    if not sub_outputs:
        print(f"⚠️ Skipping {theme} – no valid sub-output entries found.")
        return

    prompt = build_prompt(theme, sub_outputs)

    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        result = response.choices[0].message.content

        if result:
            output_path = os.path.join(O1_OUTPUT_DIR, f"{theme}_Output.txt")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result)
            print(f"✅ Output saved: {output_path}")
        else:
            print(f"⚠️ o1 model returned empty content for {theme}")

    except Exception as e:
        print(f"❌ Error during Azure o1 call for {theme}: {e}")

if __name__ == "__main__":
    for theme, config in THEME_CONFIGS.items():
        analyze_theme(theme, config)