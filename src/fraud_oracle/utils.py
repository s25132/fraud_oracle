import os
import uuid
from google.oauth2 import service_account
from googleapiclient.discovery import build
from sklearn.model_selection import train_test_split


def get_drive_service():

    credentials_path = os.getenv("GOOGLE_CREDENTIALS")
    if not credentials_path:
        raise ValueError("Missing GOOGLE_CREDENTIALS environment variable")
    
    SCOPES = ['https://www.googleapis.com/auth/drive']

    # Create credentials using the service account file
    credentials = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)

    # Build the Google Drive service
    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service



def check_number_of_columns(data, expected_number_of_columns):
    return data.shape[1] == expected_number_of_columns

def check_names_of_columns(data, expected_names_list):
    return list(data.columns) == expected_names_list

def check_null_data(data):
    return (data.isnull().sum() == 0).all()

def count_missing_values(data):
    for column in data.columns:
        null_values = data[column].isnull().sum()
        empty_values = (data[column] == "").sum()
        missing = null_values + empty_values
        print(f"{column}: {missing} brakujących wartości")

def check_empty_strings(data):
    return ((data == "").sum() == 0).all()

def validate_data(df, excepted_number_of_columns, excepted_names_of_columns):

    if(check_number_of_columns(df, excepted_number_of_columns)):
        print("Prawidłowa ilość kolumn")
    else:
        raise ValueError("Walidacja nie powiodła się: Zła ilość kolumn")

    if(check_names_of_columns(df, excepted_names_of_columns)):
        print("Prawidłowe nazwy kolumn")
    else:
        print("Złe nazwy kolumn")
        raise ValueError("Walidacja nie powiodła się: Złe nazwy kolumn")

    if(check_null_data(df)):
        print("Zbiór prawidłowy -> brak null")
    else:
        raise ValueError("Walidacja nie powiodła się: Zbiór prawidłowy -> brak null")

    if(check_empty_strings(df)):
        print("Zbiór prawidłowy -> nie mam pustych stringów")
    else:
        raise ValueError("Walidacja nie powiodła się: Wykryte puste wartości")
    
    return True


def get_train_and_test_sets(data, target_column):
    """
    Dzieli dane wejściowe na zbiór treningowy i testowy w proporcji 80/20.
    """
    X = data.drop(columns=[target_column])
    y = data[target_column]
    return train_test_split(X, y, test_size=0.2, random_state=123)

def generate_short_uuid():
    return str(uuid.uuid4())[:8]

def generate_filename(base_name: str, id : str):
    return f"{base_name}_{id}"