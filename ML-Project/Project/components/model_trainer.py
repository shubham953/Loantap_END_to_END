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
class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config


    
    def train(self):
        train_data = pd.read_csv(self.config.train_data_path)
        test_data = pd.read_csv(self.config.test_data_path)


        train_x = train_data.drop([self.config.target_column], axis=1)
        test_x = test_data.drop([self.config.target_column], axis=1)
        train_y = train_data[[self.config.target_column]]
        test_y = test_data[[self.config.target_column]]

                
        scaler = StandardScaler()
        train_x = scaler.fit_transform(train_x)
        test_x  = scaler.transform(test_x)


        tree_clf = DecisionTreeClassifier(criterion='entropy', max_depth=2)
        tree_clf.fit(  train_x,   train_y)
        np.save(os.path.join(self.config.root_dir, "test_x"),test_x)
        np.save(os.path.join(self.config.root_dir, "test_y"),test_y)
       
        joblib.dump(scaler, os.path.join(self.config.root_dir, self.config.scaler_name))
        joblib.dump(tree_clf, os.path.join(self.config.root_dir, self.config.model_name))