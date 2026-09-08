# research.py — AI-assisted research drafting
# Drafts the 6 research fields from topic + scripture via OpenAI.
# David still reviews everything: this only PRE-FILLS, the 12-blocker gate is untouched.
import json
import requests
from config import settings

MODEL = "gpt-4o-mini"

PROMPT_TEMPLATE = """You are a research assistant for "Answers in Faith", a YouTube channel that answers
Bible questions with theological rigor. The channel enforces 12 blockers:
- every claim needs scripture support and historical/literary context
- no "this word only means" without lexical evidence
- speculation must be labeled, never asserted as fact
- no date-setting, no Antichrist identification
- always present alternative interpretations honestly

Draft RESEARCH (not a script) for this video:

Topic: {topic}
Source question: {source_question}
Primary scripture: {primary_scripture}
Category: {category}
Gospel video: {gospel}

Fill exactly these 6 fields, each 2-5 sentences, plain text, no markdown:
1. hook — a gripping opening that raises the question honestly
2. problem — why this confuses people / what's at stake
3. explanation — what the text actually says, with context and original-language notes where relevant
4. story — a relatable real-life illustration
5. application — what the viewer should do with this
6. cta — call to action inviting comments with the viewer's questions

Be balanced: mention the main alternative interpretation in the explanation where one exists.
Return ONLY a JSON object: {{"hook": "...", "problem": "...", "explanation": "...", "story": "...", "application": "...", "cta": "..."}}"""


def auto_research(topic, source_question, primary_scripture, category, gospel_video):
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured on the server.")
    prompt = PROMPT_TEMPLATE.format(
        topic=topic or "(not specified)",
        source_question=source_question or "(not specified)",
        primary_scripture=primary_scripture or "(not specified)",
        category=category or "general",
        gospel=gospel_video,
    )
    resp = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {settings.openai_api_key}", "Content-Type": "application/json"},
        json={
            "model": MODEL,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": "You are a careful biblical research assistant. Output only valid JSON."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
        },
        timeout=90,
    )
    if resp.status_code != 200:
        raise RuntimeError(f"OpenAI error {resp.status_code}: {resp.text[:200]}")
    content = resp.json()["choices"][0]["message"]["content"]
    data = json.loads(content)
    return {k: str(data.get(k, "")).strip() for k in ("hook", "problem", "explanation", "story", "application", "cta")}
