from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.project import Project
from models.review import Review

review_bp = Blueprint("review", __name__)


@review_bp.route("", methods=["GET"])
@jwt_required()
def list_reviews():
    user_id = int(get_jwt_identity())
    search = request.args.get("search", "").strip().lower()
    min_score = request.args.get("min_score", type=int)

    query = (
        db.session.query(Review)
        .join(Project, Review.project_id == Project.id)
        .filter(Project.user_id == user_id)
    )
    if search:
        query = query.filter(Project.project_name.ilike(f"%{search}%"))
    if min_score is not None:
        query = query.filter(Review.review_score >= min_score)

    reviews = query.order_by(Review.created_at.desc()).all()
    return jsonify(reviews=[r.to_dict() for r in reviews])


@review_bp.route("/<int:review_id>", methods=["GET"])
@jwt_required()
def get_review(review_id):
    user_id = int(get_jwt_identity())
    review = (
        db.session.query(Review)
        .join(Project, Review.project_id == Project.id)
        .filter(Review.id == review_id, Project.user_id == user_id)
        .first_or_404()
    )
    return jsonify(review=review.to_dict(include_findings=True))


@review_bp.route("/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(review_id):
    user_id = int(get_jwt_identity())
    review = (
        db.session.query(Review)
        .join(Project, Review.project_id == Project.id)
        .filter(Review.id == review_id, Project.user_id == user_id)
        .first_or_404()
    )
    db.session.delete(review)
    db.session.commit()
    return jsonify(message="Review deleted")
