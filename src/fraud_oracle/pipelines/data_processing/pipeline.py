from kedro.pipeline import Pipeline, node, pipeline

from .nodes import download_data_csv, check_data, clean_data, create_train_and_test_data, upload_train_and_test_data


def create_pipeline(**kwargs) -> Pipeline:
      return pipeline([
        node(
            func=download_data_csv,
            inputs=None,
            outputs="fraud_oracle",
            name="download_csv_node"
        ),
        node(
            func=check_data,
            inputs='fraud_oracle',
            outputs=None,
            name="check_data_node"
        ),
        node(
            func=clean_data,
            inputs='fraud_oracle',
            outputs='fraud_oracle_clean',
            name="clean_data_node"
        ),
        node(
            func=create_train_and_test_data,
            inputs='fraud_oracle_clean',
            outputs=['X_train', 'X_test', 'y_train', 'y_test'],
            name="create_train_and_test_data_node"
        ),
        node(
            func=upload_train_and_test_data,
            inputs=['X_train', 'X_test', 'y_train', 'y_test'],
            outputs=None,
            name="upload_train_and_test_data_node"
        )
    ])
