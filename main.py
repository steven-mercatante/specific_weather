import json
# --
import conf
import errors
# --
from flask import Flask
from flask import jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
	return 'Hello'

@app.route('/sunrise/<int:zip_code>', methods=['GET'])
def sunrise(zip_code):
	if len(str(zip_code)) != 5:
		return jsonify({'error': errors.INVALID_ZIP_CODE.format(zip_code )})
	endpoint = 'http://api.wunderground.com/api/{0}/astronomy/q/{1}.json'.format(conf.API_KEY, zip_code)
	r = requests.get(endpoint)
	json_content = json.loads(r.content)

	# Check if we got back valid data
	if 'error' in json_content['response']:
		return jsonify({'error': json_content['response']['error']['description']})

	resp = jsonify({
		'sunrise': '{0}:{1}'.format(
			json_content['sun_phase']['sunrise']['hour'],
			json_content['sun_phase']['sunrise']['minute']
		)
	})
	return resp

@app.route('/conditions/<int:zip_code>', methods=['GET'])
def conditions(zip_code):
	if len(str(zip_code)) != 5:
		return jsonify({'error': errors.INVALID_ZIP_CODE.format(zip_code )})
	endpoint = 'http://api.wunderground.com/api/{0}/conditions/q/CA/{1}.json'.format(conf.API_KEY, zip_code)
	r = requests.get(endpoint)
	json_content = json.loads(r.content)

	# Check if we got back valid data
	if 'error' in json_content['response']:
		return jsonify({'error': json_content['response']['error']['description']})

	resp = jsonify({
		'condition': json_content['current_observation']['weather']
	})
	return resp

if __name__ == '__main__':
	app.run()