import pytest

from src.flask_orm.app import create_app
from src.flask_orm.extensions import db


@pytest.fixture()
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_assignments_crud(client):
    # Create
    res = client.post("/assignments", json={"title": "Quiz 1", "max_points": 10})
    assert res.status_code == 201
    aid = res.get_json()["id"]

    # List
    res = client.get("/assignments")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data, list) and len(data) == 1

    # Get
    res = client.get(f"/assignments/{aid}")
    assert res.status_code == 200
    assert res.get_json()["title"] == "Quiz 1"

    # Duplicate title
    res = client.post("/assignments", json={"title": "Quiz 1", "max_points": 10})
    assert res.status_code == 409


def test_students_and_grades_flow(client):
    # Create assignment first
    res = client.post("/assignments", json={"title": "HW 1", "max_points": 100})
    assert res.status_code == 201
    aid = res.get_json()["id"]

    # Create student
    res = client.post("/students", json={"name": "Ava", "email": "ava@example.com"})
    assert res.status_code == 201
    sid = res.get_json()["id"]

    # Add grade requires assignment_id
    res = client.post(f"/students/{sid}/grades", json={"assignment_id": aid, "score": 95})
    assert res.status_code == 201
    g = res.get_json()
    assert g["student_id"] == sid
    assert g["assignment_id"] == aid
    assert g["score"] == 95

    # Duplicate grade for same student+assignment -> 409
    res = client.post(f"/students/{sid}/grades", json={"assignment_id": aid, "score": 96})
    assert res.status_code == 409

    # List grades (includes assignment details)
    res = client.get(f"/students/{sid}/grades")
    assert res.status_code == 200
    grades = res.get_json()
    assert len(grades) == 1
    assert grades[0]["assignment"]["title"] == "HW 1"

    # Missing assignment
    res = client.post(f"/students/{sid}/grades", json={"assignment_id": 999, "score": 1})
    assert res.status_code == 404
