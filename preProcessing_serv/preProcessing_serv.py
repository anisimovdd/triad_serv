# Запуск сервера: python preProcessing_serv.py
from flask import Flask
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish

app = Flask(__name__)
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "glove"
MQTT_CLIENT_ID = "pP_serv"
error_count = 0 # подсчёт числа ошибок

@app.route('/')
def pP_serv():
	
	arr = [ ] # единый массив, его назнаение описано ниже
	
	
	# Подключение + Подписка на TOPICS
	def on_connect(client, userdata, flags, rc):
		if rc == 0:
			print("🟢 Connected to Mosquitto (" + MQTT_BROKER + ":" + str(MQTT_PORT) + ")")
			client.subscribe(MQTT_TOPIC)
			print("Waiting for any messages with TOPIC='" + MQTT_TOPIC + "'...")
		else:
			print("🔴 Connection failed")

	# Обработка сообщений от перчатки	
	def on_message(client, userdata, msg):
		
		message = str(msg.payload, 'utf-8')
		message = message.replace("#", "") # убираем преамбулу Бахадыра
		print("\n> TOPIC: " + msg.topic + " 📩 MESSAGE: " + message)
		
		# ===========================
		# МЕСТО ДЛЯ ФУНКЦИИ ОБРАБОТКИ:
		#
		# from scipy.ndimage.filters import gaussian_filter
		#
		# array = [2, 3, 6, 4, 7, 7, 9, 9, 7, 8, 5, 3, 1, 4, 1 ]
		#
		# x = gaussian_filter(array, sigma=(.8), mode='nearest')
		# print(x)
		#
		# В качестве входных данных стоит принимать String "message".
		# На выходе String "message" должен быть перезаписан.
		# Но можно назвать по своему,  тогда будет необходимо переименовать другие переменные в коде.
		# ===========================
		
		# Обработка пустых сообщений
		if (len(message) != 35):
			global error_count
			error_count = error_count + 1
			print("Incorrect length of message. Now " + str(error_count) + " errors.")
		else:
			# Преобразование в массив целых чисел
			message_arr = message.split(',')
			message_arr = list(map(int, message_arr))
			
			# Предварительно массив будет иметь следующюю структуру:
			# message_arr = [ R1, R2, R3, R4, R5, AG1, AG2, AG3, IO_button], где
			# Rn - показания резисторов изгиба каждого пальца
			# AGn - показания акселерометра и гироскопа 
			# IO_button - кнопка 0 или 1. На неё возложена большая задача. Данные c IO_button = 0,
			# напрямую транслируются на роборуку. При IO_button = 1 алгоритм переходит в режим обучения.
			# Формируется единый массив arr = [ [], [], ... ]. При поступлении пакета с IO_button = 0,
			# запись в массив прекращается и считается, что он готов к обработке. По завершению обработки
			# единый массив должен быть отправлен на dS_serv.
			
			# Если поступил массив с IO_button = 0
			if message_arr[8] == 100:
				# Eсли единый массив ещё не заполнялся или был очищен
				if len(arr) == 0:
					publish.single("dS_serv", payload = str(msg.payload, 'utf-8'), hostname = "127.0.0.1", port = 1883)
					print("Live broadcast MODE. Send to robohand.")
				# Если единый массив сформирован
				else:
					# Отправка обработанного массива на dS_serv
					publish.single("pP_serv", payload = str(arr), hostname = "127.0.0.1", port = 1883)
					print("Learning MODE. End of array formation. Send to dataStore_serv. " + str(arr) )
					# Очистка единого массива
					arr.clear()
			# Если поступил массив с IO_button = 1
			else:
				# Формирование единого массива
				arr.append(message_arr)
				print("Learning MODE. Array formation.")			

	client = mqtt.Client(MQTT_CLIENT_ID)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(MQTT_BROKER, MQTT_PORT, 60)
	client.loop_forever()
	
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002) # https://codex.so/python-flask