from datetime import datetime
from handyfarm import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='dummy.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)# Post 테이블과 관계를 맺어준다 1:다 관계 lazy를 써주면 무조건 관계가 있다.

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    content_img=db.Column(db.String(20), nullable=False, default='default2.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # 위의 모델에서 Post모델과 관게를 나타낼때는 단순히 테이블을 참조한다해서 대문자를 사용하고, user.id는 컬럼을 참조하기에 소문자

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"