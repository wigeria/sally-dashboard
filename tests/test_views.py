""" Contains tests for the views declared in the Backend.app instance """

from backend.database.models import Bot, Job
from backend.utils import bot_utils
from datetime import datetime
from io import BytesIO


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
    assert r.json["user"]["id"] == str(user.id), r.json


def test_bot_creation(client, db, user):
    """ Tests that the bot creation endpoint is behind auth permissions
        and the bot-file gets uploaded to s3 correctly
    """
    ctype = "multipart/form-data"
    content = b"""
        steps:
          - title: Step 1
            action: navigate
    """
    data = {
        "name": "Test Bot",
        "file": (BytesIO(content), "file.yaml")
    }
    url = "/api/bots/"
    # Missing Auth; 401
    r = client.post(url, data=data)
    assert r.status_code == 401

    # Missing title in bot; 400
    headers = {"Authorization": f"Token {user.generate_jwt().decode()}"}
    data["file"] = (BytesIO(content), "file.yaml")
    r = client.post(url, data=data, headers=headers)
    assert r.status_code == 400

    # Valid bot + auth; 201
    content = b"""
        title: Bot
        steps:
          - title: Step 1
            action: navigate
            url: http://google.com
    """
    data["file"] = (BytesIO(content), "file.yaml")
    r = client.post(url, data=data, headers=headers)
    assert r.status_code == 201
    bot = Bot.query.filter(Bot.id == r.json["id"]).first()
    bot_utils.delete_bot(bot.s3_path)
    db.session.delete(bot)
    db.session.commit()

def test_bot_list(client, db, user):
    """ Tests that the bots can be listed correctly """
    bot = Bot(name="TestBot")
    db.session.add(bot)
    db.session.commit()
    url = "/api/bots/"

    # Missing auth; 401
    r = client.get(url)
    assert r.status_code == 401

    headers = {"Authorization": f"Token {user.generate_jwt().decode()}"}
    r = client.get(url, headers=headers)
    assert r.status_code == 200
    db.session.delete(bot)
    db.session.commit()


def test_bot_delete(client, db, user):
    """ Tests that the bots can be deleted correctly """
    bot = Bot(name="TestBot")
    db.session.add(bot)
    db.session.commit()
    bot_utils.upload_bot(b"Test File", bot.s3_path)
    url = f"/api/bots/{bot.id}/"

    # Missing auth; 401
    r = client.delete(url)
    assert r.status_code == 401

    headers = {"Authorization": f"Token {user.generate_jwt().decode()}"}
    r = client.delete(url, headers=headers)
    assert r.status_code == 200


def test_job_start(client, db, user):
    """ Tests that a job can be created (started) successfully against a
        valid bot
    """
    content = b"""
        title: Bot
        steps:
          - title: Step 1
            action: navigate
            url: http://google.com
    """
    bot = Bot(name="TestBot")
    db.session.add(bot)
    db.session.commit()
    bot_utils.upload_bot(content, bot.s3_path)
    url = "/api/jobs/"
    headers = {"Authorization": f"Token {user.generate_jwt().decode()}"}

    # Missing auth; 401
    r = client.post(url, json={})
    assert r.status_code == 401

    # Missing runtime_data; 400
    r = client.post(url, json={"bot_id": "111"}, headers=headers)
    assert r.status_code == 400

    # Invalid Bot ID; 404
    r = client.post(url, json={"bot_id": "111", "runtime_data": {}},
                    headers=headers)
    assert r.status_code == 404

    # Valid bot-id + auth; 200
    r = client.post(url, json={"bot_id": str(bot.id), "runtime_data": {}},
                    headers=headers)
    assert r.status_code == 200

    # bot_utils.delete_bot(bot.s3_path)
    Job.query.delete()
    db.session.delete(bot)
    db.session.commit()


def test_jobs_list(client, db, user):
    """ Tests that the list of jobs can be retrieved through a status
        filter
    """
    bot = Bot(name="TestBot")
    running_job = Job(bot=bot, start_time=datetime.utcnow())
    finished_job = Job(
        bot=bot, start_time=datetime.utcnow(),
        finish_time=datetime.utcnow())
    bot.jobs = [running_job, finished_job]
    db.session.add(bot)
    db.session.commit()

    url = "/api/jobs/"
    headers = {"Authorization": f"Token {user.generate_jwt().decode()}"}

    # Unauthenticated request; 401
    r = client.get(url)
    assert r.status_code == 401

    # All jobs; 2 jobs returned
    r = client.get(url, headers=headers)
    assert r.status_code == 200
    assert len(r.json) == 2

    # Running jobs; 1 job returned
    r = client.get(url+"?status=0", headers=headers)
    assert r.status_code == 200
    assert len(r.json) == 1
