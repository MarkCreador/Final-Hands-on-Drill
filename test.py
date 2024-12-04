import test
from drill import app, db  

@test.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  
        yield client
        with app.app_context():
            db.session.remove()  
            db.drop_all()  

def test_get_sensor_data(client):
    
    response = client.get('/sensor-data')
    assert response.status_code == 200
    assert b'[]' in response.data  

def test_create_sensor_data(client):
    response = client.post('/sensor-data', json={
        "Timestamp": "2024-12-03 10:00:00",
        "SensorType": "Ultrasonic",
        "ObjectDistance": 50,
        "FeedbackType": "Vibration",
        "VibrationLevel": 2,
        "SoundLevel": 0
    })
    assert response.status_code == 201
    assert b"Sensor data created" in response.data  
    
    with app.app_context():
        sensor_data = db.session.query(SensorData).first()
        assert sensor_data is not None
        assert sensor_data.SensorType == 'Ultrasonic'
        assert sensor_data.ObjectDistance == 50


def test_get_specific_sensor_data(client):
   
    client.post('/sensor-data', json={
        "Timestamp": "2024-12-03 10:00:00",
        "SensorType": "Ultrasonic",
        "ObjectDistance": 50,
        "FeedbackType": "Vibration",
        "VibrationLevel": 2,
        "SoundLevel": 0
    })

    
    response = client.get('/sensor-data/1') 
    assert response.status_code == 200
    assert b'Ultrasonic' in response.data
    assert b'50' in response.data

