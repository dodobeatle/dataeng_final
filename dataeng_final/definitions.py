from dagster import Definitions, load_assets_from_modules, define_asset_job, AssetSelection
from dataeng_final.assets.airbyte import airbyte_connections
from dataeng_final import assets  # noqa: TID252


all_assets = load_assets_from_modules([assets])

#--------------------------------Jobs Definitions--------------------------------    
airbyte_sync_job = define_asset_job(name="airbyte_sync_job",  selection=AssetSelection.groups("raw_data_ingestion"))

sync_all_jobs = define_asset_job(name="sync_all_jobs", selection="*")
#--------------------------------Definitions--------------------------------    
defs = Definitions(
    assets=[airbyte_connections, *all_assets],
    jobs=[airbyte_sync_job, sync_all_jobs]
)
