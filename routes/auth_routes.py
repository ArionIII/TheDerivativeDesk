from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
import os
from config import db

auth_routes = Blueprint("auth_routes", __name__)

# Connect to MongoDB

users_collection = db.get_collection("users")


@auth_routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Validate user
        user = users_collection.find_one({"email": email})
        if user and check_password_hash(user["password"], password):
            session["user_id"] = str(user["_id"])
            session["first_name"] = user["first_name"]
            session["profile_picture"] = user.get("profile_picture", "/static/images/default-profile.png")
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid email or password.", "danger")
    
    return render_template("login.html")

@auth_routes.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        # Validation
        if password != confirm_password:
            flash("Passwords do not match.", "danger")
        elif users_collection.find_one({"email": email}):
            flash("Email already registered.", "danger")
        else:
            hashed_password = generate_password_hash(password)
            users_collection.insert_one({
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": hashed_password,
                "profile_picture": "/static/images/default-profile.png",
            })
            flash("Registration successful! You can now log in.", "success")
            return redirect(url_for("auth_routes.login"))
    
    return render_template("register.html")

@auth_routes.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth_routes.login"))
