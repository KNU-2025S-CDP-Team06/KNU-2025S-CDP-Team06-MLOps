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

if __name__ == '__main__':
    argv = sys.argv
    if len(argv) != 2 or (argv[1] != "all" and argv[1] != 'cluster' and argv[1] != 'prophet' and argv[1] != 'xgboost'):
        print(f"usage: python {argv[0]} (all | cluster | prophet | xgboost)")
    else:
        if argv[1] == "all":
            send_cluster_data()
            send_prophet_data()
            send_xgboost_data()
        if argv[1] == "cluster":
            send_cluster_data()
        if argv[1] == "prophet":
            send_prophet_data()
        if argv[1] == "xgboost":
            send_xgboost_data()