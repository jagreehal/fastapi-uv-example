import asyncio
import os
from contextlib import asynccontextmanager
from typing import Dict, List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from loguru import logger
from pydantic import BaseModel
from scalar_fastapi import get_scalar_api_reference

load_dotenv()

port = os.getenv("PORT", "default_port_number")

# Loguru configuration
logger.add(
    sink=lambda msg: print(msg, end=""),
    format="{time} | {level} | {message}",
    level="INFO",
    serialize=True,
)


class Todo(BaseModel):
    name: str
    completed: bool = False


# Mock database
todos: Dict[str, Todo] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application has started", port=port)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )


@app.get("/todo", response_model=List[Todo])
async def read_todos():
    logger.info("Reading all todos")
    return list(todos.values())


@app.post("/todo", response_model=Todo)
async def create_todo(todo: Todo):
    await asyncio.sleep(1)
    todo_id = str(len(todos) + 1)
    todos[todo_id] = todo
    logger.info("Todo created", todo_id=todo_id, todo=todo.model_dump())
    return todo


@app.get("/todo/{todo_id}", response_model=Todo)
async def read_todo(todo_id: str):
    logger.info("Reading a todo", todo_id=todo_id)
    todo = todos.get(todo_id)
    if todo is None:
        logger.error("Todo not found", todo_id=todo_id)
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.put("/todo/{todo_id}", response_model=Todo)
async def update_todo(todo_id: str, updated_todo: Todo):
    logger.info("Updating todo", todo_id=todo_id)
    if todo_id not in todos:
        logger.error("Todo not found for update", todo_id=todo_id)
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[todo_id] = updated_todo
    return updated_todo


@app.delete("/todo/{todo_id}", response_model=Todo)
async def delete_todo(todo_id: str):
    logger.info("Deleting todo", todo_id=todo_id)
    if todo_id not in todos:
        logger.error("Todo not found for deletion", todo_id=todo_id)
        raise HTTPException(status_code=404, detail="Todo not found")
    return todos.pop(todo_id)
