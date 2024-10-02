import os
from urllib.parse import quote_plus

class Config:
    SECRET_KEY = os.urandom(32)
    
    # Escape username and password in MONGO_URI
    mongo_uri = os.environ.get('MONGO_URI')
    if mongo_uri:
        parts = mongo_uri.split('://')
        if len(parts) == 2:
            auth_parts = parts[1].split('@')
            if len(auth_parts) == 2:
                user_pass, host_part = auth_parts
                user, password = user_pass.split(':')
                escaped_user = quote_plus(user)
                escaped_password = quote_plus(password)
                MONGO_URI = f"{parts[0]}://{escaped_user}:{escaped_password}@{host_part}"
            else:
                MONGO_URI = mongo_uri
        else:
            MONGO_URI = mongo_uri
    else:
        # Fallback to a local MongoDB instance if MONGO_URI is not set
        MONGO_URI = "mongodb://localhost:27017/servafri_cloud"
    
    PAYSTACK_SECRET_KEY = os.environ.get('PAYSTACK_SECRET_KEY')
