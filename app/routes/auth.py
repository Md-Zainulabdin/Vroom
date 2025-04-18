from flask import Blueprint, request, render_template, redirect, flash, url_for
from app.models.user_model import Customer, Admin, User
from flask_login import login_user, current_user
from app import db, login_manager
from bson import ObjectId

auth_bp = Blueprint("auth", __name__, template_folder='templates')

# ──────────────────────────────
# Routes
# ──────────────────────────────

@login_manager.user_loader
def load_user(user_id):
    """
    Load a user from the database.
    """
    try:
        user_data = db.users.find_one({"_id": ObjectId(user_id)})
        if user_data:
            if user_data["role"] == "customer":
                return Customer(**user_data)
            elif user_data["role"] == "admin":
                return Admin(**user_data)
    except Exception as e:
        print(f"Error loading user: {e}")
        return None

@auth_bp.route("/register", methods=["GET"])
def show_register():
    """
    Shows the registration form.
    """
    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET"])
def show_login():
    """
    Shows the login form.
    """
    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Registers a new user.
    """
    data = request.form
    first_name = data.get("first_name", "").strip()
    last_name = data.get("last_name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    phone_number = data.get("phone_number", "").strip()
    address = data.get("address", "").strip()
    
    # Validate required fields
    if not all([first_name, last_name, email, password]):
        flash("All fields are required", "error")
        return redirect(url_for("auth.register"))
        
    
    if not User.validate_email(email):
        flash("Invalid email address", "error")
        return redirect(url_for("auth.register"))
        
    try:
        # Check if user already exists
        existing_user = db.users.find_one({"email": email})
        if existing_user:
            flash("User already exists", "error")
            return redirect(url_for("auth.register"))
        
        # Create new user
        new_user = Customer(first_name, last_name, email, password, phone_number, address)
        db.users.insert_one(new_user.to_dict())
        
        flash("Registration successful", "success")
        return redirect(url_for("auth.login"))
    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for("auth.register"))
        
@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Logs in a user.
    """
    data = request.form
    email = data.get("email", "").strip()
    password = data.get("password", "").strip()
    
    # Validate required fields
    if not all([email, password]):
        flash("Email and password are required.", 'error')
        return redirect(url_for("auth.login"))
    
    if not User.validate_email(email):
        flash("Please enter a valid email address.", 'error')
        return redirect(url_for("auth.login"))
        
    try:
        # Check if user exists
        user_data = db.users.find_one({"email": email})
        if not user_data:
            flash("User with this email does not exist", "error")
            return redirect(url_for("auth.login"))
        
        # Verify password
        if not User.verify_password(user_data["password"], password):
            flash("Incorrect password.", "error")
            return redirect(url_for("auth.login"))
                
        if user_data["role"] == "admin":
            user = Admin(**user_data)
            login_user(user, remember=True)
            flash("Admin login successful", "success")
            return redirect(url_for("admin.dashboard"))
        else:
            user = Customer(**user_data)
            login_user(user, remember=True)
            flash("Login successful", "success")
            
            return redirect(url_for("home.home"))
        
    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for("auth.login"))
        
        
        
        
        
        
        
        







