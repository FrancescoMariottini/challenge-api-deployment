# Challenge-api-deployment
The real estate company ['ImmoEliza'](https://immoelissa.be/) was really happy about our previously made regression model. They would like you to create an API to let their web-devs create a website around it.

# Description (why)
Housing prices prediction is an essential element for an economy. Analysis of price ranges influence both sellers and buyers. 

Our [previous project](https://github.com/FrancescoMariottini/Belgium-prices-prediction/settings) created a Linear Regression model to estimate the price of the house accurately with the given features. Within this project an online API to run the price prediction is made. 

# Target audience (to whom)
['ImmoEliza'](https://immoelissa.be/) web developers to receive price prediction based on input values provided by a user.

# Objectives (what)
1. Be able to deploy a machine learning model.
2. Be able to create a Flask API that can handle a machine learning model.
3. Deploy an API to Heroku with Docker.

Project evalution is based on the compliance to the following criteria:

Criteria	Indicator |	Yes/No
--- | ---
1. Is complete	|Your API works.	
|Your API is wrapped in a Docker image.
|Pimp up the readme. (what, why, how, who).
|Your model predict.
|Your API is deployed on Heroku.
2. Is good |The repo doesn't contain unnecessary files.
|You used typing.	
|The presentation is clean.	
|The web-dev group understood well how your API works.


# Development (how)
Input requirements for the web developers were initially agreed with the other Becode teams. Then the team agreed on how to fulfill and split the required development steps among its members. Step 0 (team management) was added.

## Input requirements
Hereby follow the agreed requirements for the json to be provided by the web developers:

```json
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
```
Output requirements were not strictly fixed but rather delegated to each team after sharing a reference template:

```json
{
    "prediction": Optional[float],
    "error": Optional[str]
}
```
A HTTP status code is also provided in case of error.

## Step 1: Project preparation ##
Demanded requirements were: 
Create a folder to handle your project.
Create a file app.py that will contain the code for your API.
Create a folder preprocessing that will contain all the code to preprocess your data.
Create a folder model that will contain your model.
Create a folder predict that will contain all the code to predict a price.
Step 2: Pre-processing pipeline
This python module will contain all the code to preprocess your data. Make sure to think about what will be the format of your data to fit the model. Also, be sure to know which information HAVE to be there and which one can be empty (NAN).

In preprocessing folder:

Create a file cleaning_data.py that will contain all the code that will be used to preprocess the data you will receive to predict a new price. (fill the nan, handle text data,...).
Your file should contain a function preprocess() that will take a new house's data as input and return those data preprocessed as output.
If your data doesn't contain the required information, you should return an error to the user.
Step 3: Fit your data!
Fit your data to your model.

In the predict folder:

Create a file prediction.py that will contain all the code used to predict a new house's price.
Your file should contain a function predict() that will take your preprocessed data as an input and return a price as output.
Step 4: Create your API
In your app.py file, create a Flask API that contains:

A route at / that accept:
GET request and return "alive" if the server is alive.
A route at /predict that accept:
POST request that receives the data of a house in json format.
GET request returning a string to explain what the POST expect (data and format).
Step 5: Create a Dockerfile to wrap your API
To deploy your API, you will use Docker.

Create a Dockerfile that creates an image with:
Ubuntu
Python 3.8
Flask
All the other dependencies you will need
All the files of your project in an /app folder that you will previously create.
Run your app.py file with python
Step 6: Deploy your Docker image in Heroku
Heroku will allow you to push your docker container on their server and to start it.

#### Date of Completion: 
8/12/2020 (code)
14/12/2020 (presentation)

# Team:
Ankita
Francesco
Opaps
Philippe
