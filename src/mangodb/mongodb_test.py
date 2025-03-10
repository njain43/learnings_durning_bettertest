from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Create a database
db = client["test_database"]

# Create a collection (table in RDBMS terms)
collection = db["users"]

# Insert a document (record)
user_data = {"name": "Nitesh", "age": 35, "city": "Pune"}
collection.insert_one(user_data)

# Fetch and print data
print("Inserted document:", collection.find_one({"name": "Nitesh"}))
