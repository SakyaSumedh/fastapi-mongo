from fastapi import FastAPI

app = FastAPI()

@app.get("/", tags=["Root"])
# Tags are identifiers used to group routes. Routes with the same tags are grouped into a section on the API documentation.
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
