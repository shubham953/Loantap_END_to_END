import sys
sys.path.append('D:\Desktop\Loantap_END_to_END_CI_CD_MlOps_AWS\ML-Project')
from flask import Flask, render_template, request
import os 
import numpy as np
import pandas as pd
from Project.pipeline.prediction import PredictionPipeline
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    data = [
    request.form['loanAmount'],
    request.form['term'],
    request.form['intRate'],
    request.form['grade'],
    request.form['subGrade'],
    
    request.form['empLength'],
   
    request.form['annualInc'],

    request.form['dti'],

   
   

    
    
    
    request.form['openAcc'],
    request.form['pubRec'],
    request.form['revolBal'],
    request.form['revolUtil'],
    request.form['totalAcc'],
    request.form['initialListStatus'],
    
    request.form['mortAcc'],
    request.form['pubRecBankruptcies']
    ]

    
    data['grade'] = ord_enc.transform(data[['grade']])
    data['sub_grade'] = ord_enc1.transform(data[['sub_grade']])

    data['grade']=data['grade'].astype(float)
    data['sub_grade']=data['subgrade'].astype(float)
    
    scaler= joblib.load("artifacts\model_trainer\model.joblib")
    
    
    
    data = scaler.transform(data)


# Perform prediction or any other processing here
# For example:
    try:
        obj = PredictionPipeline()
        predict = obj.predict(data)
        if predict == 0:
            pred = "Rejected"
        elif(predict==1):
            pred = "Approved"
        else:
            pred = "wrong input"  

        return render_template('result.html', prediction_result=pred)
      
    except:
         return render_template('result.html')
    
    # return render_template('results.html', prediction = str(predict))




if __name__ == "__main__":
	app.run(host="0.0.0.0", port = 8080)