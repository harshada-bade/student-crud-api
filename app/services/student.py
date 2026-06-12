import logging
from app import db
from app.models.student import Student
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)


def get_all_students():
    logger.info("Fetching all students")
    try:
        students = Student.query.all()
        logger.info("Found %d students", len(students))
        return students
    except Exception as e:
        logger.error("Error fetching all students: %s", str(e))
        raise


def get_student_by_id(student_id):
    logger.info("Fetching student with id=%s", student_id)
    return db.session.get(Student, student_id)


def create_student(data):
    logger.info("Creating new student")
    try:
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
    except IntegrityError:
        db.session.rollback()
        logger.warning("Duplicate email: %s", data.get("email"))
        raise ValueError("A student with this email already exists")
    except Exception as e:
        db.session.rollback()
        logger.error("Error creating student: %s", str(e))
        raise


def update_student(student_id, data):
    logger.info("Updating student with id=%s", student_id)

    student = db.session.get(Student, student_id)
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

    student = db.session.get(Student, student_id)
    if not student:
        logger.warning("Student with id=%s not found", student_id)
        return False

    db.session.delete(student)
    db.session.commit()
    logger.info("Student with id=%s deleted successfully", student_id)
    return True