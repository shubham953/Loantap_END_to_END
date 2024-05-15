import sys
sys.path.append('D:\Desktop\Loantap_END_to_END_CI_CD_MlOps_AWS\ML-Project')
import os
import pandas as pd
import numpy as np
import codecs, json 
from Project.utils.common import save_json
from urllib.parse import urlparse
import numpy as np
import joblib
from Project.entity.config_entity import ModelEvaluationConfig
from pathlib import Path
from sklearn.metrics import confusion_matrix, classification_report

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config

    def eval_metrics(self,actual, pred):
        classification = classification_report(actual, pred)
        confusion = confusion_matrix(actual, pred)
        
        return classification ,confusion




    def save_results(self):
            
        
        model = joblib.load(self.config.model_path)

        test_x = np.load(self.config.test_data_path_x)
        test_y = np.load(self.config.test_data_path_y)
        
        predicted_qualities = model.predict(test_x)

        (classification ,confusion) = self.eval_metrics(test_y, predicted_qualities)
        
        # Saving metrics as local
        scores = {"classification_report":classification ,"confusion_matrix":confusion}
     
        # Convert NumPy array to list
        confusion = confusion.tolist()

        scores = {"classification_report": classification, "confusion_matrix": confusion}

        # Writing the dictionary to a JSON file using Path
        json_file_path = Path(self.config.metric_file_name)
        with open(json_file_path, 'w') as json_file:
            json.dump(scores, json_file)
       