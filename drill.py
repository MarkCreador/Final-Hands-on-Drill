from flask import Flask, request, jsonify, make_response
import mysql.connector
import xmltodict

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="blindassistdevice"  
)
cursor = db.cursor(dictionary=True)


def to_xml(data):
    """Convert JSON to XML."""
    return xmltodict.unparse({"response": data}, pretty=True)


@app.route('/sensor-data', methods=['GET', 'POST'])
def manage_sensor_data():
    if request.method == 'GET':
        format_type = request.args.get('format', 'json')
        cursor.execute("SELECT * FROM SensorData")
        sensor_data = cursor.fetchall()
        if format_type == 'xml':
            response = make_response(to_xml(sensor_data))
            response.headers["Content-Type"] = "application/xml"
            return response
        return jsonify(sensor_data)

    elif request.method == 'POST':
        data = request.json
        cursor.execute(
            "INSERT INTO SensorData (Timestamp, SensorType, ObjectDistance, FeedbackType, VibrationLevel, SoundLevel) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (data['Timestamp'], data['SensorType'], data['ObjectDistance'], data['FeedbackType'], data['VibrationLevel'], data['SoundLevel'])
        )
        db.commit()
        return jsonify({"message": "Sensor data created"}), 201

@app.route('/sensor-data/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def sensor_data_operations(id):
    if request.method == 'GET':
        format_type = request.args.get('format', 'json')
        cursor.execute("SELECT * FROM SensorData WHERE ID = %s", (id,))
        sensor_data = cursor.fetchone()
        if not sensor_data:
            return jsonify({"error": "Sensor data not found"}), 404
        if format_type == 'xml':
            response = make_response(to_xml(sensor_data))
            response.headers["Content-Type"] = "application/xml"
            return response
        return jsonify(sensor_data)

    elif request.method == 'PUT':
        data = request.json
        cursor.execute(
            "UPDATE SensorData SET Timestamp = %s, SensorType = %s, ObjectDistance = %s, FeedbackType = %s, "
            "VibrationLevel = %s, SoundLevel = %s WHERE ID = %s",
            (data['Timestamp'], data['SensorType'], data['ObjectDistance'], data['FeedbackType'], data['VibrationLevel'], data['SoundLevel'], id)
        )
        db.commit()
        return jsonify({"message": "Sensor data updated"})

    elif request.method == 'DELETE':
        cursor.execute("DELETE FROM SensorData WHERE ID = %s", (id,))
        db.commit()
        return jsonify({"message": "Sensor data deleted"})

if __name__ == '__main__':
    app.run(debug=True)
