
from flask import Flask, render_template, request
import os 
import numpy as np
import pandas as pd
from mlProject.pipeline.prediction import PredictionPipeline


app = Flask(__name__)

@app.route("/ping", methods=['GET'])
def ping():
    return {"message": "Hi there, I'm working!!"}
#defining the endpoint which will make the prediction
@app.route("/predict", methods=['POST'])
def prediction():
    """ Returns loan application status using ML model
    """
    loan_req = request.get_json()
    print(loan_req)
    if loan_req['Gender'] == "Male":
        Gender = 0
    else:
        Gender = 1
    if loan_req['Married'] == "Unmarried":
        Married = 0
    else:
        Married = 1
    if loan_req['Credit_History'] == "Unclear Debts":
        Credit_History = 0
    else:
        Credit_History = 1

    ApplicantIncome = loan_req['ApplicantIncome']
    LoanAmount = loan_req['LoanAmount']

    result = PredictionPipeline.predict([[Gender, Married, ApplicantIncome, LoanAmount, Credit_History]])

    if result == 0:
        pred = "Rejected"
    else:
        pred = "Approved"

    return {"loan_approval_status": pred}