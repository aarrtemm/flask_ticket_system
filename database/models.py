from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    role = db.Column(
        db.Enum("Admin", "User", "Manager", "Analyst"),
        nullable=False,
        default="User"
        )
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))

    def is_admin(self):
        return self.role == "Admin"
    
    def is_manager(self):
        return self.role == "Manager"
    
    def is_analyst(self):
        return self.role == "Analyst"



class Group(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship("User", backref="group")


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    note = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.Enum("Pending", "Closed", "In review"), default="Pending", nullable=False
        )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"))
