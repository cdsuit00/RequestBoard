from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
from backend.models import db, User, Request, Response

api = Blueprint("api", __name__, url_prefix="/api")

# -------------------
# Auth Routes
# -------------------
@api.route("/auth/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(
        username=data["username"],
        email=data["email"],
        password_hash=generate_password_hash(data["password"])
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


@api.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()

    if not user or not check_password_hash(user.password_hash, data.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401

    # JWT identity must be a string
    token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))
    return jsonify({"access_token": token})


# -------------------
# Request Routes
# -------------------
@api.route("/requests", methods=["GET"])
@jwt_required()
def get_requests():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    requests_query = Request.query.paginate(page=page, per_page=per_page, error_out=False)
    requests = [
        {
            "id": r.id,
            "title": r.title,
            "description": r.description,
            "priority": r.priority,
            "status": r.status,
            "user_id": r.user_id,
            "responses": [resp.to_dict() for resp in r.responses]
        }
        for r in requests_query.items
    ]
    return jsonify({
        "data": requests,
        "total": requests_query.total,
        "page": requests_query.page,
        "pages": requests_query.pages,
    })


@api.route("/requests", methods=["POST"])
@jwt_required()
def create_request():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    new_request = Request(
        title=data.get("title"),
        description=data.get("description"),
        priority=data.get("priority", "Low"),
        status=data.get("status", "Open"),
        user_id=user_id,
    )
    db.session.add(new_request)
    db.session.commit()
    return jsonify({"message": "Request created", "id": new_request.id}), 201


@api.route("/requests/<int:request_id>", methods=["PATCH"])
@jwt_required()
def update_request(request_id):
    user_id = int(get_jwt_identity())
    req = Request.query.get_or_404(request_id)

    if req.user_id != user_id:
        return jsonify({"error": "Not authorized"}), 403

    data = request.get_json()
    for field in ["title", "description", "priority", "status"]:
        if field in data:
            setattr(req, field, data[field])

    db.session.commit()
    return jsonify({"message": "Request updated"})


@api.route("/requests/<int:request_id>", methods=["DELETE"])
@jwt_required()
def delete_request(request_id):
    user_id = int(get_jwt_identity())
    req = Request.query.get_or_404(request_id)

    if req.user_id != user_id:
        return jsonify({"error": "Not authorized"}), 403

    db.session.delete(req)
    db.session.commit()
    return jsonify({"message": "Request deleted"})


# -------------------
# Response Routes
# -------------------
@api.route("/requests/<int:request_id>/responses", methods=["POST"])
@jwt_required()
def create_response(request_id):
    user_id = int(get_jwt_identity())
    req = Request.query.get_or_404(request_id)

    data = request.get_json()
    response = Response(
        content=data.get("content"),
        request_id=req.id,
    )
    db.session.add(response)
    db.session.commit()

    return jsonify({"message": "Response added", "id": response.id}), 201


@api.route("/requests/<int:request_id>/responses", methods=["GET"])
@jwt_required()
def get_responses(request_id):
    req = Request.query.get_or_404(request_id)
    responses = [
        {"id": r.id, "content": r.content, "request_id": r.request_id}
        for r in req.responses
    ]
    return jsonify(responses)
