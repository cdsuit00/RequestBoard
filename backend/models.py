from datetime import datetime
from backend.app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)

    requests = db.relationship("Request", backref="user", lazy=True)

    def to_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(50), default="Open")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    responses = db.relationship("Response", backref="request", cascade="all, delete-orphan")

    def to_dict(self, include_responses=False):
        data = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "status": self.status,
            "date_created": self.date_created.isoformat(),
            "user_id": self.user_id,
        }
        if include_responses:
            data["responses"] = [r.to_dict() for r in self.responses]
        return data

class Response(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    request_id = db.Column(db.Integer, db.ForeignKey("request.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "date_created": self.date_created.isoformat(),
            "request_id": self.request_id,
        }
