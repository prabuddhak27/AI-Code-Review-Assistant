"""Runs Pylint against a Python source file and returns a normalized report.

Pylint is invoked as a subprocess with JSON output so this stays decoupled
from Pylint's internal Python API (which changes across versions).
"""
import json
import subprocess


def run_pylint(file_path: str) -> dict:
    try:
        result = subprocess.run(
            ["pylint", file_path, "--output-format=json", "--exit-zero"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        messages = json.loads(result.stdout or "[]")
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as exc:
        return {"error": str(exc), "messages": []}

    findings = [
        {
            "severity": _map_severity(m.get("type")),
            "source": "pylint",
            "issue": m.get("symbol", m.get("message-id", "issue")),
            "explanation": m.get("message"),
            "suggestion": None,
            "file_name": m.get("path"),
            "line_number": m.get("line"),
        }
        for m in messages
    ]

    score = _estimate_score(messages)
    return {"score": score, "messages": messages, "findings": findings}


def _map_severity(pylint_type: str) -> str:
    return {
        "error": "high",
        "fatal": "critical",
        "warning": "medium",
        "convention": "low",
        "refactor": "low",
        "info": "info",
    }.get(pylint_type, "info")


def _estimate_score(messages: list) -> int:
    # Simple deduction model since --exit-zero doesn't print pylint's own score line reliably.
    penalty = {"error": 5, "fatal": 10, "warning": 2, "convention": 1, "refactor": 1, "info": 0}
    total = sum(penalty.get(m.get("type"), 1) for m in messages)
    return max(0, 100 - total)
