import logging
from flask import Blueprint, request, jsonify
from app.services.student import (
    get_all_students,
    get_student_by_id,
    create_student,
    update_student,
    delete_student
)

logger = logging.getLogger(__name__)

student_bp = Blueprint("student", __name__)


# POST /api/v1/students
@student_bp.route("/students", methods=["POST"])
def create():
    data = request.get_json()
    logger.info("POST /students called with data=%s", data)

    required_fields = ["name", "email", "age", "grade"]
    missing = [f for f in required_fields if f not in data]
    if missing:
        logger.warning("Missing fields: %s", missing)
        return jsonify({"error": f"Missing fields: {missing}"}), 400

    try:
        student = create_student(data)
        return jsonify(student.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 409
    except Exception as e:
        logger.error("Failed to create student: %s", str(e))
        return jsonify({"error": "Failed to create student"}), 500


# GET /api/v1/students
@student_bp.route("/students", methods=["GET"])
def get_all():
    logger.info("GET /students called")
    students = get_all_students()
    return jsonify([s.to_dict() for s in students]), 200


# GET /api/v1/students/<id>
@student_bp.route("/students/<int:student_id>", methods=["GET"])
def get_one(student_id):
    logger.info("GET /students/%s called", student_id)
    student = get_student_by_id(student_id)

    if not student:
        logger.warning("Student id=%s not found", student_id)
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student.to_dict()), 200


# PUT /api/v1/students/<id>
@student_bp.route("/students/<int:student_id>", methods=["PUT"])
def update(student_id):
    data = request.get_json()
    logger.info("PUT /students/%s called with data=%s", student_id, data)

    student = update_student(student_id, data)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student.to_dict()), 200


# DELETE /api/v1/students/<id>
@student_bp.route("/students/<int:student_id>", methods=["DELETE"])
def delete(student_id):
    logger.info("DELETE /students/%s called", student_id)
    success = delete_student(student_id)

    if not success:
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": f"Student {student_id} deleted successfully"}), 200
