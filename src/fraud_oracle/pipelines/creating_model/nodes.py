import pandas as pd
import os
import shutil
import zipfile
from autogluon.tabular import TabularPredictor
from fraud_oracle.utils import get_drive_service, validate_data, generate_short_uuid, generate_filename
from tools import download_file, upload_zip_file, download_zip_file
from sklearn.metrics import classification_report
import wandb

model_path = "tmp/tabular_model"

target_column = 'FraudFound_P'

zip_file = 'tmp/tabular_model.zip'

unzipped_dir = 'unzipped_model'

excepted_number_of_columns_test_data = 1

excepted_names_of_columns_test_data = ['FraudFound_P']

excepted_number_of_columns_train_data = 15

excepted_names_of_columns_train_data = ['Month','WeekOfMonth','Make','AccidentArea','MonthClaimed','MaritalStatus','Fault','PolicyType','VehicleCategory',
                                        'Deductible','PoliceReportFiled','AgentType','AddressChange_Claim','Year','BasePolicy']

def download_train_and_test_data_csv(file_id):

    print(f"Przetwarzam plik o ID: {file_id}")
    drive_service = get_drive_service()

    if file_id == 'default_id':
        suffix = None
    else:
        suffix = file_id

    X_train_cloud = download_file(suffix=suffix, folder_name='X_train_data', destination_path='tmp/X_train_data.csv', drive_service=drive_service)
    y_train_cloud = download_file(suffix=suffix, folder_name='y_train_data', destination_path='tmp/y_train_data.csv', drive_service=drive_service)
    X_test_cloud = download_file(suffix=suffix, folder_name='X_test_data', destination_path='tmp/X_test_data.csv', drive_service=drive_service)
    y_test_cloud = download_file(suffix=suffix, folder_name='y_test_data', destination_path='tmp/y_test_data.csv', drive_service=drive_service)
    
    return X_train_cloud, X_test_cloud, y_train_cloud, y_test_cloud
    

def check_X_test_data(X_test_data : pd.DataFrame):
   validate_data(X_test_data, excepted_number_of_columns_train_data, excepted_names_of_columns_train_data)


def check_y_test_data(y_test_data : pd.DataFrame):
    validate_data(y_test_data, excepted_number_of_columns_test_data, excepted_names_of_columns_test_data)

def check_test_data(X_test_cloud : pd.DataFrame, y_test_cloud : pd.DataFrame):
   check_X_test_data(X_test_cloud)
   check_y_test_data(y_test_cloud)
   validate_row_count(X_test_cloud, y_test_cloud)

   return X_test_cloud, y_test_cloud


def check_X_train_data(X_train_data : pd.DataFrame):
    validate_data(X_train_data, excepted_number_of_columns_train_data, excepted_names_of_columns_train_data)
def check_y_train_data(y_train_data : pd.DataFrame):
    validate_data(y_train_data, excepted_number_of_columns_test_data, excepted_names_of_columns_test_data)

def check_train_data(X_train_cloud : pd.DataFrame, y_train_cloud : pd.DataFrame):
   check_X_train_data(X_train_cloud)
   check_y_train_data(y_train_cloud)
   validate_row_count(X_train_cloud, y_train_cloud)

   return X_train_cloud, y_train_cloud

def validate_row_count(df1, df2):
    if len(df1) != len(df2):
        raise ValueError(f"Liczba wierszy się nie zgadza: {len(df1)} != {len(df2)}")
    return df1, df2

def train_model(X_train, y_train):

    os.makedirs(model_path, exist_ok=True)

    train_data = pd.concat([X_train, y_train], axis=1)

    predictor = TabularPredictor(label=target_column, eval_metric='f1', path=model_path).fit(
        train_data=train_data,
        ag_args_fit={'random_seed': 42},
        presets='high_quality',
        hyperparameters={
            'XGB': {'scale_pos_weight': 12},
            'CAT': {'auto_class_weights': 'Balanced'},
            'GBM': {'is_unbalance': True}
        }
    )

    shutil.make_archive(base_name=model_path, format='zip', root_dir=model_path)
    print(f"Model spakowany do: {model_path}.zip")
    
    model_id = generate_short_uuid()

    upload_zip_file(zip_file, name=generate_filename(base_name='tabular_model', id=model_id), folder_name='models', drive_service=get_drive_service())

    return model_id


def test_model(model_id, X_test, y_test):
    print(f"Model id: {model_id}")

    download_zip_file(suffix=model_id, folder_name='models', destination_path=zip_file, drive_service=get_drive_service())

    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(unzipped_dir)

    print(f"Model rozpakowany do: {unzipped_dir}")

    loaded_predictor = TabularPredictor.load(unzipped_dir)
    print("Model został wczytany z ZIP-a!")

    predictions = loaded_predictor.predict(X_test)

    # Raport klasyfikacji – precyzja, czułość, F1 dla każdej klasy
    report = classification_report(y_test, predictions, digits=4, output_dict=True)
    print("Raport klasyfikacji:\n", report)

    return report


def log_metrics(flattened_metrics):
    # Logowanie do W&B
    wandb.init(project="fraud_oracle")
    # Zamiana słownika na DataFrame
    df_report = pd.DataFrame(flattened_metrics).transpose()

    # Logowanie jako tabela
    wandb.log({"classification_report": wandb.Table(dataframe=df_report)})
    wandb.finish()
