import sys
sys.path.append('D:\Desktop\Loantap_END_to_END_CI_CD_MlOps_AWS\ML-Project')
import pandas as pd
import os
from Project import logger
import pandas as pd
import joblib
from Project.entity.config_entity import ModelTrainerConfig
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config


    
    def train(self):
        data = pd.read_csv(self.config.train_data_path)
        
        X = data.drop('loan_status', axis=1)
        y = data['loan_status']

        SmoteBL = SMOTE(k_neighbors=5)
        X_smote , y_smote = SmoteBL.fit_resample(X,y)

        train_x, test_x, train_y, test_y = train_test_split(X_smote, y_smote, test_size=0.30,stratify=y_smote, random_state=42)

                
        scaler = StandardScaler()
        train_x = scaler.fit_transform(train_x)
        test_x  = scaler.transform(test_x)


        tree_clf = DecisionTreeClassifier(criterion='entropy', max_depth=2)
        tree_clf.fit(  train_x,   train_y)
        np.save(os.path.join(self.config.root_dir, "test_x"),test_x)
        np.save(os.path.join(self.config.root_dir, "test_y"),test_y)
       
        joblib.dump(scaler, os.path.join(self.config.root_dir, self.config.scaler_name))
        joblib.dump(tree_clf, os.path.join(self.config.root_dir, self.config.model_name))