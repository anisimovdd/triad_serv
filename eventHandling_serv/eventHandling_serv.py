# python eventHandling_serv.py # запуск сервера
# 192:168:0:20

from flask import Flask, jsonify, request, abort

app = Flask(__name__)

@app.route('/event_1', methods=['POST'])
def event_1():
	sensor_1 = request.json
	min_int = 12 # крайние значения диапазона,
	max_int = 45 # полученные опытным путём
	if (min_int < sensor_1 < max_int)
		# curl -i -X GET -H 'Content-Type: application/json' -d '{\"req_1\": \"1\"}' http://192:168:0:15:5000/event_1
	else
		abort 400

@app.route('/event_2', methods=['POST'])
def event_2():
	sensor_2 = request.json
	min_int = 1154 # крайние значения диапазона,
	max_int = 8975 # полученные опытным путём
	if (min_int < sensor_2 < max_int)
		# curl -i -X GET -H 'Content-Type: application/json' -d '{\"req_2\": \"1\"}' http://192:168:0:15:5000/event_2
	else
		abort 400

@app.route('/event_3', methods=['POST'])
def event_3():
	sensor_3 = request.json
	min_int = 445588 # крайние значения диапазона,
	max_int = 454848 # полученные опытным путём
	if (min_int < sensor_3 < max_int)
		# curl -i -X GET -H 'Content-Type: application/json' -d '{\"req_3\": \"1\"}' http://192:168:0:15:5000/event_3
	else
		abort 400

if __name__ == '__main__':
    app.run(host='192.168.0.20', port=5000) # https://codex.so/python-flask