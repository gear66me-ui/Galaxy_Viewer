from __future__ import annotations

import base64
import json
import urllib.error
import urllib.request

from google.colab import output as colab_output

PRE_GEMINI_BLOB_URL = "https://api.github.com/repos/gear66me-ui/Galaxy_Viewer/git/blobs/29128c207caec619e101593ef3e017706b048316"

with urllib.request.urlopen(PRE_GEMINI_BLOB_URL, timeout=60) as response:
    payload = json.loads(response.read().decode("utf-8"))
wrapper_source = base64.b64decode(payload["content"]).decode("utf-8")

wrapper_source = wrapper_source.replace(
    '"Galaxy Viewer — VIEWER-9-7", 1)',
    '"Galaxy Viewer — VIEWER-9-7 GEMINI", 1)',
    1,
)
wrapper_source = wrapper_source.replace(
    "Random Galaxy does not call the OpenAI API.",
    "Random Galaxy does not call the Gemini API.",
)
wrapper_source = wrapper_source.replace(
    "OpenAI research timed out after 75 seconds.",
    "Gemini Search timed out after 75 seconds.",
)
wrapper_source = wrapper_source.replace(
    'out.error||"OpenAI request failed."',
    'out.error||"Gemini request failed."',
)

compile(wrapper_source, "VIEWER-9-7-pre-gemini.py", "exec")
exec(compile(wrapper_source, "VIEWER-9-7-pre-gemini.py", "exec"), globals(), globals())


def _gemini_json(prompt: str, schema_name: str, schema: dict) -> dict:
    api_key = _secret("Gemini API Key") or _secret("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            'Gemini API Key is missing from Colab Secrets. '
            'Add a secret named exactly "Gemini API Key" and enable notebook access.'
        )

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json",
            "responseJsonSchema": schema,
        },
    }

    request = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "x-goog-api-key": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini API error {exc.code}: {detail[:1200]}") from exc
    except Exception as exc:
        raise RuntimeError(f"Gemini request failed: {exc}") from exc

    candidates = result.get("candidates") or []
    if not candidates:
        feedback = result.get("promptFeedback") or {}
        raise RuntimeError(
            "Gemini returned no candidate response. "
            + json.dumps(feedback)[:800]
        )

    parts = ((candidates[0].get("content") or {}).get("parts") or [])
    text = "".join(
        str(part.get("text", ""))
        for part in parts
        if part.get("text")
    )
    if not text:
        finish = candidates[0].get("finishReason", "unknown")
        raise RuntimeError(
            f"Gemini returned no JSON text. Finish reason: {finish}"
        )

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"Gemini returned invalid JSON: {text[:1000]}") from exc


# viewer9_get_info resolves this global function when the button is pressed.
# Replacing it here removes the OpenAI request path without changing the viewer.
_openai_json = _gemini_json


def viewer9_gemini_info_callback(name: str, ra: float, dec: float):
    try:
        return {"ok": True, "payload": viewer9_get_info(name, ra, dec)}
    except Exception as exc:
        return {"ok": False, "error": str(exc)}


colab_output.register_callback(
    "viewer9.getGalaxyInfo",
    viewer9_gemini_info_callback,
)

assert _openai_json is _gemini_json
assert "Gemini API Key" in _gemini_json.__code__.co_consts
