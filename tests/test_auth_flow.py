import requests
import uuid

ROUTE = "http://localhost:5000"
MESSAGE = "View tickets here"


def test_register():
    with requests.Session() as session:
        # Register a new account with random username
        register_response = session.post(
            f"{ROUTE}/register",
            data={
                "email": f"test-{uuid.uuid4()}@company.com",
                "password": "Password123!",
                "confirm_password": "Password123!",
            },
        )

        # Confirm register request responded
        assert register_response

        # Request (auth protected) homepage
        home_response = session.get(f"{ROUTE}")

        # Confirm page successfully loaded and auth wall was not hit
        assert MESSAGE in home_response.text


def test_login():
    with requests.Session() as session:
        # Log in to default admin account
        login_response = session.post(
            f"{ROUTE}/login",
            data={
                "email": "admin@company.com",
                "password": "Password123!",
            },
        )

        # Confirm login request responded
        assert login_response

        # Request (auth protected) homepage
        home_response = session.get(f"{ROUTE}/")

        # Confirm page successfully loaded and auth wall was not hit
        assert MESSAGE in home_response.text


def test_logout():
    with requests.Session() as session:
        # Log in to default admin account
        register_response = session.post(
            f"{ROUTE}/login",
            data={
                "email": "admin@company.com",
                "password": "Password123!",
            },
        )

        # Confirm login request responded
        assert register_response

        # Log out
        logout_response = session.get(f"{ROUTE}/logout")

        # Confirm logout request responded
        assert logout_response

        # Request (auth protected) homepage
        home_response = session.get(f"{ROUTE}")

        # Confirm auth wall was hit and page did not load
        assert MESSAGE not in home_response.text
