from pathlib import Path
import os
import yaml
from dagster import Definitions, load_assets_from_modules, define_asset_job, AssetSelection, ScheduleDefinition, file_relative_path
from dataeng_final.assets.airbyte import airbyte_connections
from dataeng_final import assets  # noqa: TID252
from dagster_mlflow import mlflow_tracking
from dataeng_final.assets import dbt, train_model   
from dataeng_final.resources import dbt_resource, postgres_io_manager



# Load the cofigs.yml file (config parameters file)
config_file_path = file_relative_path(__file__, "configs.yml")
with open(config_file_path, "r") as file:
    config_parameters = yaml.safe_load(file)

#--------------------------------Assets Definitions--------------------------------    

dbt_assets = load_assets_from_modules([dbt], group_name="raw_data_transformation")

train_assets = load_assets_from_modules([train_model])

#--------------------------------Jobs Definitions--------------------------------    
airbyte_sync_job = define_asset_job(name="airbyte_sync_job",  selection=AssetSelection.groups("raw_data_ingestion"))

dbt_sync_job = define_asset_job("dbt_sync_job" , selection=AssetSelection.groups("raw_data_transformation"))

data_prep_job = define_asset_job("data_prep_job", selection=AssetSelection.groups("data_preparation"))

model_training_job = define_asset_job("model_training_job", selection=AssetSelection.groups("model_training"))

model_evaluation_job = define_asset_job("model_evaluation_job", selection=AssetSelection.groups("model_evaluation"))

sync_all_jobs = define_asset_job(name="sync_all_jobs", selection=AssetSelection.all())


#--------------------------------Schedules Definitions--------------------------------    

daily_sync_schedule = ScheduleDefinition(
    job=sync_all_jobs,
    cron_schedule="0 0 * * *", # podria ser también @daily
    execution_timezone="America/Argentina/Buenos_Aires"
)

#--------------------------------Definitions--------------------------------    
defs = Definitions(
    assets=[airbyte_connections, *dbt_assets, *train_assets],
    jobs=[airbyte_sync_job, dbt_sync_job, data_prep_job, model_training_job, model_evaluation_job, sync_all_jobs],
    resources={
        "dbt": dbt_resource, 
        "postgres_io_manager": postgres_io_manager.configured({
            "connection_string": "env:POSTGRES_CONNECTION_STRING",
            "schema": "target"}),
        "mlflow": mlflow_tracking.configured(config_parameters['mlflow']),

    },
    schedules=[daily_sync_schedule]
)
