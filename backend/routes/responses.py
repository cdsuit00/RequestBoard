from flask import Blueprint, request, jsonify
from extensions import db
from models import Response, Request as Req
from utils.auth_decorators import login_required

responses_bp = Blueprint('responses', __name__)

@responses_bp.route('/', methods=['POST'])
@login_required
def create_response(current_user):
    data = request.get_json() or {}
    request_id = data.get('request_id')
    content = (data.get('content') or '').strip()
    if not request_id or not content:
        return jsonify({'error': 'request_id and content are required'}), 400
    req = Req.query.get(request_id)
    if not req:
        return jsonify({'error': 'Parent request not found'}), 404
    resp = Response(content=content, request_id=request_id, user_id=current_user.id)
    db.session.add(resp)
    db.session.commit()
    return jsonify(resp.to_dict()), 201

@responses_bp.route('/<int:response_id>', methods=['PATCH'])
@login_required
def update_response(current_user, response_id):
    resp = Response.query.get_or_404(response_id)
    # Optionally only allow author to edit
    if resp.user_id != current_user.id:
        return jsonify({'error': 'Forbidden: not the author of this response'}), 403
    data = request.get_json() or {}
    if 'content' not in data:
        return jsonify({'error': 'content required'}), 400
    resp.content = data['content']
    db.session.commit()
    return jsonify(resp.to_dict()), 200

@responses_bp.route('/<int:response_id>', methods=['DELETE'])
@login_required
def delete_response(current_user, response_id):
    resp = Response.query.get_or_404(response_id)
    if resp.user_id != current_user.id:
        return jsonify({'error': 'Forbidden: not the author of this response'}), 403
    db.session.delete(resp)
    db.session.commit()
    return jsonify({'message': 'Response deleted'}), 200
