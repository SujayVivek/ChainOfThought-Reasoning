# app.py
import json
import argparse
from llm_client import call_llm
from prompts import SIMPLE_PROMPT, COT_PROMPT_SUMMARY
from utils import extract_json, validate_simple_label

def load_case(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_simple(case_json):
    prompt = SIMPLE_PROMPT.format(case_json=json.dumps(case_json))
    resp = call_llm(prompt, max_tokens=10, temperature=0.0)
    text = extract_text_from_response(resp)
    label = validate_simple_label(text)
    return label

def run_cot(case_json):
    prompt = COT_PROMPT_SUMMARY.format(case_json=json.dumps(case_json))
    resp = call_llm(prompt, max_tokens=800, temperature=0.0)
    text = extract_text_from_response(resp)
    try:
        parsed = extract_json(text)
    except Exception as e:
        raise RuntimeError(f"Failed to parse JSON from model response: {e}\nRaw text:\n{text}")
    if parsed.get("diagnosis") not in ("ckd", "control"):
        raise RuntimeError("diagnosis must be ckd or control")
    if not isinstance(parsed.get("confidence", None), (float, int)):
        raise RuntimeError("confidence must be a number 0-1")
    return parsed

def extract_text_from_response(resp_json):
    if isinstance(resp_json, dict):
        if "choices" in resp_json and isinstance(resp_json["choices"], list):
            c = resp_json["choices"][0]
            return c.get("text") or (c.get("message") or {}).get("content") or resp_json.get("output_text","")
        if "candidates" in resp_json and resp_json["candidates"]:
            return resp_json["candidates"][0].get("content", "")
        if "output" in resp_json:
            return resp_json["output"]
    return str(resp_json)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", "-i", required=True, help="Path to case JSON")
    parser.add_argument("--mode", choices=["simple","cot"], default="simple")
    args = parser.parse_args()

    case = load_case(args.input)

    if args.mode == "simple":
        label = run_simple(case)
        print(label)
    else:
        parsed = run_cot(case)
        print(json.dumps(parsed, indent=2))

if __name__ == "__main__":
    main()
