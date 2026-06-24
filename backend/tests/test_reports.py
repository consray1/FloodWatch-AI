import pytest


def test_create_report(client, auth_token):
    response = client.post(
        "/api/v1/reports",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "source": "web",
            "raw_text": "Heavy flooding reported on Mombasa Road. Water levels rising rapidly.",
            "location_lat": -1.2921,
            "location_lng": 36.8219,
            "location_name": "Mombasa Road, Nairobi"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["source"] == "web"
    assert data["status"] == "pending"


def test_create_report_minimal_text(client, auth_token):
    response = client.post(
        "/api/v1/reports",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "source": "web",
            "raw_text": "Short"
        }
    )
    assert response.status_code == 422


def test_list_reports(client, auth_token):
    client.post(
        "/api/v1/reports",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "source": "web",
            "raw_text": "Test report for listing. This should be long enough."
        }
    )

    response = client.get(
        "/api/v1/reports",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "pagination" in data


def test_list_reports_with_filter(client, auth_token):
    client.post(
        "/api/v1/reports",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "source": "web",
            "raw_text": "Web source report that should appear in the filter."
        }
    )

    response = client.get(
        "/api/v1/reports?source=web",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    for report in data["data"]:
        assert report["source"] == "web"


def test_get_single_report(client, auth_token):
    create_response = client.post(
        "/api/v1/reports",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "source": "web",
            "raw_text": "Report for single retrieval test. This is a longer text to pass validation."
        }
    )
    report_id = create_response.json()["id"]

    response = client.get(
        f"/api/v1/reports/{report_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == report_id


def test_get_nonexistent_report(client, auth_token):
    response = client.get(
        "/api/v1/reports/00000000-0000-0000-0000-000000000000",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 404


def test_update_report(client, auth_token):
    create_response = client.post(
        "/api/v1/reports",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "source": "web",
            "raw_text": "Original report text that will be updated. This needs more characters."
        }
    )
    report_id = create_response.json()["id"]

    response = client.put(
        f"/api/v1/reports/{report_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "raw_text": "Updated report text with new information."
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["raw_text"] == "Updated report text with new information."


def test_delete_report(client, auth_token):
    create_response = client.post(
        "/api/v1/reports",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "source": "web",
            "raw_text": "Report that will be deleted. This needs more characters to pass validation."
        }
    )
    report_id = create_response.json()["id"]

    response = client.delete(
        f"/api/v1/reports/{report_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 204

    get_response = client.get(
        f"/api/v1/reports/{report_id}",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert get_response.status_code == 404