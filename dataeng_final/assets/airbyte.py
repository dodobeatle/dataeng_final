from dagster_airbyte import load_assets_from_airbyte_instance
from dataeng_final.resources import airbyte_resource

#airbyte_assets = load_assets_from_airbyte_instance(airbyte_resource)

airbyte_connections = load_assets_from_airbyte_instance(airbyte_resource, 
                                                        key_prefix="mlops_raw", 
                                                        connection_to_group_fn=lambda connection_name: "raw_data_ingestion")