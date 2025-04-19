from dagster import asset, AssetIn, AssetKey, Output, multi_asset, AssetOut, AssetExecutionContext
import pandas as pd
from sklearn.model_selection import train_test_split



@multi_asset(
    group_name="data_preparation",
    ins={"preprocessed_data": AssetIn(key=AssetKey("movies"),
        input_manager_key= "postgres_io_manager")
    },
    outs={
        "preprocessed_training_data": AssetOut(),
        "user2Idx": AssetOut(),
        "movie2Idx": AssetOut() 
    }
)
def preprocessed_data(context, preprocessed_data: pd.DataFrame):
    """
    Preprocesses the data for training the model.
    """
   # rows_count = len(preprocessed_data)

    user2Idx = {}
    movie2Idx = {}
    preprocessed_training_data = preprocessed_data.copy()
    
    return preprocessed_training_data, user2Idx, movie2Idx 

@multi_asset(
    group_name="data_preparation",
    ins={ "preprocessed_training_data": AssetIn()
    },
    outs={
        "X_train": AssetOut(),
        "X_test": AssetOut(),
        "y_train": AssetOut(),
        "y_test": AssetOut()
    }
)
def split_data(context: AssetExecutionContext, preprocessed_training_data):
    """
    Splits the data for training the model.
    """
    X_train, X_test, y_train, y_test = train_test_split(preprocessed_training_data, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test



@asset(
    group_name="model_training",
    ins={
        "X_train": AssetIn(),
        "y_train": AssetIn(),
        "user2Idx": AssetIn(),
        "movie2Idx": AssetIn(),
    }
)
def model_trained(context, X_train, y_train, user2Idx, movie2Idx):
    model = {}
    return model

@asset(
    group_name="model_training",
    ins={
        "model_trained": AssetIn(),
    }
)
def model_stored(context, model_trained):
    return ...


@asset(
    group_name="model_evaluation",
    ins={
        "model_stored": AssetIn(),
        "X_test": AssetIn(),
        "y_test": AssetIn(),
    }
)
def model_metrics(context, model_stored, X_test, y_test):
    return ...  
