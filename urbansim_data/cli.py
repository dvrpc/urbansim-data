import click

from urbansim_data.data_import import import_data as _import_data
from urbansim_data.data_manipulation import projects_to_parcels, _find_latest_project_table


@click.group()
def main():
    """'urbansim' provides command-line access to the Python/SQL tool"""
    pass


@click.command()
def import_data():
    """Import CSV and Shapefiles to SQL database """
    _import_data()


@click.command()
@click.option("-pr", "--project-table", default=_find_latest_project_table())
@click.option("-pa", "--parcel-table", default="parcels")
@click.option("-y", "--year-filter", default="start_year >= 2020")
def assign_geom_to_projects(project_table, parcel_table, year_filter):
    projects_to_parcels(
        project_table=project_table, parcel_table=parcel_table, year_filter=year_filter
    )


commands = [import_data, assign_geom_to_projects]

for cmd in commands:
    main.add_command(cmd)
