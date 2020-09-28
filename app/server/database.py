import urllib.parse as parser

from decouple import config

import motor.motor_asyncio as mongo_client
from bson.objectid import ObjectId

DB_USER = config("DB_USER")
DB_PASSWORD = parser.quote(config("DB_PASSWORD"))
DB_HOST = config("DB_HOST")
DB_PORT = config("DB_PORT")
DB_NAME = config("DB_NAME")

MONGO_DETAILS = f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/?authSource=admin"

client = mongo_client.AsyncIOMotorClient(MONGO_DETAILS, uuidRepresentation="standard")

database = client[DB_NAME]

student_collection = database.get_collection("students_collection")

'''
In the code above, we imported Motor, defined the connection details, and created a client via AsyncIOMotorClient.

We then referenced a database called students and a collection (akin to a table in a relational database) called students_collection.
Since these are just references and not actual I/O, neither requires an await expression.
When the first I/O operation is made, both the database and collection will be created if they don't already exist.
'''


# helpers
def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "GPA": student["gpa"],
    }


# List all students
async def retrive_students():
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students


# Add a new student
async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    return student_helper(new_student)


# Retrieve a student with a matching ID
async def retrive_student(id: str) -> dict:
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        return student_helper(student)


# Update a student with a matching ID
async def update_student(id: str, data: dict):
    if len(data) < 1:
        return False
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        updated_student = await student_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_student:
            return True
        return False


# Delete a student
async def delete_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})
    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True
