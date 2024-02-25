from src.extensions import db
from datetime import datetime


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(200))
    title = db.Column(db.String(200))
    upvotes = db.Column(db.Integer)
    body_text = db.Column(db.String(20000))
    _created_at = db.Column(db.DateTime, default=datetime.utcnow)
    _last_updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Post "{self.title}">'
