from flask import Blueprint
from flask import render_template


from database.models import User, db, Group, Ticket


main_bp = Blueprint("main", __name__, template_folder="templates")




@main_bp.route("/")
def index():
    user = User.query.first()
    return render_template("index.html", user=user)
