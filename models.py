import logging
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId
from extensions import mongo

class User(UserMixin):
    def __init__(self, username, email, auth0_id, balance=0.0, _id=None):
        self.username = username
        self.email = email
        self.auth0_id = auth0_id
        self.balance = balance
        self._id = _id if _id else ObjectId()

    def get_id(self):
        return str(self.auth0_id)

    def save(self):
        user_data = {
            'username': self.username,
            'email': self.email,
            'auth0_id': self.auth0_id,
            'balance': self.balance
        }
        try:
            result = mongo.db.users.update_one(
                {'auth0_id': self.auth0_id},
                {'$set': user_data},
                upsert=True
            )
            if result.upserted_id:
                self._id = result.upserted_id
            logging.debug(f"User saved successfully: {self.username}")
        except Exception as e:
            logging.error(f"Error saving user: {str(e)}")

    @classmethod
    def from_dict(cls, data):
        user = cls(
            username=data['username'],
            email=data['email'],
            auth0_id=data['auth0_id'],
            balance=data.get('balance', 0.0),
        )
        user._id = data.get('_id')
        return user

    @classmethod
    def get_user_by_email(cls, email):
        user_data = mongo.db.users.find_one({'email': email})
        return cls.from_dict(user_data) if user_data else None

    @classmethod
    def get_user_by_auth0_id(cls, auth0_id):
        user_data = mongo.db.users.find_one({'auth0_id': auth0_id})
        return cls.from_dict(user_data) if user_data else None

class VM:
    def __init__(self, name, cpu_cores, ram, disk_size, user_id, azure_id, ip_address, os_image, _id=None):
        self.name = name
        self.cpu_cores = cpu_cores
        self.ram = ram
        self.disk_size = disk_size
        self.user_id = user_id
        self.azure_id = azure_id
        self.ip_address = ip_address
        self.os_image = os_image
        self._id = _id if _id else ObjectId()

    def save(self):
        vm_data = {
            'name': self.name,
            'cpu_cores': self.cpu_cores,
            'ram': self.ram,
            'disk_size': self.disk_size,
            'user_id': self.user_id,
            'azure_id': self.azure_id,
            'ip_address': self.ip_address,
            'os_image': self.os_image
        }
        try:
            if self._id:
                result = mongo.db.vms.update_one({'_id': self._id}, {'$set': vm_data})
            else:
                result = mongo.db.vms.insert_one(vm_data)
                self._id = result.inserted_id
            logging.debug(f"VM saved successfully: {self.name}")
        except Exception as e:
            logging.error(f"Error saving VM: {str(e)}")

    @classmethod
    def get_vms_by_user_id(cls, user_id):
        vms_data = mongo.db.vms.find({'user_id': user_id})
        return [cls(**vm_data) for vm_data in vms_data]

class Payment:
    def __init__(self, user_id, amount, reference, status, created_at, _id=None):
        self.user_id = user_id
        self.amount = amount
        self.reference = reference
        self.status = status
        self.created_at = created_at
        self._id = _id if _id else ObjectId()

    def save(self):
        payment_data = {
            'user_id': self.user_id,
            'amount': self.amount,
            'reference': self.reference,
            'status': self.status,
            'created_at': self.created_at
        }
        try:
            if self._id:
                result = mongo.db.payments.update_one({'_id': self._id}, {'$set': payment_data})
            else:
                result = mongo.db.payments.insert_one(payment_data)
                self._id = result.inserted_id
            logging.debug(f"Payment saved successfully: {self.reference}")
        except Exception as e:
            logging.error(f"Error saving payment: {str(e)}")
