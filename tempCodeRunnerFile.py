@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(UserID=data['UserID'], Name=data['Name'], PhoneNumber=data['PhoneNumber'])
    db.session.add(new_user)
    for usage in data['Usages']:
        new_usage = Usage(
            UsageID=usage['UsageID'],
            UserID=data['UserID'],
            UsageDetails=usage['UsageDetails'],
            IncubatorType=usage['IncubatorType'],
            StartTime=datetime.strptime(usage['StartTime'], '%Y-%m-%d %H:%M') if usage['StartTime'] else None,
            EndTime=datetime.strptime(usage['EndTime'], '%Y-%m-%d %H:%M') if usage['EndTime'] else None,
            Comment=usage['Comment'],
            Status=usage['Status']
        )
        db.session.add(new_usage)
    db.session.commit()
    return jsonify({'message': 'User and usages added successfully'}), 201
