from urbansim_data import _db
from pg_data_etl import Database
from tqdm import tqdm
from typing import Union


def _find_latest_project_table(db: Database = _db) -> str:
    """
    You may have multiple development ('project') tables.
    This function finds the one with the most recent datestamp
    and returns the name of the table
    """

    query = """
        select table_name 
        from information_schema.tables
        where table_name like 'all_devprojects%%'
        order by table_name desc limit 1
    """

    project_table = db.query_via_psycopg2(query)

    return project_table[0][0]


def projects_to_parcels(
    project_table: str = "all_devprojects_2021_03_15",
    parcel_table: str = "parcels",
    db: Database = _db,
    year_filter: Union[str, bool] = False,
) -> None:
    """
    If you want to limit to developments starting in a certain year,
    provide a SQL-valid year_filter argument as a string.
    For example:
        year_filter = 'start_year > 2020'
    """

    # Parse the date out of the project table name
    # Turn "all_devprojects_2021_03_15" into "2021_03_15"
    project_table_date = "_".join(project_table.split("_")[-3:])
    new_project_table = f"projects_{project_table_date}"

    # Create a new version of the project table with only the projects we want to analyze
    projects_to_map_query = f"""
        select
            project_id,
            name,
            address,
            parcel_id,
            building_type,
            start_year
            residential_units,
            non_res_sqft
        from {project_table}
    """

    # Add the year filter to the SQL code and the new table name
    if year_filter:

        projects_to_map_query += f"""
            WHERE {year_filter}
        """

        year_filter_table_name = year_filter.replace(" ", "_")
        for old_char, new_char in [("<", "lt"), (">", "gt"), ("<=", "lte"), (">=", "gte")]:
            if old_char in year_filter_table_name:
                year_filter_table_name = year_filter_table_name.replace(old_char, new_char)
        new_project_table += f"_{year_filter_table_name}"

    print("-" * 80)
    print(f"Applying parcel geometries to {new_project_table}")

    create_table_query = f"""
    create table {new_project_table} as (
        {projects_to_map_query}
    )
    """
    db.execute_via_psycopg2(create_table_query)

    # Add a 'geom' column to hold POINT data
    db.execute_via_psycopg2(
        f"select addgeometrycolumn('{new_project_table}', 'geom', 26918, 'POINT', 2)"
    )

    # Loop over every project and assign an appropriate point location to the 'geom' column
    parcel_ids = db.query_via_psycopg2(f"SELECT parcel_id FROM {new_project_table}")
    pids = [pid[0] for pid in parcel_ids]

    for pid in tqdm(pids, total=len(pids)):

        if ";" not in pid:
            query = f"""
                update {new_project_table} set geom = (
                    select st_centroid(geom) from {parcel_table} where primary_id = {pid}
                )
                where parcel_id = '{pid}'
            """
        else:
            query = f"""
                update {new_project_table} set geom = (
                    select st_centroid(st_union(geom)) from {parcel_table}
                    where primary_id in (select unnest(string_to_array('{pid}', ';'))::int)
                )
                where parcel_id = '{pid}'
            """
        db.execute_via_psycopg2(query)


if __name__ == "__main__":
    projects_to_parcels(year_filter="start_year >= 2020")
