import motor.motor_asyncio as mongo_client

MONGO_DETAILS = "mongodb://root:p%40ssw0rd@localhost:27017/?authSource=admin"

client = mongo_client.AsyncIOMotorClient(MONGO_DETAILS)

database = client.students

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