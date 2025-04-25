from dagster import asset, AssetIn, AssetKey, Output, multi_asset, AssetOut, AssetExecutionContext, Config
import pandas as pd
from sklearn.model_selection import train_test_split



@multi_asset(
    group_name="data_preparation",
    ins={"preprocessed_data": AssetIn(key=AssetKey("movies_users"),
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
    # Assuming 'rating' is your target variable
    X = preprocessed_training_data.drop(columns=['rating'])
    y = preprocessed_training_data['rating']
    
    split_param = {
        'test_size': 0.4,
        'random_state': 42
    }

    
    X_train, X_test, y_train, y_test = train_test_split(X, y, **split_param)

    print(X_train.columns)

    return X_train, X_test, y_train, y_test


class MyModelConfig(Config):
    batch_size : int = 128
    epochs : int = 10
    learning_rate: float = 1e-3
    embeddings_dim: int = 5
    

@asset(
    required_resource_keys={"mlflow"},

    group_name="model_training",
    ins={
        "X_train": AssetIn(),
        "y_train": AssetIn(),
        "user2Idx": AssetIn(),
        "movie2Idx": AssetIn(),
    }
)
def model_trained(context, config:MyModelConfig, X_train, y_train, user2Idx, movie2Idx):
    from .model_helper import get_model
    from keras.optimizers import Adam
    

    mlflow = context.resources.mlflow
    mlflow.log_params(context.op_config)
    mlflow.tensorflow.autolog()
    
    batch_size = config.batch_size
    epochs = config.epochs
    learning_rate = config.learning_rate
    embeddings_dim = config.embeddings_dim

    model = get_model(len(movie2Idx), len(user2Idx), embeddings_dim)

    model.compile(Adam(learning_rate=learning_rate), 'mean_squared_error')
    
    context.log.info(f'batch_size: {batch_size} - epochs: {epochs}')
    
    history = model.fit(
        [
            X_train.user_id,
            X_train.movie_id
        ], 
        y_train, 
        batch_size=batch_size,
        # validation_data=([ratings_val.userId, ratings_val.movieId], ratings_val.rating), 
        epochs=epochs, 
        verbose=1
    )
    for i, l in enumerate(history.history['loss']):
        mlflow.log_metric('mse', l, i)
    from matplotlib import pyplot as plt
    fig, axs = plt.subplots(1)
    axs.plot(history.history['loss'], label='mse')
    plt.legend()
    mlflow.log_figure(fig, 'plots/loss.png')
    return model

@asset(
    required_resource_keys={"mlflow"},

    group_name="model_training",
    ins={
        "model_trained": AssetIn(),
    }
)
def model_stored(context, model_trained):
    import numpy as np
    mlflow = context.resources.mlflow
    
    logged_model = mlflow.tensorflow.log_model(
        model_trained,
        "keras_dot_product_model",
        registered_model_name='keras_dot_product_model',
        # input_example=[np.array([1, 2]), np.array([2, 3])],
    )
    # logged_model.flavors
    model_data = {
        'model_uri': logged_model.model_uri,
        'run_id': logged_model.run_id
    }
    return model_data

@asset(
    required_resource_keys={"mlflow"},

    group_name="model_evaluation",
    ins={
        "model_stored": AssetIn(),
        "X_test": AssetIn(),
        "y_test": AssetIn(),
    }
)
def model_metrics(context, model_stored, X_test, y_test):
    mlflow = context.resources.mlflow
    logged_model = model_stored['model_uri']

    loaded_model = mlflow.pyfunc.load_model(logged_model)
    
    y_pred = loaded_model.predict([
            X_test.encoded_user_id,
            X_test.encoded_movie_id
    ])
    from sklearn.metrics import mean_squared_error

    mse = mean_squared_error(y_pred.reshape(-1), y_test.rating.values)
    metrics = {
        'test_mse': mse,
        'test_rmse': mse**(0.5)
    }
    mlflow.log_metrics(metrics)
    return metrics  
