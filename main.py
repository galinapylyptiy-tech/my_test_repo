from fastapi import FastAPI, HTTPException
from typing import List
from models import User, Gender, Role
from uuid import uuid4, UUID

app = FastAPI()
db: List[User] = [
    User(
        id=uuid4(),
        first_name="John",
        last_name="Doe",
        middle_name=None,
        gender=Gender.MALE,
        roles=[Role.ADMIN, Role.USER]
    ),
    User(
        id=uuid4(),
        first_name="Anna",
        last_name="Smith",
        middle_name="Maria",
        gender=Gender.FEMALE,
        roles=[Role.USER]
    ),
    User(
        id=uuid4(),
        first_name="Ivan",
        last_name="Petrov",
        middle_name="Sergeevich",
        gender=Gender.MALE,
        roles=[Role.STUDENT]
    ),
    User(
        id=uuid4(),
        first_name="Elena",
        last_name="Kuznetsova",
        middle_name=None,
        gender=Gender.FEMALE,
        roles=[Role.USER, Role.STUDENT]
    )
]


@app.get("/")
async def hello():
    return {"Hello": "Galina"}


@app.get("/api/v1/users")
async def get_users():
    return db


@app.post("/api/v1/users")
async def create_user(user:User):
    db.append(user)  # Add the new user to the database
    return {"id": user.id}


@app.delete("/api/v1/users/{user_id}")
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"message": f"User with ID {user_id} was deleted successfully"}
    raise HTTPException(status_code=404, detail=f"User with ID {user_id} is not found")


@app.put("/api/v1/users/{user_id}")
async def update_user(user_id:UUID, updated_user: User):
    for index, user in enumerate(db):
        if user.id == user_id:
            db[index] = updated_user  # Update the user in the database
            return {"message": f"User with ID {user_id} was updated successfully"}
    raise HTTPException(status_code=404, detail=f"User with ID {user_id} is not found")