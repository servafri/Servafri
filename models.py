from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from extensions import mongo

class User(UserMixin):
    def __init__(self, username, email, password_hash, balance=0.0, _id=None):
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.balance = balance
        self._id = _id if _id else ObjectId()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def get_user_by_id(cls, user_id):
        user_data = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return cls(**user_data) if user_data else None

    @classmethod
    def get_user_by_username(cls, username):
        user_data = mongo.db.users.find_one({"username": username})
        return cls(**user_data) if user_data else None

    def save(self):
        mongo.db.users.update_one({"_id": self._id}, {"$set": self.__dict__}, upsert=True)

    def get_id(self):
        return str(self._id)

class VM:
    def __init__(self, name, cpu_cores, ram, disk_size, user_id, azure_id, ip_address=None, os_image='ubuntu', _id=None):
        self.name = name
        self.cpu_cores = cpu_cores
        self.ram = ram
        self.disk_size = disk_size
        self.user_id = user_id
        self.azure_id = azure_id
        self.ip_address = ip_address
        self.os_image = os_image
        self._id = _id if _id else ObjectId()

    @classmethod
    def get_vms_by_user_id(cls, user_id):
        return [cls(**vm_data) for vm_data in mongo.db.vms.find({"user_id": user_id})]

    def save(self):
        mongo.db.vms.update_one({"_id": self._id}, {"$set": self.__dict__}, upsert=True)

class Payment:
    def __init__(self, user_id, amount, reference, status, created_at, _id=None):
        self.user_id = user_id
        self.amount = amount
        self.reference = reference
        self.status = status
        self.created_at = created_at
        self._id = _id if _id else ObjectId()

    def save(self):
        mongo.db.payments.update_one({"_id": self._id}, {"$set": self.__dict__}, upsert=True)
