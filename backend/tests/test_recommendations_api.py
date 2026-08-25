"""API tests for recommendations and roadmap."""

from app.models.question import Question


def test_recommendations_generated_on_calculate(client, db_session):
    create_resp = client.post("/assessments")
    public_id = create_resp.json()["public_id"]

    client.put(
        f"/assessments/{public_id}/profile",
        json={
            "organization": {"name": "Rec Test Org", "organization_type": "smb"},
            "ai_system": {
                "name": "Rec Test AI",
                "makes_decisions_about_people": True,
            },
        },
    )

    questions = db_session.query(Question).order_by(Question.id).all()
    responses = [{"question_id": q.id, "response_value": 0} for q in questions]
    client.put(f"/assessments/{public_id}/responses", json={"responses": responses})
    client.post(f"/assessments/{public_id}/calculate")

    rec_resp = client.get(f"/assessments/{public_id}/recommendations")
    assert rec_resp.status_code == 200
    data = rec_resp.json()
    assert data["total"] > 0
    assert len(data["recommendations"]) == data["total"]

    first = data["recommendations"][0]
    assert "priority" in first
    assert "recommendation" in first
    assert "why_it_matters" in first
    assert "suggested_action" in first
    assert "responsible_role" in first
    assert "suggested_timeframe" in first


def test_roadmap_generated_from_recommendations(client, db_session):
    create_resp = client.post("/assessments")
    public_id = create_resp.json()["public_id"]

    client.put(
        f"/assessments/{public_id}/profile",
        json={
            "organization": {"name": "Roadmap Org", "organization_type": "education"},
            "ai_system": {"name": "Roadmap AI", "affects_education": True},
        },
    )

    questions = db_session.query(Question).order_by(Question.id).all()
    responses = []
    for i, q in enumerate(questions):
        value = 0 if i < 5 else 4
        responses.append({"question_id": q.id, "response_value": value})

    client.put(f"/assessments/{public_id}/responses", json={"responses": responses})
    client.post(f"/assessments/{public_id}/calculate")

    roadmap_resp = client.get(f"/assessments/{public_id}/roadmap")
    assert roadmap_resp.status_code == 200
    phases = roadmap_resp.json()["phases"]
    assert len(phases) >= 1
    assert phases[0]["recommendations"]


def test_fully_compliant_assessment_has_no_recommendations(client, db_session):
    create_resp = client.post("/assessments")
    public_id = create_resp.json()["public_id"]

    client.put(
        f"/assessments/{public_id}/profile",
        json={
            "organization": {"name": "Perfect Org", "organization_type": "other"},
            "ai_system": {"name": "Perfect AI"},
        },
    )

    questions = db_session.query(Question).order_by(Question.id).all()
    responses = [{"question_id": q.id, "response_value": 4} for q in questions]
    client.put(f"/assessments/{public_id}/responses", json={"responses": responses})
    client.post(f"/assessments/{public_id}/calculate")

    rec_resp = client.get(f"/assessments/{public_id}/recommendations")
    assert rec_resp.status_code == 200
    assert rec_resp.json()["total"] == 0
