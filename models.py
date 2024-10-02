from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bson import ObjectId

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

    def get_id(self):
        return str(self._id)

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            balance=data.get('balance', 0.0),
            _id=data['_id']
        )

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

class Payment:
    def __init__(self, user_id, amount, reference, status, created_at, _id=None):
        self.user_id = user_id
        self.amount = amount
        self.reference = reference
        self.status = status
        self.created_at = created_at
        self._id = _id if _id else ObjectId()

class KubernetesDeployment:
    def __init__(self, name, image, replicas, user_id, created_at, status, _id=None):
        self.name = name
        self.image = image
        self.replicas = replicas
        self.user_id = user_id
        self.created_at = created_at
        self.status = status
        self._id = _id if _id else ObjectId()
