from kedro.pipeline import Pipeline, node, pipeline

from .nodes import download_train_and_test_data_csv, check_test_data, check_train_data, train_model, test_model, log_metrics


def create_pipeline(**kwargs) -> Pipeline:
      return pipeline([
        node(
            func=download_train_and_test_data_csv,
            inputs='params:file_id',
            outputs=['X_train_cloud', 'X_test_cloud', 'y_train_cloud', 'y_test_cloud'],
            name="download_train_and_test_data_csv_node"
        ),       
         node(
            func=check_test_data,
            inputs=['X_test_cloud', 'y_test_cloud'],
            outputs=None,
            name="check_test_data_node"
        ),
        node(
            func=check_train_data,
            inputs=['X_train_cloud', 'y_train_cloud'],
            outputs=None,
            name="check_train_data_node"
        ),
        node(
            func=train_model,
            inputs=['X_train_cloud', 'y_train_cloud'],
            outputs='model_id',
            name="train_model_node"
        ),
        node(
            func=test_model,
            inputs=['model_id','X_test_cloud', 'y_test_cloud'],
            outputs='flattened_metrics',
            name="test_model_node"
        ),
        node(
            func=log_metrics,
            inputs='flattened_metrics',
            outputs=None,
            name="log_metrics_node"
        )
    ])
