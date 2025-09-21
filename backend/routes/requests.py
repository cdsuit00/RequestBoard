from flask import Blueprint, request, jsonify
from extensions import db
from models import Request, Response
from utils.auth_decorators import login_required
from sqlalchemy import desc
from datetime import datetime

requests_bp = Blueprint('requests', __name__)

def paginate_query(query):
    try:
        page = int(request.args.get('page', 1))
    except:
        page = 1
    try:
        per_page = int(request.args.get('per_page', 10))
    except:
        per_page = 10
    per_page = min(max(per_page, 1), 100)
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    items = [item.to_dict() for item in pagination.items]
    return {
        'items': items,
        'total': pagination.total,
        'page': pagination.page,
        'per_page': pagination.per_page,
        'pages': pagination.pages
    }

@requests_bp.route('/', methods=['GET'])
def list_requests():
    q = Request.query.order_by(desc(Request.date_created))
    # Filtering
    status = request.args.get('status')
    priority = request.args.get('priority')
    user_id = request.args.get('user_id')
    if status:
        q = q.filter_by(status=status)
    if priority:
        q = q.filter_by(priority=priority)
    if user_id:
        try:
            uid = int(user_id)
            q = q.filter_by(user_id=uid)
        except:
            pass
    return jsonify(paginate_query(q)), 200

@requests_bp.route('/<int:request_id>', methods=['GET'])
def get_request(request_id):
    req = Request.query.get_or_404(request_id)
    return jsonify(req.to_dict(detail=True)), 200

@requests_bp.route('/', methods=['POST'])
@login_required
def create_request(current_user):
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    description = data.get('description')
    priority = data.get('priority') or 'medium'
    status = data.get('status') or 'open'
    deadline = data.get('deadline')  # ISO string expected
    deadline_dt = None
    if deadline:
        try:
            deadline_dt = datetime.fromisoformat(deadline)
        except:
            return jsonify({'error': 'Invalid deadline format; use ISO 8601'}), 400

    req = Request(
        title=title,
        description=description,
        priority=priority,
        status=status,
        deadline=deadline_dt,
        user_id=current_user.id
    )
    db.session.add(req)
    db.session.commit()
    return jsonify(req.to_dict()), 201

@requests_bp.route('/<int:request_id>', methods=['PATCH'])
@login_required
def update_request(current_user, request_id):
    req = Request.query.get_or_404(request_id)
    if req.user_id != current_user.id:
        return jsonify({'error': 'Forbidden: not the owner'}), 403
    data = request.get_json() or {}
    updatable = ['title', 'description', 'priority', 'status', 'deadline']
    for key in updatable:
        if key in data:
            if key == 'deadline' and data[key]:
                try:
                    dt = datetime.fromisoformat(data[key])
                    setattr(req, key, dt)
                except:
                    return jsonify({'error': 'Invalid deadline format; use ISO 8601'}), 400
            else:
                setattr(req, key, data[key])
    db.session.commit()
    return jsonify(req.to_dict()), 200

@requests_bp.route('/<int:request_id>', methods=['DELETE'])
@login_required
def delete_request(current_user, request_id):
    req = Request.query.get_or_404(request_id)
    if req.user_id != current_user.id:
        return jsonify({'error': 'Forbidden: not the owner'}), 403
    db.session.delete(req)
    db.session.commit()
    return jsonify({'message': 'Request deleted'}), 200
