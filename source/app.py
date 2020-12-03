
from flask import Flask,request, jsonify
#import DataFeatures
#from source.preprocessing import cleaning_data
#from source.predict import prediction
import prediction

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
        #data = DataFeatures()
        #errors = data.validate(datadict)
        #if errors:
        #    abort(BAD_REQUEST, str(errors)) 
        ##get the required parameters
        #processeddata = cleaning_data.preprocess(datadict)
        #predicted_price = { "Estimated price" : prediction.predict_price(processeddata)
        #              }
        predicted_price = { "Estimated price" : prediction.predict_price(datadict)
                          }
        return jsonify(predicted_price)
        

if __name__ == "__main__":
    app.run()
