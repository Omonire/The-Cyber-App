import pytest
from app import app, db
from models import User
from unittest.mock import MagicMock

@pytest.fixture
def client():
    """
    A fixture to configure the application for testing, create a fresh in-memory
    database for each test, and provide a test client.
    """
    # Configure the app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use an in-memory SQLite DB
    app.config['SECRET_KEY'] = 'test_secret'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all() # Create all tables
        yield app.test_client() # Provide the test client
        db.drop_all() # Drop all tables after the test

@pytest.fixture
def logged_in_client(client):
    """A fixture that provides a client that is already logged in."""
    # Create a test user directly in the test database
    test_user = User(username='testuser', email='test@example.com')
    test_user.set_password('password123')
    db.session.add(test_user)
    db.session.commit()

    # Log in the user by setting the session cookie
    with client.session_transaction() as session:
        session['user_id'] = test_user.id

    return client

# --- Test Cases ---

def test_registration(client):
    """Test user registration."""
    response = client.post('/register', data={
        'username': 'newuser',
        'email': 'new@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Registration successful! Please log in." in response.data
    # Verify user was created
    user = User.query.filter_by(email='new@example.com').first()
    assert user is not None

def test_login_and_logout(client):
    """Test user login and logout."""
    # First, create a user to log in with
    test_user = User(username='testuser', email='test@example.com')
    test_user.set_password('password123')
    db.session.add(test_user)
    db.session.commit()

    # Test login
    response = client.post('/login', data={'email': 'test@example.com', 'password': 'password123'}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Welcome, testuser!" in response.data

    # Test logout
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"You have been logged out." in response.data

def test_protected_routes_unauthenticated(client):
    """Test that protected routes redirect when not logged in."""
    response = client.get('/dashboard', follow_redirects=True)
    assert response.status_code == 200
    assert b"Please log in to access this page." in response.data

def test_protected_routes_authenticated(logged_in_client):
    """Test that protected routes are accessible when logged in."""
    response = logged_in_client.get('/dashboard')
    assert response.status_code == 200
    assert b"Welcome, testuser!" in response.data

def test_task_completion(logged_in_client):
    """Test the full task completion flow."""
    # View the first task
    response = logged_in_client.get('/tasks')
    assert response.status_code == 200
    from modules.tasks import DAILY_TASKS
    first_task = DAILY_TASKS[0]
    assert bytes(first_task, 'utf-8') in response.data

    # Complete the task
    response = logged_in_client.post('/complete-task', data={'task_text': first_task}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Great job! Task marked as complete.' in response.data

    # Verify the next task is shown
    response = logged_in_client.get('/tasks')
    second_task = DAILY_TASKS[1]
    assert bytes(second_task, 'utf-8') in response.data
    assert bytes(first_task, 'utf-8') not in response.data

def test_news_page_mocked(client, mocker):
    """Test the news page with mocked feed data."""
    mock_feed = MagicMock(entries=[{'title': 'Mocked News', 'link': '#', 'summary': 'Summary', 'published': 'Date'}])
    mocker.patch('feedparser.parse', return_value=mock_feed)
    response = client.get('/news')
    assert response.status_code == 200
    assert b"Mocked News" in response.data