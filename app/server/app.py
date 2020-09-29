from fastapi import FastAPI

from server.routes.student import router as StudentRouter

app = FastAPI()

app.include_router(StudentRouter, tags=["Student"], prefix="/student")


@app.get("/", tags=["Root"])
# Tags are identifiers used to group routes.
# Routes with the same tags are grouped into a section on the API documentation.
async def read_root():
    return {"message": "Welcome to this fantastic app!"}
