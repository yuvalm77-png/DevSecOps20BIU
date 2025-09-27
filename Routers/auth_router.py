from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt, get_jwt_identity,
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies
)
from extensions import db
from Models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@auth_bp.post("/register")
def register():
    data = request.form
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not all([username, email, password]):
        return jsonify({"error": "username, email, password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already in use"}), 409

    is_admin = True if data.get("is_admin") == 'on' else False
    user = User(username=username, email=email, is_admin=is_admin)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    claims = {"user_id": user.id, "is_admin": user.is_admin}
    access = create_access_token(identity=user.email, additional_claims=claims)
    refresh = create_refresh_token(identity=user.email, additional_claims=claims)
    resp = jsonify({
        "user": {"id": user.id, "username": user.username, "email": user.email},
        "access_token": access,
        "refresh_token": refresh
    })
    # store JWTs in cookies
    set_access_cookies(resp, access)
    set_refresh_cookies(resp, refresh)
    return resp, 201

@auth_bp.post("/login", strict_slashes=False)
def login():
    data = request.form
    email = data.get("email")
    password = data.get("password")
    if not all([email, password]):
        return jsonify({"error": "email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    claims = {"user_id": user.id, "is_admin": user.is_admin}
    access = create_access_token(identity=user.email, additional_claims=claims)
    refresh = create_refresh_token(identity=user.email, additional_claims=claims)
    resp = jsonify({"access_token": access, "refresh_token": refresh})
    # send tokens via cookies instead of headers/localStorage
    set_access_cookies(resp, access)
    set_refresh_cookies(resp, refresh)
    return resp, 200

@auth_bp.route("/logout")
def logout():
    resp = jsonify({"message": "Logged out"})
    unset_jwt_cookies(resp)
    return redirect('/', code=302)

@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    claims = get_jwt()
    identity = claims.get("sub")
    new_access = create_access_token(identity=identity, additional_claims={
        "user_id": claims.get("user_id"),
        "is_admin": claims.get("is_admin", False)
    })
    resp = jsonify({"access_token": new_access})
    set_access_cookies(resp, new_access)  # set new access token in cookie
    return resp, 200

@auth_bp.get("/me")
@jwt_required()
def me():
    claims = get_jwt()
    user = User.query.filter_by(email=claims.get("sub")).first()
    return jsonify({
        "email": claims.get("sub"),
        "user_id": claims.get("user_id"),
        "is_admin": claims.get("is_admin", False),
        "username": user.username
    }), 200
