"""Main API code
"""

import json
import os

from flask import Flask,request, jsonify , make_response

from source.predict.prediction import predict_price
from source.preprocessing.cleaning_data import preprocess
from source.preprocessing.validation import DataFeatures

app = Flask(__name__)

@app.route('/')
def status():
    return 'Alive'

@app.route('/predict', methods=['POST','GET'])
def predict():
    if request.method == 'GET' :
        # returning a json to explain what the POST expect (data and format)
        with open("source/preprocessing/reqspec.json", "r") as req_spec:
            req_spec = req_spec.read()
        response = make_response(req_spec, 200)
        response.mimetype = "application/json"
        return response

    else :
        try:
            datadict = request.get_json()['data']
        except:
            errors = {
                "error": {"data": "no 'data' element in root"}
            }
            return make_response(jsonify(errors), 400)
        
        # Validation expects feature names with '_' iso '-'
        datadict = {key.replace('-', '_'): value for key,
                    value in datadict.items()}
        data = DataFeatures()
        errors = data.validate(datadict)
        if errors:
            # change feature name(s) in error back to original
            errors = {key.replace('_', '-'): value for key,
                        value in errors.items()}
            # conform to error format
            errors = {
                "error": errors
            }
            # return as json with Bad Request status code
            return make_response(jsonify(errors), 400)

        # DataFeatures corrects "10" to 10 where needed
        validated = data.load(datadict)

        # Preprocess doesn't do anyting now
        processed = preprocess(validated)

        predicted_price = {
            "Estimated price" : predict_price(processed)
                          }
        return make_response(jsonify(predicted_price), 200)
        

if __name__ == "__main__":
    # You want to put the value of the env variable PORT if it exist
    # (some services only open specifiques ports)
    port = int(os.environ.get('PORT', 5000))
    # Threaded option to enable multiple instances for
    # multiple user access support
    # You will also define the host to "0.0.0.0" because localhost
    # will only be reachable from inside de server.
    app.run(host="0.0.0.0", threaded=True, port=port)
