import os
from urllib.parse import urlparse

class Config:
    SECRET_KEY = os.urandom(32)
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/servafri')
    PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')

    @staticmethod
    def print_mongo_uri_info():
        mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/servafri')
        parsed_uri = urlparse(mongo_uri)
        print(f"MongoDB URI scheme: {parsed_uri.scheme}")
        print(f"MongoDB URI hostname: {parsed_uri.hostname}")
        print(f"MongoDB URI port: {parsed_uri.port}")
        print(f"MongoDB URI path: {parsed_uri.path}")

# Call the method to print MongoDB URI info
Config.print_mongo_uri_info()
