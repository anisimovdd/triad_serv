# Запуск сервера: python eventHandling_serv.py
from flask import Flask
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

app = Flask(__name__)
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "robohand"

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
		print("> TOPIC: " + msg.topic + "\n" + "📩 MESSAGE: " + message)
		
		# Данные с датчиков роборуки также будут просто разделены запятой. В дальнейшем будет
		# необходимо исправить на отправку массивом. Но пока, чтобы Бахадыру лишний раз
		# не пришлось переписывать код, то преобразование в массив сделаем на стороне сервера.
		
		# Преобразование в массив
		message_arr = message.split(',')
		
		# Предварительно массив будет иметь следующюю структуру:
		# message_arr = [ T1, T2, T3, T4, T5, S1, S2, S3, S4, S5 ], где
		# Tn - показания датчиков температуры
		# Sn - показания датчиков давления
		
		# Событие 1 -- пожать руку
		if (29 < message_arr[0] < 45):
			publish.single("eH_serv", payload = "event_1", hostname = "127.0.0.1", port = 1883)
			# Добавить задержку в приёме новых сообщений на выполнение действия

		# Событие 2 -- взять предмет
		elif (145 < message_arr[5] < 654):
			publish.single("eH_serv", payload = "event_2", hostname = "127.0.0.1", port = 1883)
			# Добавить задержку в приёме новых сообщений на выполнение действия
		
		# Событие 3 -- показать жест
		elif (800 < message_arr[0] < 1455):
			publish.single("eH_serv", payload = "event_3", hostname = "127.0.0.1", port = 1883)
			# Добавить задержку в приёме новых сообщений на выполнение действия
		
		# Неизвестное событие
		else:
			print("Неизвестное событие")
	
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(MQTT_BROKER, MQTT_PORT, 60)
	client.loop_forever()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000) # https://codex.so/python-flask
