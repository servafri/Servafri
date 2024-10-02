import os

class Config:
    SECRET_KEY = os.urandom(32)
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://mayowa:semmat@cluster0.9a3xw.mongodb.net/servafri_cloud_db?retryWrites=true&w=majority')
    PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')
