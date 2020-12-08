from typing import Dict, Optional, Union
import pandas as pd
import json

def preprocess(validated: Optional[Dict[str, Union[int, bool, str]]] = None) -> Dict[str, Union[int, str]]:
	'''Takes the parsed and validated json data provided in the request
	and returns a dictionary that conforms to the input features of
	our model. Dummy creation happens in prediction.py.
	:validated: the validated dictionary of the request
	'''

	# enforce notation for compatibility with our model
	processed = validated
	processed['property_type'] = processed['property_type'].upper()
	try:
		processed['building_state'] = processed['building_state'].lower()
	except:
		pass

	processed = {
		key.replace('_', '-'): value for key, value in processed.items()
		}

	processed = {
		key: int(value) if type(value) == bool else value for \
		key, value in processed.items()
		}


	# update default X features with values from the request
	default = {
			"area": None,
			"property-type": None,
			"rooms-number": None,
			"zip-code": None,
			"land-area": 0,
			"garden": 0,
			"garden-area": 0,
			"equipped-kitchen": 0,
			"swimmingpool": 0,
			"furnished": 0,
			"open-fire": 0,
			"terrace": 0,
			"terrace-area": 0,
			"facades-number": 2,
			"building-state": "good"
	}

	for key, value in default.items():
		try:
			default[key] = processed[key]
		except:
			pass

	return default
