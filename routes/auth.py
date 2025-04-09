from flask import Blueprint, request, jsonify, current_app, render_template, redirect, url_for, flash, session
from models import User
from app import db
import jwt
import datetime
from functools import wraps

auth_bp = Blueprint("auth_bp", __name__, template_folder="../templates/auth")

# Decorator to protect routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user_id"):
            flash("You must be logged in to access this page.", "warning")
            return redirect(url_for("auth_bp.login_form"))
        return f(*args, **kwargs)
    return decorated_function

# API-based registration
@auth_bp.route("/api/auth/register", methods=["POST"])
def api_register():
    data = request.get_json() or {}
    if not data.get("username") or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Missing required fields"}), 400

    if User.query.filter((User.username == data["username"]) | (User.email == data["email"])).first():
        return jsonify({"message": "User already exists"}), 400

    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# API-based login
@auth_bp.route("/api/auth/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    user = User.query.filter_by(username=data.get("username")).first()
    if user and user.check_password(data.get("password")):
        token = jwt.encode({
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)
        }, current_app.config["SECRET_KEY"], algorithm="HS256")
        return jsonify({"token": token})
    return jsonify({"message": "Invalid credentials"}), 401

# HTML form: GET routes
@auth_bp.route("/login", methods=["GET"])
def login_form():
    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET"])
def register_form():
    return render_template("auth/register.html")

# HTML form: POST registration
@auth_bp.route("/register/form", methods=["POST"])
def register_form_post():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    if not username or not email or not password:
        flash("All fields are required.", "warning")
        return redirect(url_for("auth_bp.register_form"))

    if User.query.filter((User.username == username) | (User.email == email)).first():
        flash("User already exists.", "warning")
        return redirect(url_for("auth_bp.register_form"))

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    flash("Registration successful. Please login.", "success")
    return redirect(url_for("auth_bp.login_form"))

# HTML form: POST login
@auth_bp.route("/login/form", methods=["POST"])
def login_form_post():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session["user_id"] = user.id
        session["username"] = user.username
        flash("Login successful!", "success")
        return redirect(url_for("dashboard_bp.dashboard_home"))

    flash("Invalid credentials.", "danger")
    return redirect(url_for("auth_bp.login_form"))

# Logout route
@auth_bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect("/")
