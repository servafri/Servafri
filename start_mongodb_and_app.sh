#!/bin/bash

# Start MongoDB
mongod --fork --logpath /tmp/mongod.log --dbpath /tmp/mongodb

# Wait for MongoDB to start
sleep 5

# Start the Flask application
python main.py
