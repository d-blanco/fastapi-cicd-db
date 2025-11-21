from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="Task Manager API",
    description="A simple task management API for CI/CD demonstration",
    version="1.0.0"
)

# In-memory storage (for demo purposes)
tasks = []
task_id_counter = 1


class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: Optional[str] = None
    completed: bool = False


@app.get("/")
def read_root():
    """Root endpoint returning API information"""
    return {
        "message": "Welcome to Task Manager API",
        "version": "1.0.0",
        "endpoints": ["/tasks", "/tasks/{task_id}", "/health"]
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/tasks", response_model=List[Task])
def get_tasks():
    """Get all tasks"""
    return tasks


@app.get("/tasks/{task_id}", response_model=Task)
def get_task(task_id: int):
    """Get a specific task by ID"""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: Task):
    """Create a new task"""
    global task_id_counter
    task_dict = task.dict()
    task_dict["id"] = task_id_counter
    task_id_counter += 1
    tasks.append(task_dict)
    return task_dict


@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task: Task):
    """Update an existing task"""
    for i, existing_task in enumerate(tasks):
        if existing_task["id"] == task_id:
            task_dict = task.dict()
            task_dict["id"] = task_id
            tasks[i] = task_dict
            return task_dict
    raise HTTPException(status_code=404, detail="Task not found")


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    """Delete a task"""
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return {"message": "Task deleted successfully"}
    raise HTTPException(status_code=404, detail="Task not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)