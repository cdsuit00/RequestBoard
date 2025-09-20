from flask import Blueprint, request, jsonify, abort
from backend.models import db, User, Request, Response

api = Blueprint("api", __name__)

# ------------------------
# USER ROUTES
# ------------------------
@api.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data.get("username") or not data.get("email"):
        abort(400, description="Username and email required.")
    
    user = User(username=data["username"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@api.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

# ------------------------
# REQUEST ROUTES
# ------------------------
@api.route("/requests", methods=["POST"])
def create_request():
    data = request.get_json()
    required = ["title", "description", "priority", "user_id"]
    if not all(field in data for field in required):
        abort(400, description="Missing required fields.")
    
    req = Request(
        title=data["title"],
        description=data["description"],
        priority=data["priority"],
        deadline=data.get("deadline"),
        status=data.get("status", "Open"),
        user_id=data["user_id"]
    )
    db.session.add(req)
    db.session.commit()
    return jsonify(req.to_dict()), 201

@api.route("/requests", methods=["GET"])
def list_requests():
    requests = Request.query.all()
    return jsonify([r.to_dict() for r in requests])

@api.route("/requests/<int:req_id>", methods=["GET"])
def get_request(req_id):
    req = Request.query.get_or_404(req_id)
    return jsonify(req.to_dict(include_responses=True))

@api.route("/requests/<int:req_id>", methods=["PATCH"])
def update_request(req_id):
    req = Request.query.get_or_404(req_id)
    data = request.get_json()
    
    for field in ["title", "description", "priority", "deadline", "status"]:
        if field in data:
            setattr(req, field, data[field])
    
    db.session.commit()
    return jsonify(req.to_dict())

@api.route("/requests/<int:req_id>", methods=["DELETE"])
def delete_request(req_id):
    req = Request.query.get_or_404(req_id)
    db.session.delete(req)
    db.session.commit()
    return jsonify({"message": "Request deleted"})

# ------------------------
# RESPONSE ROUTES
# ------------------------
@api.route("/responses", methods=["POST"])
def create_response():
    data = request.get_json()
    if not data.get("content") or not data.get("request_id"):
        abort(400, description="Content and request_id required.")
    
    resp = Response(content=data["content"], request_id=data["request_id"])
    db.session.add(resp)
    db.session.commit()
    return jsonify(resp.to_dict()), 201

@api.route("/responses/<int:resp_id>", methods=["GET"])
def get_response(resp_id):
    resp = Response.query.get_or_404(resp_id)
    return jsonify(resp.to_dict())

@api.route("/responses/<int:resp_id>", methods=["DELETE"])
def delete_response(resp_id):
    resp = Response.query.get_or_404(resp_id)
    db.session.delete(resp)
    db.session.commit()
    return jsonify({"message": "Response deleted"})
