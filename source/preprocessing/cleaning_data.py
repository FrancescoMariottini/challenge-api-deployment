from typing import Dict, Optional, Union

def preprocess(house_data: Optional[Dict[str, Union[int, bool, str]]]) -> Union[Dict[str, Union[int, bool, str]], str]
'''Takes the parsed json data provided by the frontend and returns a dictionary that conforms to the X input
features of our model, imputing values for optional fields where needed. If the required json format was not
adhered to, the field with the error is returned (ex. 'area_validation_error').
:house_data: the parsed json data provided as a dictionary (output of request.get_json())
'''

	# for development, a valid dictionary is pinned when no input is given
	if house_data == None:
		house_data = {
			'area': 100,
			'property-type': 'APARTMENT',
			'rooms-number': 3,
			'zip-code': 2650,
			}

	mandatories_ref = {
		'area': int,
		'property-type': ['APARTMENT', 'HOUSE', 'OTHERS'],
		'rooms-number': int,
		'zip-code': int,
	}

	optionals_ref = {
		'land-area': int,
		'garden': bool,
		'garden-area': int,
		'equipped-kitchen': bool,
		'full-address': str,
		'swimmingpool': bool,
		'furnished': bool,
		'open-fire': bool,
		'terrace': bool,
		'terrace-area': int,
		'facades-number': int,
		'building-state': ['NEW', 'GOOD', 'TO RENOVATE', 'JUST RENOVATED', 'TO REBUILD']
	}

	for key, value in mandatories_ref.items():
		try:
			if type(house_data['key']) == value:
				pass
		except:
			pass
			
	return house_data




