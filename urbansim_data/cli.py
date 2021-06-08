import click

from urbansim_data.data_import import import_data as _import_data
from urbansim_data.data_manipulation import projects_to_parcels, _find_latest_project_table
from urbansim_data.data_export import export_shp as _export_shp


@click.group()
def main():
    """'urbansim' provides command-line access to
    functions that import, manipulate, and export
    development data in helpful formats."""
    pass


@click.command()
def import_data():
    """Import CSV and Shapefiles to SQL database """
    _import_data()


@click.command()
@click.option(
    "-pr",
    "--project-table",
    default=_find_latest_project_table(),
    help="Name of the project table. Defaults to most recent download.",
)
@click.option(
    "-pa",
    "--parcel-table",
    default="parcels",
    help="Name of the parcel geo-table. Defaults to 'parcels'",
)
@click.option(
    "-y",
    "--year-filter",
    default="start_year >= 2020",
    help="SQL-valid filter to limit developments to a certain time range. Defaults to 'start_year >= 2020'",
)
def assign_geom_to_projects(project_table, parcel_table, year_filter):
    """Transform development table into spatial data, using parcel centroid"""
    projects_to_parcels(
        project_table=project_table, parcel_table=parcel_table, year_filter=year_filter
    )


@click.command()
@click.argument("tablename")
@click.option(
    "--geoid/--no-geoid",
    default=True,
    help="Flag to include geographic IDs in output. Defaults to including them, using --geoid",
)
def export_shp(tablename, geoid):
    """Export a spatial table from SQL to shapefile"""
    _export_shp(tablename, include_geoids=geoid)


commands = [import_data, assign_geom_to_projects, export_shp]

for cmd in commands:
    main.add_command(cmd)
