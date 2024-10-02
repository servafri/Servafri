import os
from pymongo import MongoClient
from urllib.parse import quote_plus

def test_mongo_connection():
    mongo_uri = os.environ.get('MONGO_URI')
    if not mongo_uri:
        print("MONGO_URI environment variable is not set")
        return

    try:
        # Parse the URI and escape username and password
        parts = mongo_uri.split('://')
        if len(parts) == 2:
            auth_parts = parts[1].split('@')
            if len(auth_parts) == 2:
                user_pass, host_part = auth_parts
                user, password = user_pass.split(':')
                escaped_user = quote_plus(user)
                escaped_password = quote_plus(password)
                mongo_uri = f"{parts[0]}://{escaped_user}:{escaped_password}@{host_part}"

        print(f"Attempting to connect to MongoDB with URI: {mongo_uri[:10]}...{mongo_uri[-10:]}")
        client = MongoClient(mongo_uri)
        
        # Test the connection
        client.admin.command('ping')
        print("MongoDB connection successful!")
        
        # List available databases
        databases = client.list_database_names()
        print("Available databases:", databases)
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")

if __name__ == "__main__":
    test_mongo_connection()
