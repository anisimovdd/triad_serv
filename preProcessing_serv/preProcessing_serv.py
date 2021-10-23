# python preProcessing_serv.py # запуск сервера
# 192:168:0:10

from flask import Flask, jsonify, request
import paho.mqtt.client as mqtt

app = Flask(__name__)

@app.route('/')
def home_page():
	return "OPEN /mqtt_sub"

@app.route('/mqtt_sub')
def mqtt_sub():
	
	def on_connect(client, userdata, flags, rc):
		print("🟢 Connected with RESULT_CODE = " + str(rc))
		client.subscribe("triad_serv/dataStore_serv")
		
	def on_message(client, userdata, msg):
		message = str(msg.payload, 'utf-8')
		print("> TOPIC: " + msg.topic + "\n" + "📩 MESSAGE: " + message)

	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect("127.0.0.1", 1883, 60)
	client.loop_forever()
	

@app.route('/event_1', methods=['POST'])
def event_1():
	arr_1 = [ ]
	received_1 = request.json # received_1 = {'title': request.json['title']}
	arr_1.append(received_1)
	# proc_arr_1 = smoothAlg(arr_1)
	# curl -i -X POST -H 'Content-Type: application/json' -d '{proc_arr_1}' http://192:168:0:15:5000/event_1
	return jsonify(arr_1), 201

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002) # https://codex.so/python-flask