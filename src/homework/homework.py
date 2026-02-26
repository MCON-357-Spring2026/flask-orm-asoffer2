"""Homework: ORM gradebook.

Implement TODOs:
  - record_assignment
  - record_grade_for_assignment
  - student_report
  - leaderboard

Schema is already defined in src/flask_orm/models.py:
  - Student
  - Assignment (with Assignment.grades)
  - Grade with UniqueConstraint(student_id, assignment_id)
"""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from src.flask_orm.extensions import db
from src.flask_orm.models import Student, Grade, Assignment


def record_assignment(title: str, max_points: int) -> Assignment:
    """TODO: Create and commit an Assignment.

    If title duplicate: raise ValueError("duplicate title")
    If max_points <= 0: raise ValueError
    """
    raise NotImplementedError


def record_grade_for_assignment(student_id: int, assignment_id: int, score: int) -> Grade:
    """TODO: Record grade linked to student + assignment.

    If student missing: raise LookupError
    If assignment missing: raise LookupError
    If score < 0: raise ValueError
    If duplicate grade: raise ValueError("duplicate grade")
    """
    raise NotImplementedError


def student_report(student_id: int) -> list[dict]:
    """TODO: Return report rows:
      { "assignment": title, "score": score, "max_points": max_points, "percent": rounded_1_decimal }
    """
    raise NotImplementedError


def leaderboard() -> list[dict]:
    """TODO: Return rows sorted by avg_percent desc:
      { "student": name, "avg_percent": value }
    Students with no grades should appear with 0.0 at the bottom.
    """
    raise NotImplementedError
