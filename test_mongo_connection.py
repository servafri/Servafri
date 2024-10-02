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
        
        # List all collections in the database
        db = client.get_default_database()
        collections = db.list_collection_names()
        print("Available collections:", collections)
        
        # Check if 'users' collection exists and count documents
        if 'users' in collections:
            users_count = db.users.count_documents({})
            print(f"Number of documents in 'users' collection: {users_count}")
            
            # Print the first user document (without sensitive information)
            first_user = db.users.find_one({}, {'password_hash': 0})
            if first_user:
                print("First user document (excluding password):")
                print(first_user)
            else:
                print("No user documents found.")
        else:
            print("'users' collection does not exist.")
        
    except Exception as e:
        print(f"Error connecting to MongoDB: {str(e)}")

if __name__ == "__main__":
    test_mongo_connection()
