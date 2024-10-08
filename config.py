import os

class Config:
    SECRET_KEY = os.urandom(32)
    MONGO_URI = os.environ.get('MONGO_URI')
    PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')
