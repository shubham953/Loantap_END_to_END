import sys
sys.path.append('D:\Desktop\Loantap_END_to_END_CI_CD_MlOps_AWS\ML-Project')
import pandas as pd
import os
from Project import logger

import joblib
from Project.entity.config_entity import ModelTrainerConfig
from sklearn.tree import DecisionTreeClassifier


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


        tree_clf = DecisionTreeClassifier(criterion='entropy', max_depth=2)
        tree_clf.fit(  train_x,   train_y)
       

        joblib.dump(tree_clf, os.path.join(self.config.root_dir, self.config.model_name))