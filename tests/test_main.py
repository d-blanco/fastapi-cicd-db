from app.main import app, tasks
from fastapi.testclient import TestClient

client = TestClient(app)


def setup_function():
    """Clear tasks before each test"""
    tasks.clear()


def test_read_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to Task Manager API"


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_task():
    """Test creating a new task"""
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False,
    }
    response = client.post("/tasks", json=task_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["id"] is not None


def test_get_tasks():
    """Test getting all tasks"""
    # Create a task first
    client.post("/tasks", json={"title": "Task 1", "completed": False})
    client.post("/tasks", json={"title": "Task 2", "completed": True})

    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task_by_id():
    """Test getting a specific task"""
    # Create a task
    create_response = client.post(
        "/tasks", json={"title": "Specific Task", "completed": False}
    )
    task_id = create_response.json()["id"]

    # Get the task
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Specific Task"


def test_get_nonexistent_task():
    """Test getting a task that doesn't exist"""
    response = client.get("/tasks/999")
    assert response.status_code == 404


def test_update_task():
    """Test updating a task"""
    # Create a task
    create_response = client.post(
        "/tasks", json={"title": "Old Title", "completed": False}
    )
    task_id = create_response.json()["id"]

    # Update the task
    update_data = {"title": "New Title", "completed": True}
    response = client.put(f"/tasks/{task_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"
    assert response.json()["completed"] is True


def test_delete_task():
    """Test deleting a task"""
    # Create a task
    create_response = client.post(
        "/tasks", json={"title": "Task to Delete", "completed": False}
    )
    task_id = create_response.json()["id"]

    # Delete the task
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200

    # Verify it's deleted
    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404
