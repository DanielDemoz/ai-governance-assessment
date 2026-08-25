"""API tests for risk matrix."""

from app.models.question import Question


def test_risk_matrix_generated_on_calculate(client, db_session):
    create_resp = client.post("/assessments")
    public_id = create_resp.json()["public_id"]

    client.put(
        f"/assessments/{public_id}/profile",
        json={
            "organization": {"name": "Risk Org", "organization_type": "government"},
            "ai_system": {
                "name": "Risk AI",
                "processes_personal_info": True,
                "makes_decisions_about_people": True,
                "affects_public_services": True,
            },
        },
    )

    questions = db_session.query(Question).order_by(Question.id).all()
    responses = [{"question_id": q.id, "response_value": 2} for q in questions]
    client.put(f"/assessments/{public_id}/responses", json={"responses": responses})
    client.post(f"/assessments/{public_id}/calculate")

    matrix_resp = client.get(f"/assessments/{public_id}/risk-matrix")
    assert matrix_resp.status_code == 200
    data = matrix_resp.json()
    assert len(data["cells"]) == 25
    assert len(data["risks"]) > 0
    assert data["ai_system_risk_profile"]["level"] in {"low", "moderate", "high", "critical"}
    assert len(data["ai_system_risk_profile"]["factors"]) > 0


def test_add_and_delete_custom_risk(client, db_session):
    create_resp = client.post("/assessments")
    public_id = create_resp.json()["public_id"]

    client.put(
        f"/assessments/{public_id}/profile",
        json={
            "organization": {"name": "Custom Risk Org", "organization_type": "smb"},
            "ai_system": {"name": "Custom Risk AI"},
        },
    )

    questions = db_session.query(Question).order_by(Question.id).all()
    responses = [{"question_id": q.id, "response_value": 3} for q in questions]
    client.put(f"/assessments/{public_id}/responses", json={"responses": responses})
    client.post(f"/assessments/{public_id}/calculate")

    add_resp = client.post(
        f"/assessments/{public_id}/risks",
        json={
            "risk_type": "security_attack",
            "description": "External attack on model API.",
            "likelihood": 3,
            "impact": 4,
        },
    )
    assert add_resp.status_code == 201
    risk_id = add_resp.json()["id"]
    assert add_resp.json()["risk_score"] == 12
    assert add_resp.json()["classification"] == "high"

    delete_resp = client.delete(f"/assessments/{public_id}/risks/{risk_id}")
    assert delete_resp.status_code == 204
