from flask_login import LoginManager, UserMixin, login_user, login_required
from flask import Flask

app = Flask(__name__)
app.secret_key = "your_secret_key"

login_manager = LoginManager(app)

class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['POST'])
def login():
    user_id = request.json.get("user_id")
    user = User(user_id)
    login_user(user)
    return jsonify({"message": "Logged in successfully!"})