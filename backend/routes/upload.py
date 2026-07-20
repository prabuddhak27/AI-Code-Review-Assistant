import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.project import Project
from models.review import Review, ReviewFinding
from utils.file_utils import allowed_file, save_upload
from services.pylint_service import run_pylint
from services.bandit_service import run_bandit
from services.radon_service import run_radon
from services.openai_service import run_ai_review

upload_bp = Blueprint("upload", __name__)


@upload_bp.route("/file", methods=["POST"])
@jwt_required()
def upload_file():
    user_id = int(get_jwt_identity())

    if "file" not in request.files:
        return jsonify(error="No file part named 'file' in request"), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify(error="No file selected"), 400
    if not allowed_file(file.filename):
        return jsonify(error="Unsupported file type"), 400

    saved_path = save_upload(file)
    project = Project(user_id=user_id, project_name=file.filename, upload_type="file")
    db.session.add(project)
    db.session.commit()

    review = _analyze_and_store(project.id, saved_path)
    return jsonify(project=project.to_dict(), review=review.to_dict(include_findings=True)), 201


@upload_bp.route("/snippet", methods=["POST"])
@jwt_required()
def upload_snippet():
    user_id = int(get_jwt_identity())
    data = request.get_json(silent=True) or {}
    code = data.get("code", "")
    project_name = data.get("project_name") or "Untitled snippet"

    if not code.strip():
        return jsonify(error="Code snippet is empty"), 400

    tmp_path = os.path.join(current_app.config["UPLOAD_FOLDER"], f"snippet_{user_id}_{Project.query.count() + 1}.py")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(code)

    project = Project(user_id=user_id, project_name=project_name, upload_type="snippet")
    db.session.add(project)
    db.session.commit()

    review = _analyze_and_store(project.id, tmp_path)
    return jsonify(project=project.to_dict(), review=review.to_dict(include_findings=True)), 201


def _analyze_and_store(project_id: int, file_path: str) -> Review:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        code = f.read()

    pylint_result = run_pylint(file_path)
    bandit_result = run_bandit(file_path)
    radon_result = run_radon(file_path)

    static_context = {
        "pylint_score": pylint_result.get("score"),
        "bandit_issue_count": len(bandit_result.get("results", [])),
        "radon": {
            "maintainability_index": radon_result.get("maintainability_index"),
            "avg_complexity": radon_result.get("avg_complexity"),
        },
    }
    ai_result = run_ai_review(code, static_context)

    scores = [s for s in [pylint_result.get("score"), ai_result.get("score")] if isinstance(s, (int, float))]
    overall_score = round(sum(scores) / len(scores)) if scores else None

    review = Review(
        project_id=project_id,
        review_score=overall_score,
        summary=ai_result.get("summary"),
        maintainability_index=radon_result.get("maintainability_index"),
        cyclomatic_complexity=radon_result.get("avg_complexity"),
        lines_of_code=radon_result.get("lines_of_code"),
        num_functions=radon_result.get("num_functions"),
        num_classes=radon_result.get("num_classes"),
        raw_pylint=pylint_result,
        raw_bandit=bandit_result,
        raw_radon=radon_result,
        raw_ai_review=ai_result,
    )
    db.session.add(review)
    db.session.flush()  # get review.id before adding findings

    all_findings = (
        pylint_result.get("findings", [])
        + bandit_result.get("findings", [])
        + [
            {
                "severity": f.get("severity", "info"),
                "source": "ai",
                "issue": f.get("issue"),
                "explanation": f.get("explanation"),
                "suggestion": f.get("suggestion"),
                "file_name": os.path.basename(file_path),
                "line_number": f.get("line_number"),
            }
            for f in ai_result.get("findings", [])
        ]
    )

    for f in all_findings:
        db.session.add(
            ReviewFinding(
                review_id=review.id,
                severity=f.get("severity", "info"),
                source=f.get("source", "ai"),
                issue=str(f.get("issue"))[:255] if f.get("issue") else "Unspecified issue",
                explanation=f.get("explanation"),
                suggestion=f.get("suggestion"),
                file_name=f.get("file_name"),
                line_number=f.get("line_number"),
            )
        )

    db.session.commit()
    return review
