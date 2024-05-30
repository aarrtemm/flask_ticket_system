from flask import Blueprint
from flask import render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from forms import LoginForm, RegisterForm, TicketForm
from database.models import User, db, Group, Ticket


main_bp = Blueprint("main", __name__, template_folder="templates")




@main_bp.route("/")
def index():
    return render_template("index.html", current_user=current_user)


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("main.index"))
    return render_template("login.html", form=form)


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=generate_password_hash(form.password.data, method="pbkdf2:sha256"),
            role="User",
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("main.index"))
    return render_template("register.html", form=form)


@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@main_bp.route("/tickets", methods=["GET", "POST"])
@login_required
def tickets():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            note=form.note.data,
            status="Pending",
            user_id=current_user.id,
            group_id=current_user.group_id
        )
        db.session.add(ticket)
        db.session.commit()
        return redirect(url_for("main.tickets"))
    
    if current_user.role == "Admin":
        tickets = Ticket.query.all()

    else:
        tickets = Ticket.query.filter_by(group_id=current_user.group_id).all()
    return render_template("tickets.html", form=form, tickets=tickets)