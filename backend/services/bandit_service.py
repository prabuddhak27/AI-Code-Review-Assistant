"""Runs Bandit (security static analysis) against a Python file."""
import json
import subprocess


def run_bandit(file_path: str) -> dict:
    try:
        result = subprocess.run(
            ["bandit", "-f", "json", file_path],
            capture_output=True,
            text=True,
            timeout=60,
        )
        # Bandit exits non-zero when it finds issues, so don't check returncode.
        report = json.loads(result.stdout or "{}")
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as exc:
        return {"error": str(exc), "results": []}

    results = report.get("results", [])
    findings = [
        {
            "severity": r.get("issue_severity", "low").lower(),
            "source": "bandit",
            "issue": r.get("test_id"),
            "explanation": r.get("issue_text"),
            "suggestion": "Review this pattern against OWASP guidance for the flagged vulnerability class.",
            "file_name": r.get("filename"),
            "line_number": r.get("line_number"),
        }
        for r in results
    ]
    return {"results": results, "findings": findings, "metrics": report.get("metrics", {})}
