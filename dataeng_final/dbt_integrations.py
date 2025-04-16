from dagster import EnvVar
from dagster_dbt import DbtCliResource, DbtProject


dbt_project = DbtProject(
    #profile="dbt_project",
    project_dir="/home/pedro/workspace/utnfrt/dataeng_final/dbt_project",
    profiles_dir="/home/pedro/.dbt/profiles.yml"    
    #profiles_dir=EnvVar.get_value("DBT_PROFILES_DIR"),
    #project_dir=EnvVar.get_value("DBT_PROJECT_DIR")
)

