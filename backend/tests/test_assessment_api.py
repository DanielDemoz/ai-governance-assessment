"""API integration tests for assessments."""

from app.models.question import Question


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_categories(client):
    response = client.get("/categories")
    assert response.status_code == 200
    categories = response.json()
    assert len(categories) == 9
    total_weight = sum(c["weight"] for c in categories)
    assert total_weight == 100.0
    assert sum(len(c["questions"]) for c in categories) == 67


def test_create_and_complete_assessment(client, db_session):
    create_resp = client.post("/assessments")
    assert create_resp.status_code == 201
    public_id = create_resp.json()["public_id"]

    profile_resp = client.put(
        f"/assessments/{public_id}/profile",
        json={
            "organization": {
                "name": "Test Org",
                "organization_type": "smb",
                "industry": "Technology",
                "country": "Canada",
                "assessment_owner": "Jane Doe",
                "assessment_date": "2026-08-24",
            },
            "ai_system": {
                "name": "Test AI System",
                "description": "A test system",
                "primary_purpose": "Testing",
                "technology_type": "machine_learning",
                "vendor_type": "in_house",
                "development_status": "testing",
                "deployment_status": "pilot",
                "processes_personal_info": True,
                "makes_decisions_about_people": True,
                "affects_education": True,
            },
        },
    )
    assert profile_resp.status_code == 200

    from app.models.question import Question

    questions = db_session.query(Question).order_by(Question.id).all()
    responses = [{"question_id": q.id, "response_value": 3} for q in questions]

    responses_resp = client.put(
        f"/assessments/{public_id}/responses",
        json={"responses": responses},
    )
    assert responses_resp.status_code == 200

    calc_resp = client.post(f"/assessments/{public_id}/calculate")
    assert calc_resp.status_code == 200
    result = calc_resp.json()
    assert result["overall_score"] == 75.0
    assert result["readiness_level"] == "advanced"
    assert len(result["category_scores"]) == 9
    assert result["calculation_trace"] is not None

    get_resp = client.get(f"/assessments/{public_id}/results")
    assert get_resp.status_code == 200
    assert get_resp.json()["overall_score"] == 75.0


def test_calculate_without_profile_fails(client):
    create_resp = client.post("/assessments")
    public_id = create_resp.json()["public_id"]
    calc_resp = client.post(f"/assessments/{public_id}/calculate")
    assert calc_resp.status_code == 400


def test_not_applicable_scoring(client, db_session):
    create_resp = client.post("/assessments")
    public_id = create_resp.json()["public_id"]

    client.put(
        f"/assessments/{public_id}/profile",
        json={
            "organization": {"name": "NA Test", "organization_type": "other"},
            "ai_system": {"name": "NA System"},
        },
    )

    from app.models.question import Question

    questions = db_session.query(Question).order_by(Question.id).all()
    responses = []
    for i, q in enumerate(questions):
        value = -1 if i == 0 else 4
        responses.append({"question_id": q.id, "response_value": value})

    client.put(f"/assessments/{public_id}/responses", json={"responses": responses})
    calc_resp = client.post(f"/assessments/{public_id}/calculate")
    assert calc_resp.status_code == 200
    assert calc_resp.json()["overall_score"] == 100.0
