# os module may be needed to get the PORT number from heroku
import os
from flask import Flask,request, jsonify
# I guess this is how to import Preprocessing
from preprocessing.validation import DataFeatures
from preprocessing.cleaning_data import preprocess
from source.predict import prediction

app = Flask(__name__)

@app.route('/')
def status():
    return 'Alive'

@app.route('/predict', methods=['POST','GET'])
def predict():
    if request.method == 'GET' :
        #returning a string to explain what the POST expect (data and format)
        retjson = {
            "area": 'int',
            "property-type": 'APARTMENT | HOUSE | OTHERS',
            "rooms-number": 'int',
            "zip-code": 'int'
                 }
        return jsonify(retjson)

    else :
        datadict = request.get_json()
        # Validation expects feature names with _ iso -
        datadict = {key.replace('-', '_'): value for key,
                            value in datadict.items()}
        data = DataFeatures()
        errors = data.validate(datadict)
        if errors:
            # change feature name in error back to original
            abort(BAD_REQUEST, str(errors).replace('_','-'))
        # DataFeatures changes "10" to 10 (as example)
        validated = data.load(datadict)
        #get the required parameters
        processeddata = cleaning_data.preprocess(validated)
        prediction = prediction.predict_price(processeddata)
        return jsonify(prediction)
        

if __name__ == "__main__":
    # You want to put the value of the env variable PORT if it exist
    # (some services only open specifiques ports)
    port = int(os.environ.get('PORT', 5000))
    # Threaded option to enable multiple instances for
    # multiple user access support
    # You will also define the host to "0.0.0.0" because localhost
    # will only be reachable from inside de server.
    app.run(host="0.0.0.0", threaded=True, port=port)
