from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username
    
    def __init__(self, username, email):
        self.username = username
        self.email = email

@app.route('/')
def index():
    return 'Hello World!'

@app.route('/users')
def users():
    users = User.query.all()
    return str(users)

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    return str(user)

@app.route('/add_user/<username>/<email>', methods=['POST'])
def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return 'User added'

@app.route('/delete_user/<username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    db.session.delete(user)
    db.session.commit()
    return 'User deleted'

if __name__ == '__main__':
    app.run()