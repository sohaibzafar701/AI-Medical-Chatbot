import os
import xml.etree.ElementTree as ET
import pandas as pd
import json

def process_directory(directory):
    data_list = []
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)
        if os.path.isdir(item_path):
            print(f"Recursing into subdirectory: {item}")
            data_list.extend(process_directory(item_path))
        elif item.endswith(".xml"):
            print(f"Processing XML file: {item_path}")
            try:
                tree = ET.parse(item_path)
                root = tree.getroot()
                doc_id = root.attrib.get("id", "Unknown")
                focus = root.find("Focus").text if root.find("Focus") is not None else "Unknown"
                print(f"Parsed document_id: {doc_id}, focus: {focus}")
                for qapair in root.findall(".//QAPair"):
                    question = qapair.find("Question").text if qapair.find("Question") is not None else ""
                    answer = qapair.find("Answer").text if qapair.find("Answer") is not None else ""
                    qtype = qapair.find("Question").attrib.get("qtype", "general") if qapair.find("Question") is not None else "general"
                    if question or answer:
                        data_list.append({
                            "document_id": doc_id,
                            "topic": focus,
                            "question": question,
                            "answer": answer,
                            "qtype": qtype,
                            "source": os.path.basename(os.path.dirname(item_path))
                        })
                        print(f"Added Q&A: {question}[:50]... -> {answer}[:50]...")
            except ET.ParseError as e:
                print(f"❌ Error parsing {item_path}: {e}")
            except Exception as e:
                print(f"❌ Unexpected error with {item_path}: {e}")
    return data_list

# Use relative path or current directory
medquad_dir = os.path.join(os.path.dirname(__file__), "MedQuAD")
output_dir = os.path.dirname(__file__)

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

print(f"Checking directory: {medquad_dir}")
if not os.path.exists(medquad_dir):
    print(f"❌ MedQuAD directory not found at: {medquad_dir}")
    exit(1)

print(f"Found MedQuAD directory, listing contents:")
for item in os.listdir(medquad_dir):
    print(f"  - {item}")

data_list = process_directory(medquad_dir)

print(f"Total items in data_list: {len(data_list)}")

# Save as CSV
csv_path = os.path.join(output_dir, "chromadb/medquad_dataset.csv")
df = pd.DataFrame(data_list)
print(f"DataFrame shape: {df.shape}")
df.to_csv(csv_path, index=False, encoding="utf-8")

# Save as JSON
json_path = os.path.join(output_dir, "chromadb/medquad_dataset.json")
with open(json_path, "w", encoding="utf-8") as json_file:
    json.dump(data_list, json_file, indent=4, ensure_ascii=False)

print(f"Dataset saved at:\nCSV: {csv_path}\nJSON: {json_path}")