# prompts.py
SIMPLE_PROMPT = """You are a medical assistant. Your task is to look at patient information and decide:
- reply with exactly one word, either: ckd or control.
- no punctuation, no extra text, no JSON, only the one-word label.

Patient case (JSON):
{case_json}
"""

COT_PROMPT_SUMMARY = """You are a medical clinician assistant. For the case below, produce a JSON-only response (no extra text).
**Important**: Do NOT produce your internal chain-of-thought. Instead produce a concise, structured summary explanation (safe, high-level reasoning).
Return ONLY valid JSON and nothing else, with exactly these keys:
- diagnosis: "ckd" or "control"
- reasoning: list of concise numbered summary steps (each step: finding -> interpretation -> how it supports or refutes CKD)
- evidence_map: dict mapping evidence_label -> short interpretation (lab or vital)
- confidence: number between 0 and 1 (float), representing your confidence.

Guidelines:
1. For each lab, compare vs a normal cutoff and mark 'high', 'low', or 'normal' in the evidence_map.
2. Include both supporting and refuting findings.
3. Each reasoning step MUST cite *one* evidence label that appears in evidence_map (e.g., "creatinine", "eGFR").
4. Keep reasoning steps concise (1–2 sentences each).

Patient case (JSON):
{case_json}
"""
