import requests
import uuid

ROUTE = "http://localhost:5000"


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
        assert "View tickets here" in home_response.text


def test_register_weak_password():
    with requests.Session() as session:
        # Register a new account with weak password
        register_response = session.post(
            f"{ROUTE}/register",
            data={
                "email": f"test-{uuid.uuid4()}@company.com",
                "password": "password",
                "confirm_password": "password",
            },
        )

        # Confirm register request responded
        assert register_response

        # Confirm register failed with correct reason
        assert "Stronger password required" in register_response.text


def test_register_non_matching_password():
    with requests.Session() as session:
        # Register a new account with non-matching confirmation password
        register_response = session.post(
            f"{ROUTE}/register",
            data={
                "email": f"test-{uuid.uuid4()}@company.com",
                "password": "Password123!",
                "confirm_password": "Password123!!",
            },
        )

        # Confirm register request responded
        assert register_response

        # Confirm register failed with correct reason
        assert "Passwords do not match" in register_response.text


def test_register_existing_email():
    with requests.Session() as session:
        # Register a new account with existing email
        register_response = session.post(
            f"{ROUTE}/register",
            data={
                "email": "admin@company.com",
                "password": "Password123!",
                "confirm_password": "Password123!",
            },
        )

        # Confirm register request responded
        assert register_response

        # Confirm register failed with correct reason
        assert "Invalid email" in register_response.text


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
        assert "View tickets here" in home_response.text


def test_login_invalid_password():
    with requests.Session() as session:
        # Log in to default admin account
        login_response = session.post(
            f"{ROUTE}/login",
            data={
                "email": "admin@company.com",
                "password": "wrongpassword",
            },
        )

        # Confirm login request responded
        assert login_response

        # Confirm login failed with correct reason
        assert "Incorrect login details" in login_response.text


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
        assert "View tickets here" not in home_response.text


def test_login_wrong_password():
    email = f"test-{uuid.uuid4()}@company.com"

    # Register a new account with random username
    register_response = requests.post(
        f"{ROUTE}/register",
        data={
            "email": email,
            "password": "Password123!",
            "confirm_password": "Password123!",
        },
    )

    # Confirm register request responded
    assert register_response

    # Attempt to log in with incorrect password
    login_response = requests.post(
        f"{ROUTE}/login",
        data={
            "email": email,
            "password": "incorrect",
        },
    )

    # Confirm log in did not succeed
    assert "Incorrect login details" in login_response.text
