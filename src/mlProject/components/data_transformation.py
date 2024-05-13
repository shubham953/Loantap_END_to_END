import os
from mlProject import logger
from sklearn.model_selection import train_test_split
import pandas as pd
from mlProject.entity.config_entity import DataTransformationConfig
from sklearn.preprocessing import OrdinalEncoder

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    
    def fill_mort_acc(total_acc, mort_acc):

        if (np.isnan(mort_acc) or str(mort_acc)=='np.nan'):
            return total_acc_avg[total_acc].round()
        else:
            return mort_acc
        
    def train_test_spliting(self):
        data = pd.read_csv(self.config.data_path)
        data.dropna(inplace=True)
    
    def fill_mort_acc(total_acc, mort_acc):

        if (np.isnan(mort_acc) or str(mort_acc)=='np.nan'):
            return total_acc_avg[total_acc].round()
        else:
            return mort_acc
    
    data = pd.read_csv(self.config.data_path)

    numerical_data = data.select_dtypes(include='number')

    num_cols = numerical_data.columns

    for col in num_cols:

        mean = data[col].mean()

        std = data[col].std()

        upper_limit = mean+3*std

        lower_limit = mean-3*std

        data.shape

        data = data[(data[col]<upper_limit) & (data[col]>lower_limit)]

    #IMPUTATION
    total_acc_avg = data.groupby(by='total_acc')['mort_acc'].median()

    data['mort_acc'] = data.apply(lambda x: self.fill_mort_acc(x['total_acc'], x['mort_acc']),axis=1)

        
    label_grade = sorted(data.grade.unique())[::-1]
    label_sgrade = sorted(data.sub_grade.unique())[::-1]

    ord_enc = OrdinalEncoder(categories = [label_grade])

    ord_enc1 = OrdinalEncoder(categories = [label_sgrade])

    ord_enc.fit(data[['grade']])

    ord_enc1.fit(data[['sub_grade']])

    data['grade'] = ord_enc.transform(data[['grade']])

    data['sub_grade'] = ord_enc1.transform(data[['sub_grade']])

    dummies = [ 'verification_status', 'application_type','purpose']

    data = pd.get_dummies(data, columns=dummies, drop_first=True)
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