import pytest

from src.flask_orm.app import create_app
from src.flask_orm.extensions import db
from src.flask_orm.models import Assignment
from src.exercises import exercises as ex


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


def test_exercises_flow(app):
    with app.app_context():
        a1 = Assignment(title="Quiz 1", max_points=10)
        a2 = Assignment(title="HW 1", max_points=100)
        db.session.add_all([a1, a2])
        db.session.commit()

        s = ex.create_student("Ava", "ava@example.com")
        assert ex.find_student_by_email("ava@example.com").id == s.id
        assert ex.find_student_by_email("missing@example.com") is None

        ex.add_grade(s.id, a1.id, 9)    # 90%
        ex.add_grade(s.id, a2.id, 95)   # 95%
        assert round(ex.average_percent(s.id), 1) == 92.5

        with pytest.raises(ValueError):
            ex.add_grade(s.id, a1.id, 10)  # duplicate grade

        with pytest.raises(LookupError):
            ex.add_grade(999, a1.id, 1)

        with pytest.raises(LookupError):
            ex.add_grade(s.id, 999, 1)

        with pytest.raises(ValueError):
            ex.create_student("Other", "ava@example.com")  # duplicate email
