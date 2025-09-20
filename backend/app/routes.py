from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app import db
from app.models import User, Request, Response

api = Blueprint('api', __name__)

# Authentication routes
@api.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Username already exists'}), 400
    
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token, 'user_id': user.id}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

# Request routes
@api.route('/requests', methods=['GET'])
@jwt_required()
def get_requests():
    user_id = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    requests = Request.query.filter_by(user_id=user_id).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'requests': [{
            'id': req.id,
            'title': req.title,
            'description': req.description,
            'priority': req.priority,
            'status': req.status,
            'date_created': req.date_created.isoformat()
        } for req in requests.items],
        'total': requests.total,
        'pages': requests.pages,
        'current_page': page
    })

@api.route('/requests', methods=['POST'])
@jwt_required()
def create_request():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    new_request = Request(
        title=data['title'],
        description=data['description'],
        priority=data.get('priority', 'medium'),
        user_id=user_id
    )
    
    db.session.add(new_request)
    db.session.commit()
    
    return jsonify({'message': 'Request created', 'id': new_request.id}), 201

@api.route('/requests/<int:request_id>', methods=['GET'])
@jwt_required()
def get_request(request_id):
    user_id = get_jwt_identity()
    req = Request.query.filter_by(id=request_id, user_id=user_id).first()
    
    if not req:
        return jsonify({'message': 'Request not found'}), 404
    
    return jsonify({
        'id': req.id,
        'title': req.title,
        'description': req.description,
        'priority': req.priority,
        'status': req.status,
        'date_created': req.date_created.isoformat(),
        'responses': [{
            'id': resp.id,
            'content': resp.content,
            'date_created': resp.date_created.isoformat()
        } for resp in req.responses]
    })

@api.route('/requests/<int:request_id>', methods=['PATCH'])
@jwt_required()
def update_request(request_id):
    user_id = get_jwt_identity()
    req = Request.query.filter_by(id=request_id, user_id=user_id).first()
    
    if not req:
        return jsonify({'message': 'Request not found'}), 404
    
    data = request.get_json()
    for field in ['title', 'description', 'priority', 'status']:
        if field in data:
            setattr(req, field, data[field])
    
    db.session.commit()
    return jsonify({'message': 'Request updated'})

@api.route('/requests/<int:request_id>', methods=['DELETE'])
@jwt_required()
def delete_request(request_id):
    user_id = get_jwt_identity()
    req = Request.query.filter_by(id=request_id, user_id=user_id).first()
    
    if not req:
        return jsonify({'message': 'Request not found'}), 404
    
    db.session.delete(req)
    db.session.commit()
    return jsonify({'message': 'Request deleted'})

# Response routes
@api.route('/requests/<int:request_id>/responses', methods=['POST'])
@jwt_required()
def create_response(request_id):
    user_id = get_jwt_identity()
    req = Request.query.filter_by(id=request_id, user_id=user_id).first()
    
    if not req:
        return jsonify({'message': 'Request not found'}), 404
    
    data = request.get_json()
    response = Response(content=data['content'], request_id=request_id)
    
    db.session.add(response)
    db.session.commit()
    
    return jsonify({'message': 'Response created', 'id': response.id}), 201