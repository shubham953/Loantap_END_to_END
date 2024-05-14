import sys
sys.path.append('D:\Desktop\Loantap_END_to_END_CI_CD_MlOps_AWS\ML-Project')
from Project.config.configuration import ConfigurationManager
from Project.components.feature_engineering import Feature_Engineering
from Project import logger
from pathlib import Path



STAGE_NAME = "Data Feature Engineering stage"

class DataFeatureEngineeringPipeline:
    def __init__(self):
        pass


    def main(self):
        try:
            with open(Path("artifacts/data_validation/status.txt"), "r") as f:
                status = f.read().split(" ")[-1]

            if status == "True":
                config = ConfigurationManager()
                data_feature_engineering_config = config.get_data_transformation_config()
                data_feature_engineering = Feature_Engineering(config=data_feature_engineering_config)
                data_feature_engineering.get_data()

            else:
                raise Exception("You data schema is not valid")

        except Exception as e:
            print(e)