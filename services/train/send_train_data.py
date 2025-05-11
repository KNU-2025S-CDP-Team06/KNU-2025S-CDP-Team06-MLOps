import sys
import train_utils

def send_cluster_data():
    category = sys._getframe().f_code.co_name.split('_')[1]
    train_utils.integration(category)

def send_prophet_data():
    category = sys._getframe().f_code.co_name.split('_')[1]
    train_utils.integration(category)

def send_xgboost_data():
    category = sys._getframe().f_code.co_name.split('_')[1]
    train_utils.integration(category)
