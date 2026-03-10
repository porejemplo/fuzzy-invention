import os
import sqlite3
import pytest
from techtrends.app import app

@pytest.fixture
def client():
    # Use a temporary database for testing
    db_path = os.path.join(os.path.dirname(__file__), 'test_database.db')
    app.config['TESTING'] = True
    
    # Patch the get_db_connection to use test database
    import techtrends.app as tech_app
    original_get_db_connection = tech_app.get_db_connection
    
    def get_test_db_connection():
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        return connection
    
    tech_app.get_db_connection = get_test_db_connection
    
    # Initialize test database
    connection = sqlite3.connect(db_path)
    with open(os.path.join(os.path.dirname(__file__), '../schema.sql')) as f:
        connection.executescript(f.read())
    connection.execute("INSERT INTO posts (title, content) VALUES (?, ?)", ('Test Post', 'Test Content'))
    connection.commit()
    connection.close()

    with app.test_client() as client:
        yield client

    # Cleanup
    tech_app.get_db_connection = original_get_db_connection
    if os.path.exists(db_path):
        os.remove(db_path)

def test_index_page(client):
    """Test that the index page loads and contains the test post."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Test Post' in response.data

def test_about_page(client):
    """Test that the about page loads."""
    response = client.get('/about')
    assert response.status_code == 200
    assert b'About Us' in response.data

def test_post_page(client):
    """Test that a single post page loads."""
    response = client.get('/1')
    assert response.status_code == 200
    assert b'Test Post' in response.data

def test_non_existent_post(client):
    """Test that a non-existent post returns 404."""
    response = client.get('/100')
    assert response.status_code == 404
    assert b'Article Not Found' in response.data

def test_create_post_get(client):
    """Test that the create post page loads."""
    response = client.get('/create')
    assert response.status_code == 200
    assert b'Create a New Post' in response.data

def test_create_post_post_success(client):
    """Test creating a new post (POST request and redirect)."""
    response = client.post('/create', data={
        'title': 'New Test Post',
        'content': 'New Test Content'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'New Test Post' in response.data
    # Check if redirect happened to index
    assert len(response.history) == 1
    assert response.history[0].status_code == 302

def test_create_post_no_title(client):
    """Test creating a post without a title."""
    response = client.post('/create', data={
        'title': '',
        'content': 'Content only'
    })
    assert b'Title is required!' in response.data

def test_healthz_healthy(client):
    """Test healthz endpoint returns 200 when database is healthy."""
    response = client.get('/healthz')
    assert response.status_code == 200
    assert b'OK - healthy' in response.data

def test_metrics(client):
    """Test metrics endpoint."""
    response = client.get('/metrics')
    assert response.status_code == 200
    assert b'post_count' in response.data
    assert b'1' in response.data # We added one post in fixture

def test_healthz_unhealthy(client):
    """Test healthz endpoint returns 500 when database is missing."""
    # We can simulate this by making get_db_connection fail
    import techtrends.app as tech_app
    original_get_db_connection = tech_app.get_db_connection
    
    def fail_connection():
        raise Exception("Database connection failed")
    
    tech_app.get_db_connection = fail_connection
    
    response = client.get('/healthz')
    assert response.status_code == 500
    assert b'ERROR - unhealthy' in response.data
    
    # Restore for other tests if any (though fixture handles it)
    tech_app.get_db_connection = original_get_db_connection
