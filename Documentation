TODO 
1. Add default route
2. Update the api route in the doc
3. double check Jsons exposed

# Title of the API

This API version of the API (1.0) exposes serveral routes to get predictions on the price of real estate.
Access to routes doesn't need any kind of authentification.
To get a prediction you need to provide several parameters, some are mandatory other are optional. 

## Summary

1. Requests:
1.1. Alive
1.2. Predict
2. Objects
2.1. Request object 
2.2. Response object
3. Errors

# /

## Allowed HTTP Methods

- GET - Returns "alive" if the server is alive.

## Ressource Information

- Authentication - Not required
- Request Object - None
- Response Format - string
- API Version - 1.0
- Resource URI - https://api.tobedefined.com

# /Predict 

## Allowed HTTP Methods

- GET - Request returning a string to explain what the POST expect (data and format).
- POST - Receives a Json data object and returns a prediction of price or an error message. 

## Resource Information

- Authentication - Not required
- Request Object - data
- Response Format - Json
- Response Object - price-wrapper
- API Version - 1.0
- Resource URI - https://api.tobedefined.com

## Request Object

{
    "data": {
            "area": int,
            "property-type": "APARTMENT" | "HOUSE" | "OTHERS",
            "rooms-number": int,
            "zip-code": int,
            "land-area": Optional[int],
            "garden": Optional[bool],
            "garden-area": Optional[int],
            "equipped-kitchen": Optional[bool],
            "full-address": Optional[str],
            "swimmingpool": Opional[bool],
            "furnished": Opional[bool],
            "open-fire": Optional[bool],
            "terrace": Optional[bool],
            "terrace-area": Optional[int],
            "facades-number": Optional[int],
            "building-state": Optional["NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO REBUILD"]
    }
} 

## Response Object

{
    "price-wrapper": {
            "prediction": Optional[float],
            "error": Optional[str]
    }
}

## Example Request

1. Get a string to explain what the POST expects (data and format):

GET https://api.tobedefined.com/predict

2. Get a prediction:

POST https://api.tobedefined.com/predict



{
    "data": {
            "area": 150,
            "property-type": "APARTMENT",
            "rooms-number": 2,
            "zip-code": 1000,
            "open-fire": true,
            "terrace": false,
            "terrace-area": 50,
            "facades-number": 4,
            "building-state":"TO RENOVATE"
    }
} 
// Note you can ommit some parameters in the Json file if they are `Optional`

**return object**

{
    "price-wrapper": {
            "prediction": 259451            
    }
}

# Request object 

All strings are not case sensitive.

Name|Type|Mandatory|Description|validation
area|int|yes|Amount of m² of the property| must be higher than 0
property-type|string|yes| Type of the property| must be an "apartment", "house" or "others"   
rooms-number|int|yes|The amount of rooms in the property| must be higher than 0
zip-code|int|yes|postcode of the property | must be between 1000 and 9999
land-area|int|no|Amount of m² of the whole plot (garden included)| must be higher than 0
garden|bool|no|Incidcates wheter or not the property has a garden| 
garden-area|int|Amount of m² of the garden|must be higher than 0
equipped-kitchen|bool|no|Incidcates wheter or not the property has an equipped kitchen|
full-address|string|no|Full address of the property|
swimmingpool|bool|no|Incidcates wheter or not the property has a swimmingpool|
furnished|bool|no|Incidcates wheter or not the property is furnished|
open-fire|bool|no|Incidcates wheter or not the property an open fire installed|
terrace|bool|no|Incidcates wheter or not the property a terrace|
terrace-area|int|no|Amount of m² of the terrace| must be higher than 0
facades-number|int|no|Amount of facades of the property|must be higher than 0
building-state|string|no|Current state of the property| must be part of the following values ["NEW" | "GOOD" | "TO RENOVATE" | "JUST RENOVATED" | "TO REBUILD"]

# Return object 

Name|Type|Mandatory|Description
prediction|float|no|The price predicted by our model based on the info you provided
error|string|no|If something didn't go right in the prediction, we'll let you know through this message


# Errors

When requesting our API you will always get a HTTP Status codes, here's a list of the ones you might encounter and what they mean.

- 200 `OK` Means the request was accepeted, you will get the expected output.
- 400 `Bad Request` Whenever something goes wrong with your request, e.g. your POST data and/or structure is wrong, a 400 Bad Request HTTP status is returned, describing the error within the content.
- 405 `error` Indicates that the URI you provided can't be mapped.
- 500 `Internal server error` It means there is somehting wrong with our code, please contact us in such a situation.

