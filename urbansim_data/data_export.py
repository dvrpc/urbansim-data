from pathlib import Path
from .db import _db, GDRIVE_FOLDER
from pg_data_etl import Database


def export_shp(
    tablename: str,
    output_path: Path = GDRIVE_FOLDER,
    db: Database = _db,
    include_geoids: bool = True,
) -> None:
    """
    Export a spatial table from SQL to a shapefile.

    If include_geoids = True, it will include geographic identifiers
    by joining the projects to blocks, and then to a lookup table.
    """

    output_folder = output_path / "Outputs"

    export_args = {
        "filetype": "shp",
    }

    if include_geoids:
        export_args[
            "table_or_sql"
        ] = f"""
            with points_and_blockids as (
                select
                    p.*,
                    b.geoid as block_geoid
                from
                    {tablename} p
                left join
                    blocks b
                on
                    st_within(p.geom, b.geom)
            )
            select
                p.*,
                b.*
            from
                points_and_blockids p
            left join
                blocktogeos_lookup b
            on
                b.block10::text = p.block_geoid
        """
        export_args["filepath"] = output_folder / f"{tablename}_with_geoids.shp"

    else:
        export_args["table_or_sql"] = tablename
        export_args["filepath"] = output_folder / f"{tablename}.shp"

    print("-" * 80)
    print(f"Exporting {tablename} to {export_args['filepath']}")

    db.export_gis(**export_args)
