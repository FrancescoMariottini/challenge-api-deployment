

# Immo Elisa API Documentation

![.](https://tovodata.com/wp-content/uploads/sites/77/2020/08/animation_640_kdmubtw7.gif)

This API version of the API (1.0) exposes serveral routes to get predictions on the price of real estate.
Access to routes doesn't need any kind of authentification.
To get a prediction you need to provide several parameters, some are mandatory other are optional. 
The more parameters your provide the better the prediction will be.
The Base url is roberta-eliza.herokuapp.com.

## Summary

1. Requests<br>
1.1. [Alive](#alive)<br>
1.2. [Predict](#predict)<br>
2. Entities<br>
2.1. [Request entity](#Request-entity) <br>
2.2. [Response entity](#Return-entity)<br>
3. [Errors](#Errors)<br>

# Alive

## Allowed HTTP Methods

- GET - Returns "alive" string if the server is alive.

## Ressource Information

- Authentication - Not required
- Request Object - None
- Response Format - string
- API Version - 1.0
- Resource URI - roberta-eliza.herokuapp.com/

# Predict 

## Allowed HTTP Methods

- GET - Request returning a string to explain what the POST expect (data and format).
- POST - Receives a Json data object and returns a prediction of price or an error message. 

## Resource Information

- Authentication - Not required
- Request Format -  Json
- Request Object - [data](#Request-entity)
- Response Format - Json
- Response Object - [price-wrapper](#Return-entity)
- API Version - 1.0
- Resource URI - roberta-eliza.herokuapp.com/predict

## Request Entity Json


<pre>
{ <br /> 
  "data": { <br />
            "area": int,<br>
            "property-type": "APARTMENT" | "HOUSE" | "OTHERS",<br>
            "rooms-number": int,<br>
            "zip-code": int,<br>
            "land-area": Optional[int],<br>
            "garden": Optional[bool],<br>
            "garden-area": Optional[int],<br>
            "equipped-kitchen": Optional[bool],<br>
            "full-address": Optional[str],<br>
            "swimmingpool": Opional[bool],<br>
            "furnished": Opional[bool],<br>
            "open-fire": Optional[bool],<br>
            "terrace": Optional[bool],<br>
            "terrace-area": Optional[int],<br>
            "facades-number": Optional[int],<br>
            "building-state": Optional["NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO REBUILD"]<br>
    }<br>
} </pre>

## Response Entity format

<pre>
response = {
  prediction: {
    price: int,
    test_size: int,
    median_absolute_error: float,
    max_error: float,
    percentile025: float,
    percentile975: float
  },
  error: str
}
</pre>

## Example Request

1. Get a string to explain what the POST expects (data and format):

GET roberta-eliza.herokuapp.com/predict

2. Get a prediction:

POST roberta-eliza.herokuapp.com/predict


<pre>
{<br>
    "data": {<br>
            "area": 150,<br>
            "property-type": "APARTMENT",<br>
            "rooms-number": 2,<br>
            "zip-code": 1000,<br>
            "open-fire": true,<br>
            "terrace": false,<br>
            "terrace-area": 50,<br>
            "facades-number": 4,<br>
            "building-state":"TO RENOVATE"<br>
    }<br>
} <br>
</pre>
// Note you can ommit some parameters in the Json file if they are `Optional`

Response :

<pre>
response = {
  prediction: {
    price: 190000,
    test_size: 5,
    median_absolute_error: 25314.01,
    max_error: 2548.01,
    percentile025: 124.12,
    percentile975: 13485.12
  }
}
</pre>

// Note that there is no error when the request succeeds.


# Request entity 

All strings are not case sensitive.

Name|Type|Mandatory|Description|validation
---|---|---|---|---
area|int|yes|Amount of m² of the property| must be higher than 0
property-type|string|yes| Type of the property| must be an "apartment", "house" or "others"   
rooms-number|int|yes|The amount of rooms in the property| must be higher than 0
zip-code|int|yes|postcode of the property | must be between 1000 and 9999
land-area|int|no|Amount of m² of the whole plot (garden included)| must be higher than 0
garden|bool|no|Incidcates wheter or not the property has a garden| 
garden-area|int|no|Amount of m² of the garden|must be higher than 0
equipped-kitchen|bool|no|Indicates whether or not the property has an equipped kitchen|
full-address|string|no|Full address of the property|
swimmingpool|bool|no|Indicates whether or not the property has a swimmingpool|
furnished|bool|no|Indicates whether or not the property is furnished|
open-fire|bool|no|Indicates whether or not the property an open fire installed|
terrace|bool|no|Indicates whether or not the property a terrace|
terrace-area|int|no|Amount of m² of the terrace| must be higher than 0
facades-number|int|no|Amount of facades of the property|must be higher than 0
building-state|string|no|Current state of the property|Must be one of these values: ["NEW", "GOOD", "TO RENOVATE", "JUST RENOVATED", "TO REBUILD"]

# Return entity 

the response object has two sub objects the `error` containing an error message if there is one and the prediction object containing the prediction and other useful information.

Name|Type|Description
---|---|---
price|int|The price predicted by our model based on the info you provided
test_size|int|The number of properties used to test the model performance
median_absolute_error|float|The maximum absolute error between the prediction and test real values for 50% of the tested properties
max_error|float|The maximum absolute error when considering the entire test dataset of properties
percentile025|float| minimum negative error when considering 95% of the properties (around the median) in the test dataset
percentile975|float| maximum positive error when considering 95% of the properties (around the median) in the test dataset 



# Errors

When requesting our API you will always get a HTTP Status codes, here's a list of the ones you might encounter and what they mean.

- 200 `OK` Means the request was accepeted, you will get the expected output.
- 400 `Bad Request` Whenever something goes wrong with your request, e.g. your POST data and/or structure is wrong, a 400 Bad Request HTTP status is returned, describing the error within the content.
- 404 `error` Indicates that the URI you provided can't be mapped.
- 500 `Internal server error` It means there is somehting wrong with our code, please contact us in such a situation.

## Specific error handling for the predict route

![.](https://media.discordapp.net/attachments/762942794183999539/785888441699008512/uml_roberta-eliza.png?width=413&height=905)
