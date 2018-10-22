from datetime import datetime
from blogz_package.hashutils import make_pw_hash, check_pw_hash
from blogz_package import db



class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    text = db.Column(db.Text)
    completed = db.Column(db.Boolean)
    moment = db.Column(db.DateTime, default=datetime.utcnow)  # possible hour ajustment fix: DateTime.UtcNow.ToLocalTime because I'm 7 hours off stl time.
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, text, owner, moment=None):
        self.title = title
        self.text = text
        self.owner = owner
        self.moment = moment
        

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(120))
    pw_hash = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')
    

    def __init__(self, username, email, password):
        self.username = username
        self.email = email # used as main username for signup
        self.pw_hash = make_pw_hash(password) 