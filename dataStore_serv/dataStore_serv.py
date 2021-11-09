# Запуск сервера: python dataStore_serv.py
from flask import Flask
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

app = Flask(__name__)
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = [["pP_serv", 0], ["eH_serv", 0]]
MQTT_CLIENT_ID = "dS_serv"
count = 0

@app.route('/')
def dS_serv():
	
	arr = [ ] # общий массив
	
	# Подключение + Подписка на TOPICS
	def on_connect(client, userdata, flags, rc):
		if rc == 0:
			print("🟢 Connected to Mosquitto (" + MQTT_BROKER + ":" + str(MQTT_PORT) + ")")
			client.subscribe(MQTT_TOPIC)
			print("Waiting for any messages with TOPIC='" + MQTT_TOPIC[0][0] + "','" + MQTT_TOPIC[1][0] + "'...")
		else:
			print("🔴 Connection failed")
			
	# Обработка полученных сообщений	
	def on_message(client, userdata, msg):
		message = str(msg.payload, 'utf-8')
		print("\n> TOPIC: " + msg.topic + " 📩 MESSAGE: " + message)

		# Запрос на запись от pP_serv
		if msg.topic == "pP_serv":
			m1 = message.replace("[[", "")
			m1 = m1.replace("]]", "")
			m1 = m1.replace(" ", "")
			message_arr = m1.split('],[')
			# Добавить в общий массив
			arr.append(message_arr)
			global count
			print("Writing to arr[" + str(count) + "]. " + "message_arr = " + str(message_arr))
			count = count + 1
			
		# Запрос события от eH_serv
		else:
			# Событие 1 -- пожать руку
			if message == "event_1":
				event_1_arr = arr[0]
				# Преобразуем в строку с разделением запятой и передаём на роборуку
				for e in event_1_arr:
					publish.single("dS_serv", payload = e, hostname = "127.0.0.1", port = 1883)
					print("EVENT_1. 📧 SEND: " + e)
			
			# Событие 2 -- взять предмет
			elif message == "event_2":
				event_2_arr = arr[1]
				# Преобразуем в строку с разделением запятой и передаём на роборуку
				for e in event_2_arr:
					publish.single("dS_serv", payload = e, hostname = "127.0.0.1", port = 1883)
					print("📧 SEND: " + e)
			
			# Событие 3 -- показать жест
			elif message == "event_3":
				event_3_arr = arr[2]
				# Преобразуем в строку с разделением запятой и передаём на роборуку
				for e in event_3_arr:
					publish.single("dS_serv", payload = e, hostname = "127.0.0.1", port = 1883)
					print("📧 SEND: " + e)
			
			# Неизвестное событие
			else:
				print("Неизвестное событие")
	
	client = mqtt.Client(MQTT_CLIENT_ID)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(MQTT_BROKER, MQTT_PORT, 60)
	client.loop_forever()
	

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000) # https://codex.so/python-flask