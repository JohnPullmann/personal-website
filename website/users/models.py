from website import database, login_manager
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(database.Model, UserMixin):
    __tablename__ = 'user'
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String(20), unique=True, nullable=False)
    email = database.Column(database.String(120), unique=True, nullable=False)
    image_file = database.Column(database.String(20), nullable=False, default='default.jpg')
    password = database.Column(database.String(60), nullable=False)
    portfolio_comments = database.relationship('Portfolio_Comment', backref='author_object', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id})

    @staticmethod
    def verify_reset_token(token, max_age=1800):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=max_age)
            user_id = data['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    
class Portfolio_Comment(database.Model):
    __tablename__ = 'portfolio_comment'
    id = database.Column(database.Integer, primary_key=True)
    content = database.Column(database.Text, nullable=False)
    date_posted = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    user_id = database.Column(database.Integer, database.ForeignKey('user.id'), nullable=False)
    portfolio_element_id = database.Column(database.Integer, database.ForeignKey('portfolio_element.id'), nullable=False)

    def __repr__(self):
        return f"Portfolio_Comment('{self.author}', '{self.date_posted}')"