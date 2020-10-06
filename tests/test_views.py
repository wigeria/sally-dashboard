""" Contains tests for the views declared in the Backend.app instance """


def test_running(client, user):
    """ Tests that the test-api returns a successful response """
    r = client.get("/api/")
    assert r.status_code == 200
    assert "status" in r.json and r.json["status"] == "Running"


def test_login(client, db, user):
    """ Tests that the login api returns a 200 only for valid credentials """
    # Testing an invalid login
    data = {
        "email": "Test",
        "password": "test"
    }
    r = client.post("/api/login/", json=data)
    assert r.status_code == 400

    data = {
        "email": "test@email.com",
        "password": "test"
    }
    r = client.post("/api/login/", json=data)
    assert r.status_code == 401

    data["password"] = "testpass"
    r = client.post("/api/login/", json=data)
    assert r.status_code == 200
    assert r.json["user"]["id"] == str(user.id)
