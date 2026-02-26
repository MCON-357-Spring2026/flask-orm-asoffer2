import pytest

from src.flask_orm.app import create_app
from src.flask_orm.extensions import db
from src.flask_orm.models import Student
from src.homework import homework as hw


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


def test_homework_flow(app):
    with app.app_context():
        ava = Student(name="Ava", email="ava@example.com")
        noah = Student(name="Noah", email="noah@example.com")
        db.session.add_all([ava, noah])
        db.session.commit()

        a1 = hw.record_assignment("Quiz 1", 10)
        a2 = hw.record_assignment("HW 1", 100)

        hw.record_grade_for_assignment(ava.id, a1.id, 9)   # 90.0
        hw.record_grade_for_assignment(ava.id, a2.id, 95)  # 95.0
        hw.record_grade_for_assignment(noah.id, a1.id, 7)  # 70.0

        with pytest.raises(ValueError):
            hw.record_grade_for_assignment(ava.id, a1.id, 10)  # duplicate grade

        rep = hw.student_report(ava.id)
        percents = sorted([r["percent"] for r in rep])
        assert percents == [90.0, 95.0]

        board = hw.leaderboard()
        assert board[0]["student"] == "Ava"
        assert round(board[0]["avg_percent"], 1) == 92.5

        with pytest.raises(ValueError):
            hw.record_assignment("Bad", 0)

        with pytest.raises(ValueError):
            hw.record_assignment("Quiz 1", 10)  # duplicate title

        with pytest.raises(LookupError):
            hw.record_grade_for_assignment(999, a1.id, 1)

        with pytest.raises(LookupError):
            hw.record_grade_for_assignment(ava.id, 999, 1)
