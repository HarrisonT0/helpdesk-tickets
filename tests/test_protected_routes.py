import requests


ROUTE = "http://localhost:5000"
MESSAGE = "You must be logged in to access this page"


def test_home_protection():
    response = requests.get(f"{ROUTE}/")
    assert MESSAGE in response.text


# Tickets


def test_list_tickets_protection():
    response = requests.get(f"{ROUTE}/tickets")
    assert MESSAGE in response.text


def test_view_ticket_protection():
    response = requests.get(f"{ROUTE}/tickets/test")
    assert MESSAGE in response.text


def test_edit_ticket_protection():
    response = requests.get(f"{ROUTE}/tickets/test/edit")
    assert MESSAGE in response.text


def test_new_ticket_protection():
    response = requests.get(f"{ROUTE}/tickets/new")
    assert MESSAGE in response.text


def test_delete_ticket_protection():
    response = requests.post(f"{ROUTE}/tickets/test/delete")
    assert MESSAGE in response.text


# Users


def test_list_users_protection():
    response = requests.get(f"{ROUTE}/users")
    assert MESSAGE in response.text


def test_delete_user_protection():
    response = requests.post(f"{ROUTE}/users/test/delete")
    assert MESSAGE in response.text


def test_promote_user_protection():
    response = requests.post(f"{ROUTE}/users/test/promote")
    assert MESSAGE in response.text


def test_demote_user_protection():
    response = requests.post(f"{ROUTE}/users/test/demote")
    assert MESSAGE in response.text
