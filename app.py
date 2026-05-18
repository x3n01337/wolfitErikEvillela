from flask import Flask, request, jsonify, url_for
from datetime import datetime, timezone
import uuid

app = Flask(__name__)

# In-memory activity log data (temporary until database-backed)
activity_log = [
    {
        'id': '0',
        'user_id': 1,
        'username': 'john',
        'timestamp': datetime.now(timezone.utc),
        'details': "Important stuff here",
    },
    {
        'id': '1',
        'user_id': 2,
        'username': 'yoko',
        'timestamp': datetime.now(timezone.utc),
        'details': "Even more important",
    },
]


def add_location(activity):
    """Add location field to an activity entry using url_for."""
    activity_copy = activity.copy()
    activity_copy['location'] = url_for('get_activity', activity_id=activity['id'], _external=True)
    return activity_copy


@app.route('/api/activities', methods=['GET'])
def get_activities():
    """GET: /api/activities -- returns all activity entries."""
    activities_with_location = [add_location(activity) for activity in activity_log]
    return jsonify({'activities': activities_with_location}), 200


@app.route('/api/activities/<activity_id>', methods=['GET'])
def get_activity(activity_id):
    """GET: /api/activities/<id> -- return a single activity entry by id."""
    for activity in activity_log:
        if activity['id'] == activity_id:
            return jsonify(add_location(activity)), 200
    return jsonify({'error': 'Activity not found'}), 404


@app.route('/api/activities', methods=['POST'])
def create_activity():
    """POST: /api/activities -- create a new activity entry."""
    data = request.get_json()
    
    # Validate required fields
    if not data or 'user_id' not in data or 'username' not in data or 'details' not in data:
        return jsonify({'error': 'Missing required fields: user_id, username, details'}), 400
    
    # Create new activity with system-generated ID
    new_activity = {
        'id': str(uuid.uuid4()),
        'user_id': data['user_id'],
        'username': data['username'],
        'timestamp': datetime.now(timezone.utc),
        'details': data['details'],
    }
    
    return jsonify(add_location(new_activity)), 201


if __name__ == '__main__':
    app.run(debug=True)
