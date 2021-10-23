# python dataStore_serv.py # запуск сервера

from flask import Flask, jsonify, request
import paho.mqtt.publish as publish

app = Flask(__name__)

@app.route('/')
def home_page():
	return "OPEN /mqtt_pub"

@app.route('/mqtt_pub')
def mqtt_pub():
	message = "finger_1"
	publish.single("triad_serv/dataStore_serv", payload = message, hostname = "127.0.0.1", port = 1883)
	print("📧 SEND: " + message)
	return "MESSAGE SENT"

@app.route('/event_1', methods=['POST', 'GET'])
def event_1():
	if request.method == 'POST':
		data_1 = request.json
		return jsonify(data_1), 201
	else:
		return 0

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000) # https://codex.so/python-flask