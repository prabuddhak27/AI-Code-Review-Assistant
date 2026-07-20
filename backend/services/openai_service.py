"""Sends source code (plus static-analysis context) to an LLM and asks for a
structured JSON review. Provider-agnostic: swap the `_call_llm` internals for
OpenAI, Anthropic, or any chat-completions-compatible API.
"""
import json
import os

from flask import current_app

SYSTEM_PROMPT = """You are an experienced Senior Software Engineer.

Review the submitted code and provide:
1. Bugs found
2. Security issues
3. Code smells
4. Complexity analysis
5. Performance improvements
6. Best practices
7. Suggested refactoring
8. Better variable/function names
9. Code quality score out of 100
10. Summary of improvements

Return ONLY valid JSON with this exact shape, no markdown fences, no preamble:
{
  "score": <int 0-100>,
  "summary": "<2-4 sentence summary>",
  "findings": [
    {
      "severity": "critical|high|medium|low|info",
      "issue": "<short title>",
      "explanation": "<what and why>",
      "suggestion": "<concrete fix>",
      "line_number": <int or null>
    }
  ]
}
"""


def run_ai_review(code: str, static_context: dict | None = None) -> dict:
    api_key = current_app.config.get("OPENAI_API_KEY")
    if not api_key:
        return _fallback_review("No AI provider configured (set OPENAI_API_KEY).")

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        user_content = _build_user_prompt(code, static_context)

        response = client.chat.completions.create(
            model=current_app.config.get("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            response_format={"type": "json_object"},
            temperature=0.2,
        )
        raw = response.choices[0].message.content
        return json.loads(raw)
    except Exception as exc:  # noqa: BLE001 - surface any provider error as a soft failure
        return _fallback_review(f"AI review failed: {exc}")


def _build_user_prompt(code: str, static_context: dict | None) -> str:
    context_str = json.dumps(static_context, default=str) if static_context else "{}"
    return (
        f"Static analysis context (Pylint/Bandit/Radon summaries):\n{context_str}\n\n"
        f"Source code to review:\n```\n{code}\n```"
    )


def _fallback_review(reason: str) -> dict:
    return {
        "score": None,
        "summary": reason,
        "findings": [],
    }
