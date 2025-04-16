from dagster import multi_asset, AssetIn, AssetKey
import pandas as pd
@multi_asset(
    group_name = "data_preparation",
    ins={
        "movies": AssetIn(
        key=AssetKey(["movies"])
        )
    }    
)
def preprocess_data(context, movies: pd.DataFrame):
    """
    Preprocesses the data for training the model.
    """
    return 0
