"""
Structured prompting layer: converts natural language music descriptions into
UserProfile dicts using Llama (via Groq's free API).
"""

import json
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

_SYSTEM_PROMPT = """You are a music preference parser. Convert a natural language music description into a structured taste profile.

Available genres (choose the single closest match):
pop, lofi, rock, ambient, jazz, synthwave, indie pop, r&b, hip-hop, classical, folk, metal, reggae, blues, edm, soul, country

Common moods (choose one word):
happy, peaceful, euphoric, focused, chill, melancholic, nostalgic, uplifting, angry, romantic, energetic, dreamy

Guidelines:
- genre: pick the single closest genre from the list above
- mood: pick the single mood word that best fits the description
- energy: float 0.0-1.0 (0.0 = very calm/quiet, 1.0 = very intense/loud)
- likes_acoustic: true if the user mentions acoustic, organic, unplugged, or natural instruments; false for electronic, produced, or if no preference is clear

Respond ONLY with a valid JSON object with exactly these four fields: genre, mood, energy, likes_acoustic"""

def parse_natural_language_to_profile(description: str) -> dict:
    """
    Send a plain-English music description to Llama via Groq and return a
    UserProfile-compatible dict with keys: genre, mood, energy, likes_acoustic.

    Raises groq.APIError on API failures.
    Raises ValueError if the response cannot be parsed as JSON.
    """
    response = _client.chat.completions.create(
        model="llama-3.1-8b-instant",
        max_tokens=256,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": description},
        ],
    )

    raw = response.choices[0].message.content
    try:
        profile = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Model returned invalid JSON: {raw!r}") from exc

    # Clamp energy to [0.0, 1.0] in case the model drifts slightly
    profile["energy"] = max(0.0, min(1.0, float(profile["energy"])))

    return profile
