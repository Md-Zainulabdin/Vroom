from bson import ObjectId
from app import db

class Car():
    """
    A class representing a car.
    """
    def __init__(self, model: str, brand: str, year: int, seats: int, price_per_day: float, image_url: str, fuel_type: str, is_available: bool, transmission: str, car_type: str, user_id: str, _id: str = None, description: str = ""):
        """
        Initialize a Car object.
        """
        self._id = ObjectId(_id)
        self.user_id = user_id
        self.model = model
        self.brand = brand
        self.year = year
        self.seats = seats
        self.price_per_day = price_per_day
        self.image_url = image_url
        self.is_available = is_available
        self.fuel_type = fuel_type # e.g: "electric", "petrol", "diesel", "hybrid"
        self.transmission = transmission # e.g: "automatic", "manual"
        self.car_type = car_type # e.g: "sedan", "suv", "hatchback", "luxury", "van"
        self.description = description
        
    @staticmethod
    def get_all_cars():
        """
        Get all cars from the database.
        """
        return db.cars.find()
    
    @staticmethod
    def filter_cars(filter: dict):
        """
        Filter cars from the database.
        """
        return db.cars.find(filter)
    
    @staticmethod
    def get_car_by_id(car_id: str):
        """
        Get a car from the database by id.
        """
        car_data = db.cars.find_one({"_id": ObjectId(car_id)})
        
        if car_data:
            return Car(
                model=car_data['model'],
                brand=car_data['brand'],
                year=car_data['year'],
                seats=car_data['seats'],
                price_per_day=car_data['price_per_day'],
                image_url=car_data['image_url'],
                fuel_type=car_data['fuel_type'],
                transmission=car_data['transmission'],
                car_type=car_data['car_type'],
                user_id=(car_data['user_id']),
                _id=str(car_data['_id']),
                is_available=car_data['is_available'],
                description=car_data.get('description', '')
            )
        return None
    
    @staticmethod
    def get_car_by_user_id(user_id: str):
        """
        Get a car from the database by user id.
        """
        return db.cars.find_one({"user_id": ObjectId(user_id)})
    
    def save(self):
        """
        Save the car to the database.
        """
        db.cars.insert_one(self.to_dict())
        
    def update(self):
        """
        Update the car in the database.
        """
        db.cars.update_one({"_id": self._id}, {"$set": self.to_dict()})
        
    def delete(self):
        """
        Delete the car from the database.
        """
        db.cars.delete_one({"_id": self._id})
        
    def to_dict(self) -> dict:
        """
        Convert the Car object to a dictionary.
        """
        return {
            'model': self.model,
            'brand': self.brand,
            'year': self.year,
            'seats': self.seats,
            'price_per_day': self.price_per_day,
            'image_url': self.image_url,
            'is_available': self.is_available,
            'fuel_type': self.fuel_type,
            'transmission': self.transmission,
            'car_type': self.car_type,
            'description': self.description,
            '_id': self._id,
            'user_id': self.user_id
        }
        
    def __str__(self) -> str:
        """
        Return a string representation of the Car object.
        """
        return f"Car(model={self.model}, brand={self.brand}, year={self.year}, seats={self.seats}, price_per_day={self.price_per_day}, image_url={self.image_url}, fuel_type={self.fuel_type}, transmission={self.transmission}, car_type={self.car_type}, description={self.description})"
