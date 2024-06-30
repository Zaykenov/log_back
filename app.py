from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
db = SQLAlchemy(app)
CORS(app)

class User(db.Model):
    UserID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    PhoneNumber = db.Column(db.String(15))
    UsageDetails = db.Column(db.String(255))
    IncubatorType = db.Column(db.String(50))
    StartTime = db.Column(db.DateTime)
    EndTime = db.Column(db.DateTime)
    Comment = db.Column(db.String(255))
    Status = db.Column(db.String(50))

# Ensure the database tables are created within the application context
with app.app_context():
    db.create_all()

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    result = [{
        'UserID': user.UserID,
        'Name': user.Name,
        'PhoneNumber': user.PhoneNumber,
        'UsageDetails': user.UsageDetails,
        'IncubatorType': user.IncubatorType,
        'StartTime': user.StartTime.strftime('%Y-%m-%d %H:%M') if user.StartTime else None,
        'EndTime': user.EndTime.strftime('%Y-%m-%d %H:%M') if user.EndTime else None,
        'Comment': user.Comment,
        'Status': user.Status
    } for user in users]
    return jsonify(result)

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(
        Name=data['Name'],
        PhoneNumber=data['PhoneNumber'],
        UsageDetails=data['UsageDetails'],
        IncubatorType=data['IncubatorType'],
        StartTime=datetime.strptime(data['StartTime'], '%Y-%m-%d %H:%M') if data.get('StartTime') else None,
        EndTime=datetime.strptime(data['EndTime'], '%Y-%m-%d %H:%M') if data.get('EndTime') else None,
        Comment=data['Comment'],
        Status=data['Status']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)
    user.Name = data.get('Name', user.Name)
    user.PhoneNumber = data.get('PhoneNumber', user.PhoneNumber)
    user.UsageDetails = data.get('UsageDetails', user.UsageDetails)
    user.IncubatorType = data.get('IncubatorType', user.IncubatorType)
    user.StartTime = datetime.strptime(data['StartTime'], '%Y-%m-%d %H:%M') if data.get('StartTime') else user.StartTime
    user.EndTime = datetime.strptime(data['EndTime'], '%Y-%m-%d %H:%M') if data.get('EndTime') else user.EndTime
    user.Comment = data.get('Comment', user.Comment)
    user.Status = data.get('Status', user.Status)
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

# Serve Swagger UI
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Incubator API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Serve the index.html at the root URL
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
