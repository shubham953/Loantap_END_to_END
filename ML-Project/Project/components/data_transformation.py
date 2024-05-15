import sys
sys.path.append('D:\Desktop\Loantap_END_to_END_CI_CD_MlOps_AWS\ML-Project')
import os
from Project import logger
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from Project.entity.config_entity import DataTransformationConfig
from sklearn.preprocessing import OrdinalEncoder
global total_acc_avg
class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    
    def fill_mort_acc(self,total_acc, mort_acc):

        if (np.isnan(mort_acc) or str(mort_acc)=='np.nan'):
            return total_acc_avg[total_acc].round()
        else:
            return mort_acc
        


    def Transformed_data(self):
        
        data = pd.read_csv(self.config.data_path)
        
         # Dropping rows with null values - # do your own research
        


        numerical_data = data.select_dtypes(include='number')

        num_cols = numerical_data.columns

        for col in num_cols:

            mean = data[col].mean()

            std = data[col].std()

            upper_limit = mean+3*std

            lower_limit = mean-3*std

            

            data = data[(data[col]<upper_limit) & (data[col]>lower_limit)]

        #IMPUTATION
        global total_acc_avg
        total_acc_avg = data.groupby(by='total_acc')['mort_acc'].median()

        data['mort_acc'] = data.apply(lambda x: self.fill_mort_acc(x['total_acc'], x['mort_acc']),axis=1)

        data['term']=data['term'].str.rsplit(' ',n= 1).str[0]
        data['term']=data['term'].str.lstrip(' ')
        data['term']=data['term'].astype(int) 
        data['emp_length']=data['emp_length'].replace({'< 1 year':0, '1 year':1, '2 years':2, '3 years':3, '4 years':4, '5 years':5,'6 years':6, '7 years':7, '8 years':8, '9 years':9, '10+ years':10})
        data['initial_list_status'] = data.initial_list_status.replace({'w':0,'f':1})
        data.dropna(inplace=True)
        #droping columns for make prediction easier at app.py you can make good score but in this 
        #the purpose is to deployee the model with fair f1 score
        data.drop(columns=['installment'], axis=1, inplace=True)
        data.drop(columns=['address'], axis=1, inplace=True)
        data.drop(columns=['issue_d', 'emp_title', 'title', 'earliest_cr_line','home_ownership','verification_status', 'application_type','purpose'], axis=1, inplace=True)

        label_grade = sorted(data.grade.unique())[::-1]
        label_sgrade = sorted(data.sub_grade.unique())[::-1]
        ord_enc = OrdinalEncoder(categories = [label_grade])
        ord_enc1 = OrdinalEncoder(categories = [label_sgrade])
        ord_enc.fit(data[['grade']])

        ord_enc1.fit(data[['sub_grade']])

        data['grade'] = ord_enc.transform(data[['grade']])

        data['sub_grade'] = ord_enc1.transform(data[['sub_grade']])



        # dummies = [ 'verification_status', 'application_type','purpose']

        # data = pd.get_dummies(data, columns=dummies, drop_first=True)
            # Saving mean of mort_acc according to total_acc_avg
            # Split the data into training and test sets. (0.75, 0.25) split.
        train, test = train_test_split(data)

        train.to_csv(os.path.join(self.config.root_dir, "train.csv"),index = False)

        test.to_csv(os.path.join(self.config.root_dir, "test.csv"),index = False)

        logger.info("Splited data into training and test sets")

        logger.info(train.shape)

        logger.info(test.shape)

        print(train.shape)

        print(test.shape)