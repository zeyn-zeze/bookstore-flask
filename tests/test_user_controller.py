import pytest
from models.User import User
from extensions import db


@pytest.fixture
def admin_user(app):
    with app.app_context():
        existing = User.query.filter_by(email="admin@test.com").first()
        if existing:
            db.session.delete(existing)
            db.session.commit()

        admin = User(
            username="admin",
            email="admin@test.com",
            phone="123456",
            role="admin",
            address="Admin Street"
        )
        admin.set_password("adminpass")
        db.session.add(admin)
        db.session.commit()
        return admin



@pytest.fixture
def login_admin(client, admin_user):
    client.post('/auth/login', data={
        'username': 'admin',
        'password': 'adminpass'
    })
    return client


def test_admin_can_access_user_dashboard(login_admin):
    response = login_admin.get('/dashboard/users/')
    assert response.status_code == 200
    assert b"User Management" in response.data


def test_non_admin_redirect(client):
    response = client.get('/dashboard/users/', follow_redirects=True)
    assert b"Only admins can access this page" in response.data


def test_add_user(login_admin):
    response = login_admin.post('/dashboard/users/', data={
        'add_user': True,
        'new_username': 'newuser',
        'new_email': 'newuser@test.com',
        'new_phone': '111222',
        'new_address': 'Ankara',
        'new_password': 'password123',
        'new_role': 'user'
    }, follow_redirects=True)
    assert b"New user added successfully" in response.data
    assert User.query.filter_by(username='newuser').first()


def test_delete_user(login_admin):
    user = User(username="temp", email="temp@test.com", phone="000", role="user", address="Test")
    user.set_password("pass")
    db.session.add(user)
    db.session.commit()

    response = login_admin.post('/dashboard/users/', data={
        'delete_user': user.id
    }, follow_redirects=True)
    assert b"User deleted successfully" in response.data
    assert User.query.get(user.id) is None


def test_user_info_requires_login(client):
    response = client.get('/dashboard/users/info', follow_redirects=True)
    assert b"Please log in to view your profile" in response.data


