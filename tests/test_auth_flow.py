import requests
import uuid


def test_register():
    with requests.Session() as session:
        # Register a new account with random username
        register_response = session.post(
            "http://localhost:5000/register",
            data={
                "email": f"test-{uuid.uuid4()}@company.com",
                "password": "Password123!",
                "confirm_password": "Password123!",
            },
        )

        # Confirm register request responded
        assert register_response

        # Request (auth protected) homepage
        home_response = session.get("http://localhost:5000")

        # Confirm page successfully loaded and auth wall was not hit
        assert "View tickets here" in home_response.text


def test_login():
    with requests.Session() as session:
        # Log in to default admin account
        login_response = session.post(
            "http://localhost:5000/login",
            data={
                "email": "admin@company.com",
                "password": "Password123!",
            },
        )

        # Confirm login request responded
        assert login_response

        # Request (auth protected) homepage
        home_response = session.get("http://localhost:5000")

        # Confirm page successfully loaded and auth wall was not hit
        assert "View tickets here" in home_response.text


def test_logout():
    with requests.Session() as session:
        # Log in to default admin account
        register_response = session.post(
            "http://localhost:5000/login",
            data={
                "email": "admin@company.com",
                "password": "Password123!",
            },
        )

        # Confirm login request responded
        assert register_response

        # Log out
        logout_response = session.get("http://localhost:5000/logout")

        # Confirm logout request responded
        assert logout_response

        # Request (auth protected) homepage
        home_response = session.get("http://localhost:5000")

        # Confirm auth wall was hit and page did not load
        assert "View tickets here" not in home_response.text
