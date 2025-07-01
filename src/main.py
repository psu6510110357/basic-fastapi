# main.py

from enum import Enum
from typing import List
from fastapi import Depends, FastAPI, Query, status
import os
from dotenv import load_dotenv
from sqlmodel import Field, SQLModel, Session, create_engine, select

load_dotenv()


class Item(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


database_url = os.getenv("DATABASE_URL")
if database_url is None:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(database_url, echo=True)

SQLModel.metadata.create_all(engine)


app = FastAPI()


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item, session: Session = Depends(get_session)):
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.get("/items/", response_model=List[Item])
async def read_items(
    session: Session = Depends(get_session),
    offset: int = Query(default=0),  # Using Query for query parameters
    limit: int = Query(default=100, le=100),  # Using Query for query parameters
):
    items = session.exec(select(Item).offset(offset).limit(limit)).all()
    return items


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {
        "item_id": item_id,
        "item_name": item.name,
        "item_description": item.description,
    }


@app.patch("/items/{item_id}")
def partial_update_item(item_id: int, item: Item):
    return {
        "item_id": item_id,
        "item_name": item.name,
        "item_description": item.description,
    }


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted"}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}
