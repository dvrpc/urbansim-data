from pathlib import Path
from pg_data_etl import Database
from urbansim_data import GDRIVE_FOLDER, _db


def clean_name_for_sql(filepath: Path) -> str:
    """
    Turn the filename into a SQL-compliant table name.

    Transform: '/my/path/to/Badly Formatted-table name.csv'
    Into: 'badly_formatted_table_name'
    """

    sql_tablename = filepath.stem.lower()

    for character in [" ", "-"]:
        sql_tablename = sql_tablename.replace(character, "_")

    return sql_tablename


def import_data(db: Database = _db, folder: Path = GDRIVE_FOLDER) -> None:
    """
    Import all shapefiles and CSV files within the '/Input/' subfolder,
    if they have not yet been uploaded.
    """

    # Ensure that the database exists
    db.create_db()

    print("-" * 80)
    print("Importing shapefiles:")

    for shp in folder.rglob("Inputs/*.shp"):
        sql_tablename = clean_name_for_sql(shp)

        if f"public.{sql_tablename}" not in db.spatial_table_list():
            print("\t ->", sql_tablename)
            db.shp2pgsql(shp, 26918, sql_tablename)

    print("Importing CSV files:")

    for csvfile in folder.rglob("Inputs/*.csv"):
        sql_tablename = clean_name_for_sql(csvfile)

        if f"public.{sql_tablename}" not in db.table_list():
            print("\t ->", sql_tablename)
            db.import_tabular_file(csvfile, sql_tablename)


if __name__ == "__main__":
    import_data()
