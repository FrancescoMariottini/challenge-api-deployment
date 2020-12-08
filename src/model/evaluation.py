import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

class Model_Evaluation:

    def __init__(self, model):

        self.model = model

    def get_predictions(self, train_data, test_data):
        """
        Function provides predicted values from train dataset and test dataset.

        :param test_data: an array that contains test dataset
        :param train_data: an array that contains train dataset

        :return: array of predicted train and test dataset
        """

        train_predictions = self.model.predict(train_data)
        test_predictions = self.model.predict(test_data)

        return train_predictions, test_predictions

    def predict_model(self, X_train, y_train, X_test, y_test):
        """
        Function generates evaluation dataset on original inputs and predicted dataset.
        :param X_train: an array that contains training dataset to be preticted
        :param y_train: an array that contains training target dataset
        :param X_test: an array that contains testing dataset to be predicted
        :param y_test: an array that contains testing target dataset
        """

        ytrain_predictions, ytest_predictions = self.get_predictions(X_train, X_test)

        mae = mean_absolute_error(y_test, ytest_predictions)

        mse = mean_squared_error(y_test, ytest_predictions)
        rmse = np.sqrt(mse)
        mape = (mse/y_test)*100
        train_score = r2_score(y_train, ytrain_predictions)
        test_score = r2_score(y_test, ytest_predictions)

        Results = pd.DataFrame({'MAE': mae, 'MSE': mse, 'RMSE': rmse,
                                'Train_RSquare': train_score, 'Test_RSquare': test_score}, index=['Values'])
        print('Evaluation Metrics')
        print(tabulate(Results, headers='keys', tablefmt='fancy_grid'))

        plt.subplot(1, 2, 1)
        # display plots
        plt.title('Actual vs Predicted Data\n')
        plt.scatter(y_test, ytest_predictions, c=np.arange(len(y_test)),cmap='Blues')

        plt.xlabel('Predicted')
        plt.ylabel('Actual')

        plt.subplot(1, 2, 2)
        plt.title('Residuals Distribution Plot\n')
        # histogram of the residuals. It tells how well the residuals are distributed from proposed model
        # FM 8/12/20 distplot deprecated to be replaced
        residuals = ytest_predictions - y_test
        # histogram of the residuals. It tells how well the residuals are distributed from proposed model
        # FM 8/12/20 distplot deprecated to be replaced
        sns.distplot(residuals)
        plt.tight_layout()
        plt.show()
        residuals_dsc = residuals.describe(percentiles=[0.975, 0.025])
        mae = median_absolute_error(y_test, ytest_predictions)
        me = max_error(y_test, ytest_predictions)
        p025, p975 = residuals_dsc['2.5%'], residuals_dsc['97.5%']
        metrics_values = [str(int(m)) for m in [len(residuals), mae, me, p025, p975]]
        metrics_keys = ['test_size', 'median_absolute_error', 'max_error', 'percentile025', 'percentile975']
        # FM 7/12/20  return error
        return y_test, ytest_predictions, dict(zip(metrics_keys, metrics_values))
