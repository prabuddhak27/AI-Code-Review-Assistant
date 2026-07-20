"""Runs Radon to compute cyclomatic complexity and maintainability index."""
import json
import subprocess


def run_radon(file_path: str) -> dict:
    complexity = _run_json(["radon", "cc", "-j", file_path])
    maintainability = _run_json(["radon", "mi", "-j", file_path])
    raw_metrics = _run_json(["radon", "raw", "-j", file_path])

    file_complexity = complexity.get(file_path, []) if isinstance(complexity, dict) else []
    if not isinstance(file_complexity, list):
        # Radon returns {"error": "..."} instead of a block list when it can't parse the file
        # (e.g. incomplete/invalid Python syntax in a pasted snippet).
        file_complexity = []

    mi_score = None
    mi_entry = maintainability.get(file_path) if isinstance(maintainability, dict) else None
    if isinstance(mi_entry, dict):
        mi_score = mi_entry.get("mi")

    raw_entry = raw_metrics.get(file_path) if isinstance(raw_metrics, dict) else None
    raw = raw_entry if isinstance(raw_entry, dict) else {}

    file_complexity = [b for b in file_complexity if isinstance(b, dict)]

    num_functions = sum(1 for block in file_complexity if block.get("type") == "function")
    num_classes = sum(1 for block in file_complexity if block.get("type") == "class")
    avg_complexity = (
        sum(b.get("complexity", 0) for b in file_complexity) / len(file_complexity)
        if file_complexity
        else 0
    )

    return {
        "complexity_blocks": file_complexity,
        "maintainability_index": mi_score,
        "avg_complexity": round(avg_complexity, 2),
        "lines_of_code": raw.get("loc"),
        "num_functions": num_functions,
        "num_classes": num_classes,
    }


def _run_json(cmd: list) -> dict:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return json.loads(result.stdout or "{}")
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError):
        return {}