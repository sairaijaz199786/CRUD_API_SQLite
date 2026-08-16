from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Task Management API",
    description="A simple CRUD API for managing tasks",
    version="1.0.0"
)


# In-memory task data
tasks = [
    {"id": 1, "title": "Learn FastAPI", "done": False},
    {"id": 2, "title": "Build CRUD API", "done": False}
]


# Request model for creating a task
class TaskCreate(BaseModel):
    title: str
    done: bool = False


# Request model for updating a task
class TaskUpdate(BaseModel):
    title: str
    done: bool


# API information
@app.get("/")
def root():
    return {
        "message": "Task Management API",
        "version": "1.0.0"
    }


# Health check
@app.get("/health")
def health():
    return {"status": "ok"}


# Get all tasks
@app.get("/tasks")
def get_tasks():
    return tasks


# Get one task
@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = next(
        (task for task in tasks if task["id"] == task_id),
        None
    )

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# Create a new task
@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    new_id = max([item["id"] for item in tasks], default=0) + 1

    new_task = {
        "id": new_id,
        "title": task.title,
        "done": task.done
    }

    tasks.append(new_task)

    return new_task


# Update a task
@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: TaskUpdate):
    existing_task = next(
        (item for item in tasks if item["id"] == task_id),
        None
    )

    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    existing_task["title"] = task.title
    existing_task["done"] = task.done

    return existing_task


# Delete a task
@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    existing_task = next(
        (item for item in tasks if item["id"] == task_id),
        None
    )

    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    tasks.remove(existing_task)