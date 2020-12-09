"""preprocessing code for the request is here
"""

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
		key: int(value) if type(value) == bool else value for \
		key, value in processed.items()
		}


	# value imputation in case not provided in request
	# areas are 1 because the model features is log(area)
	imputed = {
			"area": None,
			"property_type": None,
			"rooms_number": None,
			"zip_code": None,
			"land_area": 1,
			"garden": 0,
			"garden_area": 1,
			"equipped_kitchen": 0,
			"swimmingpool": 0,
			"furnished": 0,
			"open_fire": 0,
			"terrace": 0,
			"terrace_area": 1,
			"facades_number": 2,
			"building_state": "good"
	}

	# Do not reflect requested 'land_area' in case of apartments
	# The model wrongly provides a negative price for those
	if processed['property_type'] == 'APARTMENT':
		try:
			del processed["land_area"]
		except:
			pass

	for key, value in imputed.items():
		try:
			imputed[key] = processed[key]
		except:
			pass

	return imputed
