# triad_serv

Описание временно некорректно в связи с переходом на MQTT. Каждая из папок - отдельный Flask-сервер со своим окружением. Так я себе представляю разделение на микросервисы.

![png](https://raw.githubusercontent.com/anisimovdd/triad_serv/master/triad_serv.drawio.png)

# preProcessing_serv (192:168:0:10)

1. 	Получает данные от перчатки и формирует массив:

		# curl -i -X POST -H 'Content-Type: application/json' -d '{\"finger_1\": \"5\", \"finger_2\": \"10\", \"finger_3\": \"10\", \"finger_4\": \"5\", \"finger_5\": \"5\"}' http://192:168:0:10:5000/event_1
		received_1 = request.json
		arr_1.append(received_1)
						
2.	Массив проходит через алгоритм сглаживания:
		
		proc_arr_1 = smoothAlg(arr_1)
		
3.	Отправляет обработанный массив на dataStore_serv:
		
		curl -i -X POST -H 'Content-Type: application/json' -d '{proc_arr_1}' http://192:168:0:15:5000/event_1
		
# dataStore_serv (192:168:0:15)

1. 	Получает обработанный массив от preProcessing_serv;
2. 	Записывает массив в переменные для конкретного типа события:
	
		# curl -i -X POST -H 'Content-Type: application/json' -d '{proc_arr_1}' http://192:168:0:15:5000/event_1
		data_1 = request.json
		
3. При получении запроса от eventHandling_serv отправляет массив прямиком В ВЕНУ роборуки:
		
		# curl -i -X GET -H 'Content-Type: application/json' -d '{\"req_1\": \"1\"}' http://192:168:0:15:5000/event_1
		curl -i -X POST -H 'Content-Type: application/json' -d '{data_1}' http://[robo-hand-IP]/
					
Получив массив data_1 роборука должна перевести JSON во внутренние комманды и произвести требуемое действие

# eventHandling_serv (192:168:0:20)

1. 	Получает данные с датчиков роборуки:
		
		# curl -i -X POST -H 'Content-Type: application/json' -d '{\"sensor_1\": \"85\"}' http://192:168:0:20:5000/event_1
		sensor_1 = request.json
		
2. 	Проверяет триггер-условие;
3. 	Отправляет запрос в dataStore_serv, чтобы получить массив:

		min_int = 12 # крайние значения диапазона,
		max_int = 45 # полученные опытным путём
						
		if (min_int < sensor_1 < max_int)
			curl -i -X GET -H 'Content-Type: application/json' -d '{\"req_1\": \"1\"}' http://192:168:0:15:5000/event_1
		else
			abort 400
