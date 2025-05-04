# Fix import errors by setting the root path for Python imports
import sys
import os

from app import create_app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask import session
from models.User import User
from extensions import db

# Fixture to create a registered user for login tests
@pytest.fixture
def registered_user(client):
    app = create_app()
    with app.app_context():
        user = User(username="testuser", email="test@example.com", phone="5555555555", address="Test City")
        user.set_password("testpass")
        db.session.add(user)
        db.session.commit()
        return user

# Test: Successful user registration
def test_register_success(client):
    response = client.post("/auth/register", data={
        "username": "newuser",
        "email": "new@example.com",
        "password": "pass123",
        "confirm_password": "pass123",
        "phone": "5551234567",
        "address": "Somewhere"
    }, follow_redirects=True)
    assert b"Registration successful" in response.data

# Test: Registration fails when passwords do not match
def test_register_password_mismatch(client):
    response = client.post("/auth/register", data={
        "username": "user2",
        "email": "user2@example.com",
        "password": "123456",
        "confirm_password": "abcdef",
        "phone": "1234567890",
        "address": "Nowhere"
    }, follow_redirects=True)
    assert b"Passwords do not match" in response.data

# Test: Registration fails when username or email already exists
def test_register_existing_user(client, registered_user):
    response = client.post("/auth/register", data={
        "username": "testuser",  # already exists
        "email": "test@example.com",
        "password": "pass123",
        "confirm_password": "pass123",
        "phone": "5551234567",
        "address": "Same"
    }, follow_redirects=True)
    assert b"Username or email already registered" in response.data

# Test: Successful login with correct credentials
def test_login_success(client, registered_user):
    response = client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpass"
    }, follow_redirects=True)
    assert b"Logout (testuser)" in response.data


# Test: Login fails with incorrect credentials
def test_login_fail(client):
    response = client.post("/auth/login", data={
        "username": "nouser",
        "password": "wrongpass"
    }, follow_redirects=True)
    assert b"Incorrect username or password" in response.data

# Test: Dashboard cannot be accessed without logging in
def test_dashboard_requires_login(client):
    response = client.get("/auth/dashboard", follow_redirects=True)
    assert b"Please login first" in response.data

# Test: Successful logout clears the session
def test_logout(client, registered_user):
    # First log in
    client.post("/auth/login", data={
        "username": "testuser",
        "password": "testpass"
    }, follow_redirects=True)
    
    # Then log out
    response = client.get("/auth/logout", follow_redirects=True)
    assert b"Login" in response.data and b"Register" in response.data

