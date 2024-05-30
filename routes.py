from flask import Blueprint, abort, flash, request
from flask import render_template, redirect, url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash

from forms import LoginForm, RegisterForm, TicketForm, DeleteTicketForm
from database.models import User, db, Group, Ticket
from decorators import admin_required, admin_or_manager_required, analyst_required


main_bp = Blueprint("main", __name__, template_folder="templates")



@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login success!", category="success")
            return redirect(url_for("main.index"))
    return render_template("login.html", form=form)


@main_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=generate_password_hash(form.password.data, method="pbkdf2:sha256"),
            role="User",
        )
        db.session.add(user)
        db.session.commit()
        flash("Account created!", category="success")
        return redirect(url_for("main.login"))
    return render_template("register.html", form=form)


@main_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))


@main_bp.route("/tickets")
@login_required
def tickets():
    form = DeleteTicketForm()
    if current_user.is_admin():
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(user_id=current_user.id)
    return render_template("tickets.html", tickets=tickets, form=form)


@main_bp.route("/tickets/new", methods=["GET", "POST"])
@login_required
@admin_or_manager_required
def create_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            note=form.note.data,
            status="Pending",
            user_id=current_user.id,
        )
        db.session.add(ticket)
        db.session.commit()
        flash("Ticket created!", category="success")
        return redirect(url_for("main.tickets"))
    return render_template("create_ticket.html", form=form)


@main_bp.route("/tickets/<int:ticket_id>/update", methods=["GET", "POST"])
@login_required
@admin_or_manager_required
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = TicketForm()
    if form.validate_on_submit():
        ticket.note = form.note.data
        ticket.status = form.status.data
        db.session.commit()
        flash("Ticket updated!", category="success")
        return redirect(url_for("main.tickets"))
    elif request.method == 'GET':
        form.note.data = ticket.note
        form.status.data = ticket.status
    return render_template('create_ticket.html', form=form)


@main_bp.route("/tickets/<int:ticket_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = DeleteTicketForm()
    if form.validate_on_submit():
        db.session.delete(ticket)
        db.session.commit()
        flash("Ticket deleted!", category="success")
    return redirect(url_for("main.tickets"))
