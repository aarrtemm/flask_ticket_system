from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from database.models import db, migrate, User, Group
from werkzeug.security import generate_password_hash, check_password_hash
import routes



app = Flask(__name__)
app.config.from_object("config")
db.init_app(app)
migrate.init_app(app, db)
app.register_blueprint(routes.main_bp)
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def create_tables():
    db.create_all()
    if not User.query.first():
        user = User(
            username="admin",
            password=generate_password_hash("admin", method="pbkdf2:sha256"),
            role="Admin"
            )
        customer1 = Group(name="Customer 1")
        customer2 = Group(name="Customer 2")
        customer3 = Group(name="Customer 3")
        db.session.add_all([user, customer1, customer2, customer3])
        db.session.commit()

    


if __name__ == "__main__":
    app.run(debug=True)
