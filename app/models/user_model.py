from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import re

class User(UserMixin):
    """
    A class representing a user.
    """
    def __init__(self, first_name: str, last_name: str, email: str, password: str, _id: str = None):
        """
        Initialize a User object.
        """
        self._id = ObjectId(_id)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = self.hash_password(password)
        
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password.
        """
        return generate_password_hash(password)
        
    @staticmethod
    def verify_password(hashed_password: str, password: str) -> bool:
        """
        Verify a password against a hashed password.
        """
        return check_password_hash(hashed_password, password)
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate an email address.
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def get_id(self):
        """Overriding UserMixin method to return custom _id"""
        return str(self._id)
    
    def to_dict(self) -> dict:
        """
        Convert the User object to a dictionary.
        """
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'password': self.password,
            '_id': self._id
        }
    
    def __str__(self):
        """
        Return a string representation of the User object.
        """
        return f"User(id={self._id}, name={self.first_name} {self.last_name}, email={self.email})"

class Customer(User):
    """
    A class representing a customer.
    """
    def __init__(self, first_name: str, last_name: str, email: str, password: str, phone_number: str, address: str, balance: float = 0, _id: str = None, role: str = "customer"):
        super().__init__(first_name, last_name, email, password, _id)
        self.phone_number = phone_number
        self.address = address
        self.balance = float(balance)
        self.role = role
        
    def to_dict(self) -> dict:
        """
        Convert the Customer object to a dictionary.
        """
        data = super().to_dict()
        data.update({
            'phone_number': self.phone_number,
            'address': self.address,
            'balance': self.balance,
            'role': self.role
        })
        return data
        
class Admin(User):
    """
    A class representing an admin.
    """
    def __init__(self, first_name: str, last_name: str, email: str, password: str, _id: str = None, role: str = "admin"):
        super().__init__(first_name, last_name, email, password, _id)
        self.role = role
        
    def to_dict(self) -> dict:
        """
        Convert the Admin object to a dictionary.
        """
        data = super().to_dict()
        data.update({
            'role': self.role
        })
        return data
        

