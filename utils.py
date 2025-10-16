import json
import re


def extract_json(text):
    if isinstance(text, dict) and "output_text" in text:
        text = text["output_text"]

    if not isinstance(text, str):
        text = str(text)

    text = text.replace("``````", "").strip()

    matches = re.findall(r"\{[\s\S]*\}", text)
    if not matches:
        raise ValueError(f"No JSON object found in text:\n{text[:200]}...")

    json_str = max(matches, key=len).strip()

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        cleaned = re.search(r"\{[\s\S]*\}", text)
        if cleaned:
            json_str = cleaned.group(0)
        json_str = json_str.replace("'", '"')
        try:
            return json.loads(json_str)
        except Exception as e:
            raise ValueError(
                f"Invalid JSON format: {e}\n\nExtracted JSON string (truncated):\n{json_str[:300]}"
            )


def validate_simple_label(text: str):
    txt = text.strip().lower()
    if txt in ("ckd", "control"):
        return txt

    m = re.search(r'\b(ckd|control)\b', txt)
    if m:
        return m.group(1)
    raise ValueError("Could not parse simple label from model output.")


if __name__ == "__main__":
    sample = {
        'output_text': '``````'
    }
    print(extract_json(sample))
