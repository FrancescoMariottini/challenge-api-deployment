from typing import Dict, Optional, Union
import pandas as pd
import json

def preprocess(house_data: Optional[Dict[str, Union[int, bool, str]]] = None) -> Union[Dict[str, Union[int, bool, str]], str]:
	'''Takes the parsed and validated json data provided in the request
	and returns a dictionary that conforms to the X input features of
	our model.
	:house_data: the validated dictionary of the request
	'''

	# # create a dataframe out of the request for easier manipulation
	# # ensure the right dummies can be creatd by adding an observation
	# # with inverse booleans	
	# for key, value in house_data.items():
	# 	if type(value) == bool:
	# 		house_data[key] = [value, not value]
	# 	else:
	# 		house_data[key] = [value, value]

	# request = pd.DataFrame.from_dict(house_data)


	# # dummy encode categoricals
	# dummies = ["property_type", "zip_code", "garden",
	# 				"equipped_kitchen", "swimmingpool",
	# 				"furnished", "open_fire", "terrace",
	# 				"facades_number", "building_state"]
	# request = pd.get_dummies(data = request, columns = dummies,
	# 							prefix_sep = '')


	# # adopt naming used in our model ('-' iso '_')
	# bool_rename = {"gardenTrue": "garden",
	# 			"equipped_kitchenTrue": "equipped_kitchen",
	# 			"swimmingpoolTrue": "swimmingpool",
	# 			"furnishedTrue": "furnished",
	# 			"open_fireTrue": "open_fire",
	# 			"terraceTrue": "terrace"}
	# request.rename(columns = bool_rename, inplace = True)

	# categoricals = ["property_type", "zip_code", "building_state"]
	# for cat in categoricals:
	# 	request.columns = request.columns.str.replace(cat, '')

	# request.columns = request.columns.str.replace('_', '-')

	
	# # Set up merging of the request data into the structure
	# # of our model. Missing Optional features will be 0.
	# with open("src/model/columns.json","r") as f:
	# 	model_columns = json.load(f)['data_columns']
	# model_df = pd.DataFrame({col: 0 for col in model_columns},
	# 			index = [0]).T
	# request_df = request.T[[0]]
	
	# request = request_df.merge(model_df, how = 'right',
	# 						right_index = True,
	# 						left_index = True)
	# request['request'] = request.sum(axis = 1).astype(int)
	# request = request['request'].to_numpy()
	# print(request)

	

	return house_data


example = {'open_fire': True, 'garden': True, 'facades_number': 2,
		'full_address': 'Monseigneur Cardijnlaan 33/2 2650 Edegem',
		'land_area': 500, 'zip_code': 2650, 'property_type': 'APARTMENT',
		'garden_area': 200, 'building_state': 'NEW', 'area': 100,
		'terrace': True, 'terrace_area': 10, 'equipped_kitchen': True,
		'furnished': False, 'rooms_number': 3, 'swimmingpool': False}

preprocess(example)