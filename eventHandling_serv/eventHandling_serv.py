# Запуск сервера: python eventHandling_serv.py
from flask import Flask
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

app = Flask(__name__)
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "robohand"
MQTT_CLIENT_ID = "eH_serv"

@app.route('/')
def eH_serv():
	
	# Подключение + Подписка на TOPICS
	def on_connect(client, userdata, flags, rc):
		if rc == 0:
			print("🟢 Connected to Mosquitto (" + MQTT_BROKER + ":" + str(MQTT_PORT) + ")")
			client.subscribe(MQTT_TOPIC)
			print("Waiting for any messages with TOPIC='" + MQTT_TOPIC + "'...")
		else:
			print("🔴 Connection failed")
			
	# Обработка сообщений от роборуки	
	def on_message(client, userdata, msg):
		message = str(msg.payload, 'utf-8')
		print("\n> TOPIC: " + msg.topic + " 📩 MESSAGE: " + message)
				
		# Преобразование в массив
		message_arr = message.split(',')
		message_arr = list(map(int, message_arr))
				
		# Предварительно массив будет иметь следующюю структуру:
		# message_arr = [ T1, T2, T3, T4, T5, T6, S1, S2, S3, S4, S5 ], где
		# Tn - показания датчиков температуры
		# Sn - показания датчиков давления
		
		# Обратная связь для лампочки
		# message = "111,222,333,444,555,666,10,20,30,40,50"
		diod_feedback = message.replace(",","")[:-10]
		publish.single("diod_feedback", payload = diod_feedback, hostname = "127.0.0.1", port = 1883)
				
		# Событие 1 -- пожать руку
		if (29 < message_arr[0] < 45):
			publish.single("eH_serv", payload = "event_1", hostname = "127.0.0.1", port = 1883)
			print("EVENT_1. Shake hand.")
			# Добавить задержку в приёме новых сообщений на выполнение действия

		# Событие 2 -- взять предмет
		elif (145 < message_arr[5] < 654):
			publish.single("eH_serv", payload = "event_2", hostname = "127.0.0.1", port = 1883)
			print("EVENT_2. Take an item.")
			# Добавить задержку в приёме новых сообщений на выполнение действия
		
		# Событие 3 -- показать жест
		elif (800 < message_arr[0] < 1455):
			publish.single("eH_serv", payload = "event_3", hostname = "127.0.0.1", port = 1883)
			print("EVENT_3. Show gesture.")
			# Добавить задержку в приёме новых сообщений на выполнение действия
		
		# Неизвестное событие
		else:
			print("Неизвестное событие")
	
	client = mqtt.Client(MQTT_CLIENT_ID)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(MQTT_BROKER, MQTT_PORT, 60)
	client.loop_forever()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001) # https://codex.so/python-flask