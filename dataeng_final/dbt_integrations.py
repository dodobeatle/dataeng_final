from pathlib import Path
from dagster import EnvVar
from dagster_dbt import DbtCliResource, DbtProject

dbt_project = DbtProject(
    #project_dir="/home/pedro/workspace/utnfrt/dataeng_final/dbt_project",
    project_dir=Path(__file__).joinpath("..","..","dbt_project").resolve(),
    #profiles_dir="/home/pedro/.dbt/"    
    #profiles_dir=Path.home().joinpath(".dbt"),
    #target="dev",
    #profile="dbt_project"
)

dbt_project.prepare_if_dev()