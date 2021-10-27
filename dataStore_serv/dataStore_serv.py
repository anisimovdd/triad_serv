# python dataStore_serv.py # запуск сервера

from flask import Flask, request # jsonify
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

app = Flask(__name__)
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = [("pP_serv", 0), ("eH_serv", 0)]

@app.route('/')
def dS_serv():
	
	# Подключение + Подписка на TOPICS
	def on_connect(client, userdata, flags, rc):
		if rc == 0:
			print("🟢 Connected to Mosquitto (" + MQTT_BROKER + ":" + MQTT_PORT + ")")
			client.subscribe(MQTT_TOPIC)
		else:
			print("🔴 Connection failed")
			
	# Обработка полученных сообщений	
	def on_message(client, userdata, msg):
		message = str(msg.payload, 'utf-8')
		print("> TOPIC: " + msg.topic + "\n" + "📩 MESSAGE: " + message)
		# if msg.topic == "pP_serv":
		#	arr_1 = msg.payload # сохранить обработанный массив
		# elif msg.topic == "eH_serv":
		#	publish.single("dS_serv", payload = proc_arr_1, hostname = "127.0.0.1", port = 1883)
		#	print("📧 SEND: " + proc_arr_1)	
		
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(MQTT_BROKER, MQTT_PORT, 60)
	client.loop_forever()
	

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000) # https://codex.so/python-flask