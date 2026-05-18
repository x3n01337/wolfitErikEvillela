import pytest
import json
import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestGetActivities:
    """Tests for GET /api/activities endpoint."""
    
    def test_get_all_activities(self, client):
        """Test that GET /api/activities returns all activities."""
        response = client.get('/api/activities')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'activities' in data
        assert len(data['activities']) >= 2
        assert data['activities'][0]['username'] == 'john'
        assert data['activities'][1]['username'] == 'yoko'
    
    def test_get_activities_has_location(self, client):
        """Test that activities have location field."""
        response = client.get('/api/activities')
        data = json.loads(response.data)
        for activity in data['activities']:
            assert 'location' in activity
            assert '/api/activities/' in activity['location']
    
    def test_get_activities_has_required_fields(self, client):
        """Test that activities contain all required fields."""
        response = client.get('/api/activities')
        data = json.loads(response.data)
        required_fields = ['id', 'user_id', 'username', 'timestamp', 'details', 'location']
        for activity in data['activities']:
            for field in required_fields:
                assert field in activity


class TestGetActivityById:
    """Tests for GET /api/activities/<id> endpoint."""
    
    def test_get_activity_by_id_0(self, client):
        """Test retrieving activity with ID 0."""
        response = client.get('/api/activities/0')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == '0'
        assert data['username'] == 'john'
        assert data['details'] == "Important stuff here"
    
    def test_get_activity_by_id_1(self, client):
        """Test retrieving activity with ID 1."""
        response = client.get('/api/activities/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == '1'
        assert data['username'] == 'yoko'
        assert data['details'] == "Even more important"
    
    def test_get_activity_by_invalid_id(self, client):
        """Test that invalid ID returns 404."""
        response = client.get('/api/activities/999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_get_activity_has_location(self, client):
        """Test that single activity has location field."""
        response = client.get('/api/activities/0')
        data = json.loads(response.data)
        assert 'location' in data
        assert '/api/activities/0' in data['location']


class TestCreateActivity:
    """Tests for POST /api/activities endpoint."""
    
    def test_post_activity_success(self, client):
        """Test creating a new activity with valid data."""
        new_activity = {
            'user_id': 3,
            'username': 'alice',
            'details': 'Test activity'
        }
        response = client.post('/api/activities',
                              data=json.dumps(new_activity),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['id'] is not None
        assert data['user_id'] == 3
        assert data['username'] == 'alice'
        assert data['details'] == 'Test activity'
        assert 'timestamp' in data
        assert 'location' in data
    
    def test_post_activity_missing_user_id(self, client):
        """Test that missing user_id returns 400."""
        new_activity = {
            'username': 'bob',
            'details': 'Test activity'
        }
        response = client.post('/api/activities',
                              data=json.dumps(new_activity),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_post_activity_missing_username(self, client):
        """Test that missing username returns 400."""
        new_activity = {
            'user_id': 3,
            'details': 'Test activity'
        }
        response = client.post('/api/activities',
                              data=json.dumps(new_activity),
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_post_activity_missing_details(self, client):
        """Test that missing details returns 400."""
        new_activity = {
            'user_id': 3,
            'username': 'charlie'
        }
        response = client.post('/api/activities',
                              data=json.dumps(new_activity),
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_post_activity_empty_json(self, client):
        """Test that empty JSON returns 400."""
        response = client.post('/api/activities',
                              data=json.dumps({}),
                              content_type='application/json')
        assert response.status_code == 400
    
    def test_post_activity_generates_unique_ids(self, client):
        """Test that multiple POST requests generate different IDs."""
        new_activity = {
            'user_id': 4,
            'username': 'diana',
            'details': 'Another test'
        }
        response1 = client.post('/api/activities',
                               data=json.dumps(new_activity),
                               content_type='application/json')
        response2 = client.post('/api/activities',
                               data=json.dumps(new_activity),
                               content_type='application/json')
        data1 = json.loads(response1.data)
        data2 = json.loads(response2.data)
        assert data1['id'] != data2['id']
