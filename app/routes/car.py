from flask import Blueprint, request, render_template, redirect, flash, url_for
from flask_login import login_required, current_user
from app import db
from bson import ObjectId
from app.models.car_model import Car

car_bp = Blueprint('car', __name__)

# ──────────────────────────────
# Customer Routes
# ──────────────────────────────

@car_bp.route('/cars/', methods=["GET"])
def list_cars_customer():
    """
    List all cars.
    """
    cars = Car.get_all_cars()
    return render_template('customer/cars/list.html', cars=cars)

# Loads the car details page
@car_bp.route('/cars/<car_id>', methods=["GET"])
def show_car_details(car_id):
    """
    Loads the car details page.
    """
    car = Car.get_car_by_id(car_id)
    
    if not car:
        flash("Car not found", "error")
        return redirect(url_for('car.list_cars_customer'))
        
    return render_template('customer/cars/details.html', car=car)

# ──────────────────────────────
# Admin Routes
# ──────────────────────────────

@car_bp.route('/admin/cars', methods=["GET"])
@login_required
def list_cars_admin():
    """
    List all cars.
    """
    cars = Car.get_all_cars()
    return render_template('admin/cars/table.html', cars=cars)

# Loads the add car form
@car_bp.route('/admin/cars/add', methods=["GET"])
@login_required
def show_add_car_form():
    """
    Show the add car form.
    """
    return render_template('admin/cars/add.html')

# Handles the add car form
@car_bp.route('/admin/cars/add', methods=["POST"])
@login_required
def add_new_car():
    """
    Add a new car.
    """
    try:
        data = request.form
        model = data.get("model", "").strip()
        brand = data.get("brand", "").strip()
        year = data.get("year", "").strip()
        seats = data.get("seats", "").strip()
        price_per_day = data.get("price_per_day", "").strip()
        image_url = data.get("image_url", "").strip()
        fuel_type = data.get("fuel_type", "").strip()
        transmission = data.get("transmission", "").strip()
        car_type = data.get("car_type", "").strip()
        description = data.get("description", "").strip()
        is_available = data.get("is_available") == "on"
        user_id = str(current_user._id)
                
        # Validate required fields
        if not all([model, brand, year, seats, price_per_day, image_url, fuel_type, transmission, car_type, description]):
            flash("All fields are required", "error")
            return redirect(url_for('car.show_add_car_form'))
        
        car = Car(
            model=model,
            brand=brand,
            year=year,
            seats=seats,
            price_per_day=price_per_day,
            image_url=image_url,
            fuel_type=fuel_type,
            transmission=transmission,
            car_type=car_type,
            user_id=user_id,
            description=description,
            is_available=is_available
        )
        car.save()
        flash("Car added successfully", "success")
        return redirect(url_for('car.list_cars_admin'))
    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for('car.show_add_car_form'))

# Handles the edit car form
@car_bp.route('/admin/cars/edit/<car_id>', methods=["GET"])
@login_required
def show_edit_car_form(car_id):
    """
    Show the edit car form.
    """
    car = Car.get_car_by_id(car_id)
    if not car:
        flash("Car not found", "error")
        return redirect(url_for('car.list_cars_admin'))
    return render_template('admin/cars/edit.html', car=car)

@car_bp.route('/admin/cars/edit/<car_id>', methods=["POST"])
@login_required
def edit_car_details(car_id):
    """
    Edit a car.
    """
    try:
        data = request.form
        model = data.get("model", "").strip()
        brand = data.get("brand", "").strip()
        year = data.get("year", "").strip()
        seats = data.get("seats", "").strip()
        price_per_day = data.get("price_per_day", "").strip()
        image_url = data.get("image_url", "").strip()
        fuel_type = data.get("fuel_type", "").strip()
        transmission = data.get("transmission", "").strip()
        car_type = data.get("car_type", "").strip()
        description = data.get("description", "").strip()
        is_available = data.get("is_available") == "on"

        existing_car = Car.get_car_by_id(car_id)
        if not existing_car:
            flash("Car not found", "error")
            return redirect(url_for('car.list_cars_admin'))
        
        existing_car.model = model
        existing_car.brand = brand
        existing_car.year = year
        existing_car.seats = seats
        existing_car.price_per_day = price_per_day
        existing_car.image_url = image_url
        existing_car.fuel_type = fuel_type  
        existing_car.transmission = transmission
        existing_car.car_type = car_type
        existing_car.description = description
        existing_car.is_available = is_available

        existing_car.update()
        flash("Car updated successfully", "success")
        return redirect(url_for('car.list_cars_admin'))
    except Exception as e:
        flash(f"An error occurred: {e}", "error")
        return redirect(url_for('car.show_edit_car_form', car_id=car_id))
    
# Handles the delete car form
@car_bp.route('/admin/cars/delete/<car_id>', methods=["GET"])
@login_required
def delete_car(car_id):
    """
    Delete a car.
    """
    car = Car.get_car_by_id(car_id)
    if not car:
        flash("Car not found", "error")
        return redirect(url_for('car.list_cars_admin'))
    
    car.delete()
    flash("Car deleted successfully", "success")
    return redirect(url_for('car.list_cars_admin'))
