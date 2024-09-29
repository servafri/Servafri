import os

class Config:
    SECRET_KEY = os.urandom(32)
    MONGO_URI = 'mongodb+srv://servafri:%40Semmatinc7771@c.g2ox4.mongodb.net'
    PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')

    @staticmethod
    def print_mongo_uri_info():
        print(f"MONGO_URI: {Config.MONGO_URI}")

# Call the method to print MongoDB URI info
Config.print_mongo_uri_info()
