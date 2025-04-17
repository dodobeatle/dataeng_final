from dagster import AssetExecutionContext
from dagster_dbt import dbt_assets, DbtCliResource
from ..dbt_integrations import dbt_project

@dbt_assets(
    manifest=dbt_project.manifest_path,
    select="dbt_project.movies dbt_project.critic_reviews dbt_project.user_reviews"
)
def dbt_analytics(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["run"], context=context).stream()

    