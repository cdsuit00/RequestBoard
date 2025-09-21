from datetime import datetime
from backend.extensions import db

# ------------------------
# USER MODEL
# ------------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    requests = db.relationship("Request", backref="user", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }

# ------------------------
# REQUEST MODEL
# ------------------------
class Request(db.Model):
    __tablename__ = "requests"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.String(50))  # could be DateTime
    status = db.Column(db.String(50), default="Open")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    responses = db.relationship(
        "Response", backref="request", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "deadline": self.deadline,
            "status": self.status,
            "user_id": self.user_id,
            "responses": [r.to_dict() for r in self.responses],
        }

# ------------------------
# RESPONSE MODEL
# ------------------------
class Response(db.Model):
    __tablename__ = "responses"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    request_id = db.Column(db.Integer, db.ForeignKey("requests.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "date_created": self.date_created.isoformat(),
            "request_id": self.request_id,
        }
