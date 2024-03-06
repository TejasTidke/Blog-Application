from datetime import datetime
from flaskblog import db
from enum import Enum

class ReactionType(Enum):
    LIKE = 1
    LOVE = 2
    HATE = 3

class TargetType(Enum):
    BLOG = 1
    COMMENT = 2


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    comments = db.relationship('Comment', backref='blog', cascade='all, delete', lazy=True)
    reactions = db.relationship('Reaction', backref='blog', cascade='all, delete', lazy=True)

    def __repr__(self):
        return f"Blog('{self.title}', '{self.date_posted}', '{self.content}')"
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'), nullable=False)
    reactions = db.relationship('Reaction', backref='comment', cascade='all, delete', lazy=True)

    def __repr__(self):
        return f"Comment('{self.id}', '{self.text}')"
    
class Reaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Enum(ReactionType), nullable=False)  
    target_type = db.Column(db.Enum(TargetType), nullable=False)
    target_id = db.Column(db.Integer, nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

    def __repr__(self):
        return f"Reaction('{self.id}', '{self.type}')"