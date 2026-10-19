from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "super_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///applications.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Job application model
class JobApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    deadline = db.Column(db.String(50), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        session['username'] = user.username
        return jsonify({"message": "Login successful!"})
    return jsonify({"message": "Invalid credentials!"}), 401

@app.route('/add_application', methods=['POST'])
def add_application():
    data = request.json
    if not all(k in data for k in ('name', 'applicationDate', 'position', 'upcomingDeadlines')):
        return jsonify({"message": "Missing fields"}), 400
    new_app = JobApplication(
        name=data['name'],
        date=data['applicationDate'],
        position=data['position'],
        deadline=data['upcomingDeadlines']
    )
    db.session.add(new_app)
    db.session.commit()
    return jsonify({"message": "Application added"}), 201

@app.route('/applications', methods=['GET'])
def get_applications():
    applications = JobApplication.query.all()
    return jsonify([
        {"name": app.name, "date": app.date, "position": app.position, "deadline": app.deadline}
        for app in applications
    ])

@app.route('/create_user', methods=['POST'])
def create_user():
    data = request.json
    if 'username' not in data or 'password' not in data:
        return jsonify({"message": "Missing username/password"}), 400
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "User already exists!"}), 409
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201

if __name__ == '__main__':
    app.run(debug=True)
