import os
from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from extensions import db, bcrypt, jwt


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs(app.config["REPORTS_FOLDER"], exist_ok=True)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}}, supports_credentials=True)

    from routes.auth import auth_bp
    from routes.upload import upload_bp
    from routes.review import review_bp
    from routes.report import report_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(upload_bp, url_prefix="/api/upload")
    app.register_blueprint(review_bp, url_prefix="/api/reviews")
    app.register_blueprint(report_bp, url_prefix="/api/reports")

    @app.route("/api/health")
    def health():
        return jsonify(status="ok")

    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error="Not found"), 404

    @app.errorhandler(413)
    def too_large(e):
        return jsonify(error="File too large"), 413

    with app.app_context():
        from models.user import User  # noqa
        from models.project import Project  # noqa
        from models.review import Review, ReviewFinding  # noqa
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
