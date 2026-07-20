from datetime import datetime, timezone
from extensions import db


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    review_score = db.Column(db.Integer, nullable=True)  # 0-100 overall quality score
    summary = db.Column(db.Text, nullable=True)

    # Static analysis metrics (Radon / Pylint)
    maintainability_index = db.Column(db.Float, nullable=True)
    cyclomatic_complexity = db.Column(db.Float, nullable=True)
    lines_of_code = db.Column(db.Integer, nullable=True)
    num_functions = db.Column(db.Integer, nullable=True)
    num_classes = db.Column(db.Integer, nullable=True)

    raw_pylint = db.Column(db.JSON, nullable=True)
    raw_bandit = db.Column(db.JSON, nullable=True)
    raw_radon = db.Column(db.JSON, nullable=True)
    raw_ai_review = db.Column(db.JSON, nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    findings = db.relationship("ReviewFinding", backref="review", cascade="all, delete-orphan")

    def to_dict(self, include_findings=False):
        data = {
            "id": self.id,
            "project_id": self.project_id,
            "review_score": self.review_score,
            "summary": self.summary,
            "maintainability_index": self.maintainability_index,
            "cyclomatic_complexity": self.cyclomatic_complexity,
            "lines_of_code": self.lines_of_code,
            "num_functions": self.num_functions,
            "num_classes": self.num_classes,
            "created_at": self.created_at.isoformat(),
        }
        if include_findings:
            data["findings"] = [f.to_dict() for f in self.findings]
        return data


class ReviewFinding(db.Model):
    __tablename__ = "review_findings"

    id = db.Column(db.Integer, primary_key=True)
    review_id = db.Column(db.Integer, db.ForeignKey("reviews.id"), nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # critical | high | medium | low | info
    source = db.Column(db.String(20), nullable=False, default="ai")  # pylint | bandit | radon | ai
    issue = db.Column(db.String(255), nullable=False)
    explanation = db.Column(db.Text, nullable=True)
    suggestion = db.Column(db.Text, nullable=True)
    file_name = db.Column(db.String(255), nullable=True)
    line_number = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "severity": self.severity,
            "source": self.source,
            "issue": self.issue,
            "explanation": self.explanation,
            "suggestion": self.suggestion,
            "file_name": self.file_name,
            "line_number": self.line_number,
        }
