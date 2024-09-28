import os
from urllib.parse import quote_plus

class Config:
    SECRET_KEY = os.urandom(32)
    MONGO_URI = os.environ.get('MONGO_URI')
    PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')

    @staticmethod
    def get_mongo_uri():
        mongo_uri = os.environ.get('MONGO_URI')
        if mongo_uri:
            # Ensure the URI is in the correct format for MongoDB Atlas
            if not mongo_uri.startswith('mongodb+srv://'):
                parts = mongo_uri.split('@')
                if len(parts) == 2:
                    userpass, host = parts
                    username, password = userpass.split('://')[1].split(':')
                    encoded_username = quote_plus(username)
                    encoded_password = quote_plus(password)
                    return f"mongodb+srv://{encoded_username}:{encoded_password}@{host}"
        return mongo_uri

    @staticmethod
    def print_mongo_uri_info():
        mongo_uri = Config.get_mongo_uri()
        print(f"Formatted MONGO_URI: {mongo_uri}")
        if mongo_uri:
            parts = mongo_uri.split('@')
            if len(parts) == 2:
                userpass, host = parts
                username = userpass.split('://')[1].split(':')[0]
                print(f"MongoDB URI username: {username}")
                print(f"MongoDB URI host: {host}")
            else:
                print("MONGO_URI is not in the expected format")
        else:
            print("MONGO_URI is not set")

# Call the method to print MongoDB URI info
Config.print_mongo_uri_info()
