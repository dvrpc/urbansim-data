from pathlib import Path
from .db import _db, GDRIVE_FOLDER
from pg_data_etl import Database


def export_shp(tablename: str, output_path: Path = GDRIVE_FOLDER, db: Database = _db):
    """
    Export a spatial table from SQL to a shapefile
    """

    shp_output_path = output_path / "Outputs" / tablename

    print("-" * 80)
    print(f"Exporting {tablename} to {shp_output_path}")

    db.ogr2ogr_export(tablename, shp_output_path)