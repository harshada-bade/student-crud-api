BASE_URL = "/api/v1/students"


def create_student_payload(
    name="Alice Smith",
    email="alice@example.com",
    age=20,
    grade="A"
):
    return {"name": name, "email": email, "age": age, "grade": grade}


# ── Healthcheck ──────────────────────────────────────────────────

class TestHealthCheck:
    def test_healthcheck(self, client):
        response = client.get("/healthcheck")
        assert response.status_code == 200
        assert response.get_json()["status"] == "ok"


# ── Create Student ───────────────────────────────────────────────

class TestCreateStudent:
    def test_create_student_success(self, client):
        response = client.post(
            BASE_URL,
            json=create_student_payload()
        )
        assert response.status_code == 201
        data = response.get_json()
        assert data["name"] == "Alice Smith"
        assert data["email"] == "alice@example.com"
        assert data["age"] == 20
        assert data["grade"] == "A"
        assert "id" in data

    def test_create_student_missing_fields(self, client):
        response = client.post(
            BASE_URL,
            json={"name": "Alice"}
        )
        assert response.status_code == 400
        assert "error" in response.get_json()

    def test_create_duplicate_email(self, client):
        client.post(BASE_URL, json=create_student_payload())
        response = client.post(BASE_URL, json=create_student_payload())
        assert response.status_code == 409
        assert "error" in response.get_json()


# ── Get All Students ─────────────────────────────────────────────

class TestGetAllStudents:
    def test_get_all_students_empty(self, client):
        response = client.get(BASE_URL)
        assert response.status_code == 200
        assert response.get_json() == []

    def test_get_all_students(self, client):
        client.post(BASE_URL, json=create_student_payload())
        response = client.get(BASE_URL)
        assert response.status_code == 200
        assert len(response.get_json()) == 1


# ── Get One Student ──────────────────────────────────────────────

class TestGetOneStudent:
    def test_get_student_success(self, client):
        created = client.post(
            BASE_URL,
            json=create_student_payload()
        ).get_json()
        response = client.get(f"{BASE_URL}/{created['id']}")
        assert response.status_code == 200
        assert response.get_json()["id"] == created["id"]

    def test_get_student_not_found(self, client):
        response = client.get(f"{BASE_URL}/999")
        assert response.status_code == 404
        assert "error" in response.get_json()


# ── Update Student ───────────────────────────────────────────────

class TestUpdateStudent:
    def test_update_student_success(self, client):
        created = client.post(
            BASE_URL,
            json=create_student_payload()
        ).get_json()
        response = client.put(
            f"{BASE_URL}/{created['id']}",
            json=create_student_payload(name="Alice Updated", age=21)
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["name"] == "Alice Updated"
        assert data["age"] == 21

    def test_update_student_not_found(self, client):
        response = client.put(
            f"{BASE_URL}/999",
            json=create_student_payload()
        )
        assert response.status_code == 404
        assert "error" in response.get_json()


# ── Delete Student ───────────────────────────────────────────────

class TestDeleteStudent:
    def test_delete_student_success(self, client):
        created = client.post(
            BASE_URL,
            json=create_student_payload()
        ).get_json()
        response = client.delete(f"{BASE_URL}/{created['id']}")
        assert response.status_code == 200
        assert "message" in response.get_json()

    def test_delete_student_not_found(self, client):
        response = client.delete(f"{BASE_URL}/999")
        assert response.status_code == 404
        assert "error" in response.get_json()

    def test_deleted_student_no_longer_exists(self, client):
        created = client.post(
            BASE_URL,
            json=create_student_payload()
        ).get_json()
        client.delete(f"{BASE_URL}/{created['id']}")
        response = client.get(f"{BASE_URL}/{created['id']}")
        assert response.status_code == 404