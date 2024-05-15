import sys
sys.path.append('D:\Desktop\Loantap_END_to_END_CI_CD_MlOps_AWS\ML-Project')
import os
from Project import logger

import pandas as pd
from Project.entity.config_entity import Datafeature_engineeringConfig


class Feature_Engineering:
    def __init__(self, config: Datafeature_engineeringConfig):

        self.config = config  

    def get_data(self):      
        def pub_rec(number):
            if number == 0.0:
                return 0
            else:
                return 1
        def mort_acc(number):
            if number == 0.0:
                return 0
            elif number >= 1.0:
                return 1
            else:
                return number

        data = pd.read_csv("artifacts\data_ingestion\LoanTap.csv")

        data['mort_acc'] = data.mort_acc.apply(mort_acc)
        data['pub_rec_bankruptcies'] = data.pub_rec_bankruptcies.apply(pub_rec)

        data['term']=data['term'].str.rsplit(' ',n= 1).str[0]
        data['term']=data['term'].str.lstrip(' ')
        data['term']=data['term'].astype(int) 
        data['emp_length']=data['emp_length'].replace({'< 1 year':0, '1 year':1, '2 years':2, '3 years':3, '4 years':4, '5 years':5,'6 years':6, '7 years':7, '8 years':8, '9 years':9, '10+ years':10})
        data['initial_list_status'] = data.initial_list_status.replace({'w':0,'f':1})
        data.dropna(inplace=True)

        
        data['initial_list_status'] = data.initial_list_status.replace({'w':0,'f':1})
        
        print(self.config.data_path)

        #maping of target variable
        data['loan_status'] = data.loan_status.map({'Fully Paid':0, 'Charged Off':1})
        
        data.to_csv(os.path.join(self.config.root_dir, "featured_data.csv"),index = False)
        logger.info("Feature engineering completed")
        logger.info(data.shape)
        

            