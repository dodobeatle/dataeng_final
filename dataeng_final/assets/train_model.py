from dagster import asset, AssetIn, AssetKey, Output
import pandas as pd



@asset(
        ins={"preprocessed_data": AssetIn(key=AssetKey("movies"),
             input_manager_key= "postgres_io_manager")}
)
def preprocessed_data(context, preprocessed_data: pd.DataFrame)->Output[pd.DataFrame]:
    """
    Preprocesses the data for training the model.
    """
    rows_count = len(preprocessed_data)

    return Output(
        preprocessed_data,
        metadata={
            "rows_count": rows_count
        }
    )
