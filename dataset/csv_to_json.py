import pandas as pd
import json

# Define file paths
csv_file = r"C:\Users\sohaib\Downloads\medical-chatbot-main\medical-chatbot-main\dataset\chromadb\medquad_cleaned.csv"
json_file = r"C:\Users\sohaib\Downloads\medical-chatbot-main\medical-chatbot-main\dataset\chromadb\medquad_cleaned.json"

# Load the CSV file
df = pd.read_csv(csv_file)

# Convert to JSON
data = df.to_dict(orient="records")

# Save JSON file
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print(f"✅ JSON file saved at: {json_file}")