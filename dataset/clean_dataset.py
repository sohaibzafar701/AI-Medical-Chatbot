import pandas as pd
import re
import os

# Update file paths to match your environment
input_file = r"C:\Users\sohaib\Downloads\medical-chatbot-main\medical-chatbot-main\dataset\chromadb\medquad_dataset.csv"
output_file = r"C:\Users\sohaib\Downloads\medical-chatbot-main\medical-chatbot-main\dataset\chromadb\medquad_cleaned.csv"

# Ensure the file exists before loading
if not os.path.exists(input_file):
    raise FileNotFoundError(f"❌ File not found: {input_file}")

# Load CSV
df = pd.read_csv(input_file)

# Check column names
print("Columns in dataset:", df.columns)

# Ensure required columns exist
required_columns = ["question", "answer"]
for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"❌ Missing required column: {col}")

# Drop duplicates
df = df.drop_duplicates(subset=["question", "answer"])

# Handle missing values
df = df.dropna(subset=["question", "answer"])  # Drop rows with missing Q&A

# Text normalization function
def clean_text(text):
    if pd.isna(text):
        return ""
    text = text.lower().strip()  # Convert to lowercase & trim spaces
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    text = re.sub(r"[^\w\s]", "", text)  # Remove special characters
    return text

# Apply text cleaning
df["question"] = df["question"].apply(clean_text)
df["answer"] = df["answer"].apply(clean_text)

# Save cleaned dataset
os.makedirs(os.path.dirname(output_file), exist_ok=True)
df.to_csv(output_file, index=False)

print(f"✅ Cleaned dataset saved at: {output_file}")