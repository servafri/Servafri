import logging
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

    def get_id(self):
        return str(self._id)

    def save(self):
        user_data = {
            'username': self.username,
            'email': self.email,
            'password_hash': self.password_hash,
            'balance': self.balance
        }
        try:
            if self._id:
                result = mongo.db.users.update_one({'_id': self._id}, {'$set': user_data})
            else:
                result = mongo.db.users.insert_one(user_data)
                self._id = result.inserted_id
            logging.debug(f"User saved successfully: {self.username}")
        except Exception as e:
            logging.error(f"Error saving user: {str(e)}")

    @classmethod
    def from_dict(cls, data):
        user = cls(
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash'],
            balance=data.get('balance', 0.0),
        )
        user._id = data.get('_id')
        return user

    @classmethod
    def get_user_by_username(cls, username):
        user_data = mongo.db.users.find_one({'username': username})
        return cls.from_dict(user_data) if user_data else None

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
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            cpu_cores=data['cpu_cores'],
            ram=data['ram'],
            disk_size=data['disk_size'],
            user_id=data['user_id'],
            azure_id=data['azure_id'],
            ip_address=data.get('ip_address'),
            os_image=data.get('os_image', 'ubuntu'),
            _id=data.get('_id')
        )

    @classmethod
    def get_vms_by_user_id(cls, user_id):
        vms_data = mongo.db.vms.find({'user_id': user_id})
        return [cls.from_dict(vm_data) for vm_data in vms_data]

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

    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data['user_id'],
            amount=data['amount'],
            reference=data['reference'],
            status=data['status'],
            created_at=data['created_at'],
            _id=data.get('_id')
        )

class KubernetesDeployment:
    def __init__(self, name, image, replicas, user_id, created_at, status, _id=None):
        self.name = name
        self.image = image
        self.replicas = replicas
        self.user_id = user_id
        self.created_at = created_at
        self.status = status
        self._id = _id if _id else ObjectId()

    def save(self):
        deployment_data = {
            'name': self.name,
            'image': self.image,
            'replicas': self.replicas,
            'user_id': self.user_id,
            'created_at': self.created_at,
            'status': self.status
        }
        try:
            if self._id:
                result = mongo.db.kubernetes_deployments.update_one({'_id': self._id}, {'$set': deployment_data})
            else:
                result = mongo.db.kubernetes_deployments.insert_one(deployment_data)
                self._id = result.inserted_id
            logging.debug(f"Kubernetes deployment saved successfully: {self.name}")
        except Exception as e:
            logging.error(f"Error saving Kubernetes deployment: {str(e)}")

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            image=data['image'],
            replicas=data['replicas'],
            user_id=data['user_id'],
            created_at=data['created_at'],
            status=data['status'],
            _id=data.get('_id')
        )

    @classmethod
    def get_deployments_by_user_id(cls, user_id):
        deployments_data = mongo.db.kubernetes_deployments.find({'user_id': user_id})
        return [cls.from_dict(deployment_data) for deployment_data in deployments_data]