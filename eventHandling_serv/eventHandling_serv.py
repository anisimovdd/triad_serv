# python eventHandling_serv.py # запуск сервера
from flask import Flask
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

app = Flask(__name__)
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "robohand"

@app.route('/')
def eH_serv():
	
	e1_min = 12
	e1_max = 45
	
	e2_min = 145
	e2_max = 654
	
	e3_min = 854
	e3_max = 1245
	
	# Подключение + Подписка на TOPICS
	def on_connect(client, userdata, flags, rc):
		if rc == 0:
			print("🟢 Connected to Mosquitto (" + MQTT_BROKER + ":" + MQTT_PORT + ")")
			client.subscribe(MQTT_TOPIC)
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
		if (e1_min < message_arr[0] < e1_max)
			publish.single("eH_serv", payload = "event_1", hostname = "127.0.0.1", port = 1883)
			# Добавить задержку в приёме новых сообщений на выполнение действия

		# Событие 2 -- взять предмет
		elif (e2_min < message_arr[5] < e1_max)
			publish.single("eH_serv", payload = "event_2", hostname = "127.0.0.1", port = 1883)
			# Добавить задержку в приёме новых сообщений на выполнение действия
		
		# Событие 3 -- показать жест
		elif (e3_min < message_arr[0] < e3_max)
			publish.single("eH_serv", payload = "event_3", hostname = "127.0.0.1", port = 1883)
			# Добавить задержку в приёме новых сообщений на выполнение действия
		
		# Неизвестное событие
		else
			print("Неизвестное событие")
	
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(MQTT_BROKER, MQTT_PORT, 60)
	client.loop_forever()

if __name__ == '__main__':
    app.run(host='192.168.0.20', port=5000) # https://codex.so/python-flask