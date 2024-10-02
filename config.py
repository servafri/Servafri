import os

class Config:
    SECRET_KEY = os.urandom(32)
    MONGO_URI = 'mongodb+srv://mayowa:semmat@cluster0.9a3xw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
    PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')
