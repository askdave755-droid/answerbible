# research.py — AI-assisted research drafting
# Drafts the 6 research fields + theme suggestions via OpenAI.
# David still reviews everything: this only PRE-FILLS, the 12-blocker gate is untouched.
import json
import requests
from config import settings

MODEL = "gpt-4o-mini"

VALID_CATEGORIES = [
    "general", "genesis_6", "sheol", "spiritual_warfare", "demons",
    "election", "end_times", "divorce", "women_ministry", "salvation",
    "character_of_god", "prophecy_dating",
]

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

Fill exactly these 9 fields:
1. hook — gripping opening that raises the question honestly (2-5 sentences, plain text)
2. problem — why this confuses people / what's at stake (2-5 sentences)
3. explanation — what the text actually says, with context and original-language notes where relevant; mention the main alternative interpretation where one exists (2-5 sentences)
4. story — a relatable real-life illustration (2-5 sentences)
5. application — what the viewer should do with this (2-5 sentences)
6. cta — call to action inviting comments with the viewer's questions (1-2 sentences)
7. suggested_title — a compelling but honest video title/theme (10 words max, no clickbait)
8. suggested_scripture — the single best primary passage to anchor this video (e.g., "Genesis 6:1-4")
9. suggested_category — EXACTLY one of: general, genesis_6, sheol, spiritual_warfare, demons, election, end_times, divorce, women_ministry, salvation, character_of_god, prophecy_dating

Return ONLY a JSON object with keys: hook, problem, explanation, story, application, cta, suggested_title, suggested_scripture, suggested_category"""


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
    keys = ("hook", "problem", "explanation", "story", "application", "cta",
            "suggested_title", "suggested_scripture", "suggested_category")
    out = {k: str(data.get(k, "")).strip() for k in keys}
    if out["suggested_category"] not in VALID_CATEGORIES:
        out["suggested_category"] = "general"
    return out
