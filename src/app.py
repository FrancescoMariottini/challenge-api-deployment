"""Main API code
"""

import json
import os
import sys

from flask import Flask,request, jsonify , make_response
from flask_cors import CORS

from predict.prediction import predict_price, load_metrics
from preprocessing.cleaning_data import preprocess
from preprocessing.validation import DataFeatures

app = Flask(__name__)

CORS(app, resources=r'/*', allow_headers='Content-Type')

@app.route('/')
def status():
    return 'Alive'

@app.route('/predict', methods=['POST','GET'])
def predict():
    if request.method == 'GET' :
        # returning a json to explain what the POST expect (data and format)
        with open("src/preprocessing/reqspec.json", "r") as req_spec:
            req_spec = req_spec.read()
        response = make_response(req_spec, 200)
        response.mimetype = "application/json"
        return response

    else :
        req = request.get_json()
        try:
            datadict = req['data']
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

        # print to heroku log
        print(f"validated:\n", validated)
        sys.stdout.flush()

        processed = preprocess(validated)

        # print to heroku log
        print(f"preprocessed:\n", processed)
        sys.stdout.flush()

        #loading the model_metrics
        metrics = load_metrics(processed)
        
        predicted_price = {
            "prediction" : {  
                "price": predict_price(processed),
                "test_size": metrics['test_size'],
                "median_absolute_error": metrics['median_absolute_error'],
                "max_error": metrics['max_error'],
                "percentile025": metrics['percentile025'],
                "percentile975": metrics['percentile975']
                }
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
