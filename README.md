# triad_serv

Каждая из папок - отдельный Flask-сервер со своим окружением.
Так я себе представляю разделение на микросервисы.

![png](https://raw.githubusercontent.com/anisimovdd/triad_serv/main/triad_serv.drawio.png)

# preProcessing_serv (192:168:0:10)

arr_1 = [ { 'finger_1': '0',
			'finger_2': '0',
			'finger_3': '0',
			'finger_4': '0',
			'finger_5': '0' } ]
			
arr_2 = [ { 'finger_1': '0',
			'finger_2': '0',
			'finger_3': '0',
			'finger_4': '0',
			'finger_5': '0' } ]

arr_3 = [ { 'finger_1': '0',
			'finger_2': '0',
			'finger_3': '0',
			'finger_4': '0',
			'finger_5': '0' } ]

1. 	Получает POST (данные 5-ти пальцев) от перчатки и формирует массив 5-ти пальцев:

		EVENT_1:	
					# curl -i -X POST -H 'Content-Type: application/json' -d '{\"finger_1\": \"5\", \"finger_2\": \"10\", \"finger_3\": \"10\", \"finger_4\": \"5\", \"finger_5\": \"5\"}' http://192:168:0:10:5000/event_1
					received_1 = request.json
					arr_1.append(received_1)				
		EVENT_2:	
					# curl -i -X POST -H 'Content-Type: application/json' -d '{\"finger_1\": \"5\", \"finger_2\": \"10\", \"finger_3\": \"10\", \"finger_4\": \"5\", \"finger_5\": \"5\"}' http://192:168:0:10:5000/event_2
					received_2 = request.json
					arr_2.append(received_2)	
		EVENT_3:	
					# curl -i -X POST -H 'Content-Type: application/json' -d '{\"finger_1\": \"5\", \"finger_2\": \"10\", \"finger_3\": \"10\", \"finger_4\": \"5\", \"finger_5\": \"5\"}' http://192:168:0:10:5000/event_3
					received_3 = request.json
					arr_3.append(received_3)

? КАК ПОНЯТЬ ЧТО МАССИВ ЗАПОЛНЕН И ЕГО МОЖНО ОТПРАВЛЯТЬ НА ОБРАБОТКУ ?
						
2.	Массив 5-ти пальцесв проходит через алгоритм сглаживания:
		
		EVENT_1:	proc_arr_1 = smoothAlg(arr_1)
		
		EVENT_2:	proc_arr_2 = smoothAlg(arr_2)
		
		EVENT_3:	proc_arr_3 = smoothAlg(arr_3)
		
3.	Отправляет POST (массив 5-ти пальцесв) на dataStore_serv:
		
		EVENT_1:	curl -i -X POST -H 'Content-Type: application/json' -d '{proc_arr_1}' http://192:168:0:15:5000/event_1
		
		EVENT_2:	curl -i -X POST -H 'Content-Type: application/json' -d '{proc_arr_2}' http://192:168:0:15:5000/event_2
		
		EVENT_3:	curl -i -X POST -H 'Content-Type: application/json' -d '{proc_arr_3}' http://192:168:0:15:5000/event_3

# dataStore_serv (192:168:0:15)

1. 	Получает POST (массив 5-ти пальцев) от preProcessing_serv;
2. 	Записывает массив в переменные для конкретного типа события:
	
		EVENT_1:	
					# curl -i -X POST -H 'Content-Type: application/json' -d '{proc_arr_1}' http://192:168:0:15:5000/event_1
					data_1 = request.json
		EVENT_2:	
					# curl -i -X POST -H 'Content-Type: application/json' -d '{proc_arr_2}' http://192:168:0:15:5000/event_2
					data_2 = request.json
		EVENT_3:	
					# curl -i -X POST -H 'Content-Type: application/json' -d '{proc_arr_3}' http://192:168:0:15:5000/event_3
					data_3 = request.json

3. При получении GET (тип события) от eventHandling_serv отправляет POST (массив):
		
		EVENT_1:
					# curl -i -X GET -H 'Content-Type: application/json' -d '{\"req_1\": \"1\"}' http://192:168:0:15:5000/event_1
					curl -i -X POST -H 'Content-Type: application/json' -d '{data_1}' http://[robo-hand-IP]/
		EVENT_2:
					# curl -i -X GET -H 'Content-Type: application/json' -d '{\"req_2\": \"1\"}' http://192:168:0:15:5000/event_2
					curl -i -X POST -H 'Content-Type: application/json' -d '{data_2}' http://[robo-hand-IP]/
		EVENT_3:
					# curl -i -X GET -H 'Content-Type: application/json' -d '{\"req_3\": \"1\"}' http://192:168:0:15:5000/event_3
					curl -i -X POST -H 'Content-Type: application/json' -d '{data_3}' http://[robo-hand-IP]/
					
Получив массив data_1 роборука должна перевести JSON во внутренние комманды и произвести требуемое действие

# eventHandling_serv (192:168:0:20)

1. 	Получает POST (данные датчика) от датчика роборуки:
		
		EVENT_1:	
					# curl -i -X POST -H 'Content-Type: application/json' -d '{\"sensor_1\": \"85\"}' http://192:168:0:20:5000/event_1
					sensor_1 = request.json
		EVENT_2:	
					# curl -i -X POST -H 'Content-Type: application/json' -d '{\"sensor_2\": \"85\"}' http://192:168:0:20:5000/event_2
					sensor_2 = request.json
		EVENT_3:	
					# curl -i -X POST -H 'Content-Type: application/json' -d '{\"sensor_3\": \"85\"}' http://192:168:0:20:5000/event_3
					sensor_3 = request.json

2. 	Проверяет триггер-условие;
3. 	Отправляет GET (тип события) в dataStore_serv, чтобы получить массив:

		EVENT_1:	
					min_int = 12 # крайние значения диапазона,
					max_int = 45 # полученные опытным путём
						
					if (min_int < sensor_1 < max_int)
						curl -i -X GET -H 'Content-Type: application/json' -d '{\"req_1\": \"1\"}' http://192:168:0:15:5000/event_1
					else
						abort 400
		EVENT_2:	
					min_int = 1154 # крайние значения диапазона,
					max_int = 8975 # полученные опытным путём
					
					if (min_int < sensor_2 < max_int)
						curl -i -X GET -H 'Content-Type: application/json' -d '{\"req_2\": \"1\"}' http://192:168:0:15:5000/event_2	10
					else
						abort 400
		EVENT_3:	
					min_int = 445588 # крайние значения диапазона,
					max_int = 454848 # полученные опытным путём
						
					if (min_int < sensor_3 < max_int)
						curl -i -X GET -H 'Content-Type: application/json' -d '{\"req_3\": \"1\"}' http://192:168:0:15:5000/event_3
					else
						abort 400
