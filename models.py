"""Application Models"""
import json
import os
import bson
from pymongo import MongoClient
from bson.json_util import dumps

db = MongoClient('mongodb://mongo/new_users').db


class User:
    """User Model"""
    def __init__(self):
        return

    def create(self, name="", email="", age="", dob="", phone=""):
        """Create a new user"""
        user = self.get_by_email(email)
        print("user here in create : ",user)
        if user:
            return
        elif name and email:
            try:
                db.newusers.insert(
                    {
                        "name": name,
                        "email": email,
                        "age": age,
                        "dob": dob,
                        "phone": phone,
                        "active": True
                    }
                )

                user = self.get_by_email(email)
                return {
                    "data": json.loads(dumps(user))
                }
            except Exception as e:
                return {
                       "error": "Something went wrong",
                       "message": str(e)
                   }, 500
        else:
            return "not_found"

    #GET ALL USERS FROM DATABASE
    def get_all(self):
        """Get all users"""
        users = db.newusers.find({"active": True})
        response = dumps(users)
        return response

    # GET USERS FROM DATABASE USING USER ID
    def get_by_id(self, _id):
        """Get a user by id"""
        user = db.newusers.find_one({"_id": bson.ObjectId(_id), "active": True})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user

    # GET USERS FROM DATABASE USING USER EMAIL
    def get_by_email(self, email):
        """Get a user by email"""
        user = db.newusers.find_one({"email": email})
        if not user:
            return
        user["_id"] = str(user["_id"])
        return user

    # UPDATE USERS IN DATABASE
    def update(self, user_id, name="", email="", age="",dob="",phone=""):
        """Update a user"""
        data = {}
        if name and email and age and dob and phone:
            data["name"] = name
            data["email"] = email
            data["age"] = age
            data["dob"] = dob
            data["phone"] = phone
        db.newusers.update_one(
            {"_id": bson.ObjectId(user_id)},
            {
                "$set": data
            }
        )
        user = self.get_by_id(user_id)
        return user

    # DELETE USER FROM DATABASE USING USER ID
    def delete(self, user_id):
        """Delete a user"""
        user = db.newusers.delete_one({"_id": bson.ObjectId(user_id)})
        return user
