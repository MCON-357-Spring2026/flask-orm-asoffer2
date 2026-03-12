"""Exercises: ORM fundamentals.

Implement the TODO functions. Autograder will test them.
"""

from __future__ import annotations

from typing import Optional
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from src.exercises.extensions import db
from src.exercises.models import Student, Grade, Assignment


# ===== BASIC CRUD =====

def create_student(name: str, email: str) -> Student:
    """TODO: Create and commit a Student; handle duplicate email.

    If email is duplicate:
      - rollback
      - raise ValueError("duplicate email")
    """
    student = Student(name=name, email=email)
    db.session.add(student)
    try:
        db.session.commit()
    except Exception as ex:
        print(ex)
        raise ValueError("Duplicate email")
    return student


def find_student_by_email(email: str) -> Optional[Student]:
    """TODO: Return Student by email or None."""
    student = Student.query.filter_by(email=email).first()
    if not student:
        return None
    return student



def add_grade(student_id: int, assignment_id: int, score: int) -> Grade:
    """TODO: Add a Grade for the student+assignment and commit.

    If student doesn't exist: raise LookupError
    If assignment doesn't exist: raise LookupError
    If duplicate grade: raise ValueError("duplicate grade")
    """
    s = db.session.get(Student, student_id)
    if not s:
        raise LookupError("Student doesn't exist")
    assignment = db.session.get(Assignment, assignment_id)
    if not assignment:
        raise LookupError
    g = Grade(score= score, student=s, assignment=assignment)
    db.session.add(g)
    try:
      db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise ValueError("duplicate grade")
    return g





def average_percent(student_id: int) -> float:
    """TODO: Return student's average percent across assignments.

    percent per grade = score / assignment.max_points * 100

    If student doesn't exist: raise LookupError
    If student has no grades: return 0.0
    """
    student = db.session.get(Student, student_id)
    if not student:
        raise LookupError

    avg_expr = func.avg(Grade.score * 100.0 / Assignment.max_points)
    result = (
        db.session.query(avg_expr)
        .select_from(Grade)
        .join(Assignment, Grade.assignment_id == Assignment.id)
        .filter(Grade.student_id == student_id)
        .scalar()
    )
    return float(result) if result is not None else 0.0



# ===== QUERYING & FILTERING =====

def get_all_students() -> list[Student]:
    """TODO: Return all students in database, ordered by name."""
    students = Student.query.order_by(Student.name).all()
    return students


def get_assignment_by_title(title: str) -> Optional[Assignment]:
    """TODO: Return assignment by title or None."""
    assignment = Assignment.query.filter_by(title=title).first()
    if not assignment:
        return None
    return assignment


def get_student_grades(student_id: int) -> list[Grade]:
    """TODO: Return all grades for a student, ordered by assignment title.

    If student doesn't exist: raise LookupError
    """

    student = db.session.get(Student, student_id)
    if not student:
        raise LookupError
    return (
        Grade.query.join(Assignment)
        .filter(Grade.student_id == student_id)
        .order_by(Assignment.title)
        .all()
    )


def get_grades_for_assignment(assignment_id: int) -> list[Grade]:
    """TODO: Return all grades for an assignment, ordered by student name.

    If assignment doesn't exist: raise LookupError
    """
    assignment = db.session.get(Assignment, assignment_id)
    if not assignment:
        raise LookupError
    return (
        Grade.query.join(Student)
        .filter(Grade.assignment_id == assignment_id)
        .order_by(Student.name)
        .all()
    )


# ===== AGGREGATION =====

def total_student_grade_count() -> int:
    """TODO: Return total number of grades in database."""
    grades = Grade.query.all()
    num_grades = len(grades)
    return num_grades


def highest_score_on_assignment(assignment_id: int) -> Optional[int]:
    """TODO: Return the highest score on an assignment, or None if no grades.

    If assignment doesn't exist: raise LookupError
    """
    assignment = db.session.get(Assignment, assignment_id)
    if not assignment:
        raise LookupError
    result = db.session.query(func.max(Grade.score)).filter(Grade.assignment_id == assignment_id).scalar()
    return int(result) if result is not None else None


def class_average_percent() -> float:
    """TODO: Return average percent across all students and all assignments.

    percent per grade = score / assignment.max_points * 100
    Return average of all these percents.
    If no grades: return 0.0
    """
    avg_expr = func.avg(Grade.score * 100.0 / Assignment.max_points)
    result = (
        db.session.query(avg_expr)
        .select_from(Grade)
        .join(Assignment, Grade.assignment_id == Assignment.id)
        .scalar()
    )
    return float(result) if result is not None else 0.0


def student_grade_count(student_id: int) -> int:
    """TODO: Return number of grades for a student.

    If student doesn't exist: raise LookupError
    """
    s = db.session.get(Student, student_id)
    if not s:
        raise LookupError("Student doesn't exist")
    return len(s.grades)


# ===== UPDATING & DELETION =====

def update_student_email(student_id: int, new_email: str) -> Student:
    """TODO: Update a student's email and commit.

    If student doesn't exist: raise LookupError
    If new email is duplicate: rollback and raise ValueError("duplicate email")
    Return the updated student.
    """
    student = db.session.get(Student, student_id)
    if not student:
        raise LookupError("Student not found")
    student.email = new_email
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise ValueError("duplicate email")
    return student


def delete_student(student_id: int) -> None:
    """TODO: Delete a student and all their grades; commit.

    If student doesn't exist: raise LookupError
    """
    student = db.session.get(Student, student_id)
    if not student:
        raise LookupError("Student not found")
    db.session.delete(student)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
    return None


def delete_grade(grade_id: int) -> None:
    """TODO: Delete a grade by id; commit.

    If grade doesn't exist: raise LookupError
    """
    grade = db.session.get(Grade, grade_id)
    if not grade:
        raise LookupError("Grade not found")
    db.session.delete(grade)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
    return None


# ===== FILTERING & FILTERING WITH AGGREGATION =====

def students_with_average_above(threshold: float) -> list[Student]:
    """TODO: Return students whose average percent is above threshold.

    List should be ordered by average percent descending.
    percent per grade = score / assignment.max_points * 100
    """
    avg_percent = func.avg(Grade.score * 100.0 / Assignment.max_points)

    students = (
        db.session.query(Student)
        .join(Grade)
        .join(Assignment, Grade.assignment_id == Assignment.id)
        .group_by(Student.id)
        .having(avg_percent > threshold)
        .order_by(avg_percent.desc())
        .all()
    )
    return students


def assignments_without_grades() -> list[Assignment]:
    """TODO: Return assignments that have no grades yet, ordered by title."""
    assignments = (
        db.session.query(Assignment)
        .outerjoin(Grade)
        .filter(Grade.id == None)
        .order_by(Assignment.title)
        .all()
    )
    return assignments


def top_scorer_on_assignment(assignment_id: int) -> Optional[Student]:
    """TODO: Return the Student with the highest score on an assignment.

    If assignment doesn't exist: raise LookupError
    If no grades on assignment: return None
    If tie (multiple students with same high score): return any one
    """
    assignment = db.session.get(Assignment, assignment_id)
    if not assignment:
        raise LookupError("Assignment not found")

    max_score = db.session.query(func.max(Grade.score)).filter(Grade.assignment_id == assignment_id).scalar()

    if max_score is None:
        return None
    top_grade = db.session.query(Grade).filter(Grade.assignment_id == assignment_id, Grade.score == max_score).first()

    return top_grade.student

