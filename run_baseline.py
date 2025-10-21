import os
import json
from tqdm import tqdm
from llm_client import call_llm
from prompts import SIMPLE_PROMPT, COT_PROMPT_SUMMARY
from utils import extract_json  
os.makedirs("results", exist_ok=True)

DATA_PATH = "synthetic_cases.json"
OUTPUT_PATH = "results/outputs_baseline.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    cases = json.load(f)

print(f"✅ Loaded {len(cases)} synthetic clinical cases.")

results = []

for i, case in enumerate(tqdm(cases, desc="Running LLM on cases")):
    # Convert case to JSON string for prompt
    case_json = json.dumps(case, indent=2)

    #Simple Prompt
    simple_prompt = SIMPLE_PROMPT.format(case_json=case_json)
    try:
        simple_response = call_llm(simple_prompt)
        simple_output = simple_response["output_text"].strip().lower()
    except Exception as e:
        simple_output = f"error: {str(e)}"

    #CoT Prompt
    cot_prompt = COT_PROMPT_SUMMARY.format(case_json=case_json)
    try:
        cot_response = call_llm(cot_prompt)
        cot_output = extract_json(cot_response)
    except Exception as e:
        cot_output = {"error": str(e), "raw_output": str(cot_response)}

    #result
    results.append({
        "case_id": case.get("id", i),
        "input": case,
        "simple_prediction": simple_output,
        "cot_prediction": cot_output
    })

#save
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n✅ Inference complete! Saved results to: {OUTPUT_PATH}")
