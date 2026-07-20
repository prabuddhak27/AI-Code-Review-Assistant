from flask import Blueprint, jsonify, Response
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.project import Project
from models.review import Review

report_bp = Blueprint("report", __name__)


def _get_owned_review(review_id, user_id):
    return (
        db.session.query(Review)
        .join(Project, Review.project_id == Project.id)
        .filter(Review.id == review_id, Project.user_id == user_id)
        .first_or_404()
    )


@report_bp.route("/<int:review_id>/markdown", methods=["GET"])
@jwt_required()
def export_markdown(review_id):
    user_id = int(get_jwt_identity())
    review = _get_owned_review(review_id, user_id)

    lines = [
        f"# Code Review Report - Project #{review.project_id}",
        f"**Score:** {review.review_score}/100",
        f"**Maintainability Index:** {review.maintainability_index}",
        f"**Avg Cyclomatic Complexity:** {review.cyclomatic_complexity}",
        "",
        "## Summary",
        review.summary or "_No summary available_",
        "",
        "## Findings",
    ]
    for f in review.findings:
        lines.append(f"- **[{f.severity.upper()}] {f.issue}** ({f.source}, line {f.line_number})")
        if f.explanation:
            lines.append(f"  - {f.explanation}")
        if f.suggestion:
            lines.append(f"  - _Suggestion:_ {f.suggestion}")

    markdown = "\n".join(lines)
    return Response(
        markdown,
        mimetype="text/markdown",
        headers={"Content-Disposition": f"attachment; filename=review_{review_id}.md"},
    )

# PDF export via ReportLab can be added the same way: build a canvas/story from
# review.to_dict(include_findings=True) and return it as an application/pdf Response.
