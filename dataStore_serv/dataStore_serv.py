# python dataStore_serv.py # запуск сервера
from flask import Flask
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

app = Flask(__name__)
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = [("pP_serv", 0), ("eH_serv", 0)]

@app.route('/')
def dS_serv():
	
	arr = [ ] # общий массив
	
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
		
		# Запрос на запись от pP_serv
		if msg.topic == "pP_serv":
			# Добавить в общий массив
			arr.append(msg.payload)
		# Запрос события от eH_serv
		else:
			# Событие 1 -- пожать руку
			if msg.payload == "event_1":
				event_1_arr = arr[0]
				# Цикл FOR для каждого массива из единого массива необходимо преобразовать к виду
				# с разделением запятной И отправить на роборуку.
				# publish.single("dS_serv", payload = proc_arr_1, hostname = "127.0.0.1", port = 1883)
				# print("📧 SEND: " + proc_arr_1)
			
			# Событие 2 -- взять предмет
			elif msg.payload == "event_2":
				event_2_arr = arr[1]
				# Цикл FOR для каждого массива из единого массива необходимо преобразовать к виду
				# с разделением запятной И отправить на роборуку.
				# publish.single("dS_serv", payload = proc_arr_1, hostname = "127.0.0.1", port = 1883)
				# print("📧 SEND: " + proc_arr_1)
			
			# Событие 3 -- показать жест
			elif msg.payload == "event_3":
				event_3_arr = arr[2]
				# Цикл FOR для каждого массива из единого массива необходимо преобразовать к виду
				# с разделением запятной И отправить на роборуку.
				# publish.single("dS_serv", payload = proc_arr_1, hostname = "127.0.0.1", port = 1883)
				# print("📧 SEND: " + proc_arr_1)
			else:
				# Неизвестное событие			
	
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(MQTT_BROKER, MQTT_PORT, 60)
	client.loop_forever()
	

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000) # https://codex.so/python-flask