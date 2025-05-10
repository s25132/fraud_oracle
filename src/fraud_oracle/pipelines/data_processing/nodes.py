import pandas as pd
import os
from fraud_oracle.utils import get_drive_service, validate_data, get_train_and_test_sets, generate_filename, generate_short_uuid
from tools import download_file, upload_file


def download_data_csv() -> pd.DataFrame:
    drive_service = get_drive_service()

    os.makedirs('tmp', exist_ok=True)
    data = download_file(suffix='fraud_oracle', folder_name='raw_data', destination_path='tmp/fraud_oracle.csv', drive_service=drive_service)
    
    return data



def check_data(data : pd.DataFrame):

    excepted_number_of_columns = 33

    excepted_names_of_columns = [
        'Month', 'WeekOfMonth', 'DayOfWeek', 'Make', 'AccidentArea',
        'DayOfWeekClaimed', 'MonthClaimed', 'WeekOfMonthClaimed', 'Sex',
        'MaritalStatus', 'Age', 'Fault', 'PolicyType', 'VehicleCategory',
        'VehiclePrice', 'FraudFound_P', 'PolicyNumber', 'RepNumber',
        'Deductible', 'DriverRating', 'Days_Policy_Accident',
        'Days_Policy_Claim', 'PastNumberOfClaims', 'AgeOfVehicle',
        'AgeOfPolicyHolder', 'PoliceReportFiled', 'WitnessPresent',
        'AgentType', 'NumberOfSuppliments', 'AddressChange_Claim',
        'NumberOfCars', 'Year', 'BasePolicy'
        ]


    validate_data(data, excepted_number_of_columns, excepted_names_of_columns)

    return data

def clean_data(data : pd.DataFrame):

    columns_to_drop = [
        'PolicyNumber',
        'AgeOfPolicyHolder',
        'WeekOfMonthClaimed',
        'DayOfWeek',
        'VehiclePrice',
        'DayOfWeekClaimed',
        'NumberOfSuppliments',
        'AgeOfVehicle',
        'DriverRating',
        'PastNumberOfClaims',
        'Age',
        'Sex',
        'Days_Policy_Claim',
        'NumberOfCars',
        'RepNumber',
        'Days_Policy_Accident',
        'WitnessPresent'
    ]

    data = data.drop(columns=columns_to_drop)

    return data


def create_train_and_test_data(data : pd.DataFrame):
    target_column = "FraudFound_P"
    X_train, X_test, y_train, y_test = get_train_and_test_sets(data, target_column)
    
    return X_train, X_test, y_train, y_test


def upload_train_and_test_data(X_train : pd.DataFrame, X_test: pd.DataFrame, y_train : pd.DataFrame, y_test: pd.DataFrame):
    
    drive_service = get_drive_service()
    id = generate_short_uuid()
    print("Uploading data with id " + id)
    upload_file(dataset=X_train, name=generate_filename(base_name='X_train', id=id), folder_name='X_train_data', drive_service=drive_service)
    upload_file(dataset=y_train, name=generate_filename(base_name='y_train', id=id), folder_name='y_train_data', drive_service=drive_service)
    upload_file(dataset=X_test, name=generate_filename(base_name='X_test', id=id), folder_name='X_test_data', drive_service=drive_service)
    upload_file(dataset=y_test, name=generate_filename(base_name='y_test', id=id), folder_name='y_test_data', drive_service=drive_service)
    
