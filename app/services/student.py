import logging
from app import db
from app.models.student import Student

logger = logging.getLogger(__name__)


def get_all_students():
    logger.info("Fetching all students")
    return Student.query.all()


def get_student_by_id(student_id):
    logger.info("Fetching student with id=%s", student_id)
    return Student.query.get(student_id)


def create_student(data):
    logger.info("Creating new student with email=%s", data.get("email"))

    student = Student(
        name=data["name"],
        email=data["email"],
        age=data["age"],
        grade=data["grade"]
    )
    db.session.add(student)
    db.session.commit()

    logger.info("Student created successfully with id=%s", student.id)
    return student


def update_student(student_id, data):
    logger.info("Updating student with id=%s", student_id)

    student = Student.query.get(student_id)
    if not student:
        logger.warning("Student with id=%s not found", student_id)
        return None

    student.name = data.get("name", student.name)
    student.email = data.get("email", student.email)
    student.age = data.get("age", student.age)
    student.grade = data.get("grade", student.grade)

    db.session.commit()
    logger.info("Student with id=%s updated successfully", student_id)
    return student


def delete_student(student_id):
    logger.info("Deleting student with id=%s", student_id)

    student = Student.query.get(student_id)
    if not student:
        logger.warning("Student with id=%s not found", student_id)
        return False

    db.session.delete(student)
    db.session.commit()
    logger.info("Student with id=%s deleted successfully", student_id)
    return True