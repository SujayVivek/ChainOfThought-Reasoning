
import os
import json
from tqdm import tqdm
from llm_client import call_llm
from prompts import SIMPLE_PROMPT, COT_PROMPT_SUMMARY
from utils import extract_json  


DATA_PATH = "synthetic_cases.json"       
RESULTS_DIR = "results"
OUTPUT_PATH = os.path.join(RESULTS_DIR, "outputs_baseline.json")

os.makedirs(RESULTS_DIR, exist_ok=True)

#load dataset
print(f" Loading dataset from {DATA_PATH}...")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    cases = json.load(f)

print(f" Loaded {len(cases)} clinical cases for inference.\n")

results = []

#Run LLM
for i, case in enumerate(tqdm(cases, desc="🧠 Running LLM Baseline Inference")):
    case_json = json.dumps(case, indent=2)

    #simple prompt
    simple_prompt = SIMPLE_PROMPT.format(case_json=case_json)
    try:
        simple_response = call_llm(simple_prompt)
        simple_output = simple_response["output_text"].strip().lower()
    except Exception as e:
        simple_output = f"error: {str(e)}"

    # CoT Prompt
    cot_prompt = COT_PROMPT_SUMMARY.format(case_json=case_json)
    try:
        cot_response = call_llm(cot_prompt)
        cot_output = extract_json(cot_response)
    except Exception as e:
        cot_output = {"error": str(e), "raw_output": str(cot_response)}

    
    results.append({
        "case_id": case.get("id", f"case_{i}"),
        "input": case,
        "simple_prediction": simple_output,
        "cot_prediction": cot_output
    })

#save
print("\n Saving results...")
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"✅ Done! All outputs saved to: {OUTPUT_PATH}")
