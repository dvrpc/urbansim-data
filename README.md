# urbansim-data

Python module to manipulate development data in UrbanSim into GIS data products

## Requirements

Local requirements include `conda` and `PostgreSQL`/`PostGIS` (+ associated command-line tools `psql`, `shp2pgsql`, and `ogr2ogr` on your system path)

## Configuration

At the root of this codebase, create a `.env` file that defines the following values:

```text
DB_NAME = name_of_your_postgres_database
DB_HOST = localhost
DB_PORT = 5432
DB_USER = postgres
DB_PW = fake_password_placeholder

GOOGLE_DRIVE_ROOT = /Volumes/GoogleDrive/Shared drives/Long Range Plan/Models/etc
```

Replace the placeholder values with your database name, password, and Google Drive folder.

## CLI

You can use this tool through its command-line-interface: `urbansim`

For example:

```bash
> urbansim --help

Usage: urbansim [OPTIONS] COMMAND [ARGS]...

  'urbansim' provides command-line access to functions that import,
  manipulate, and export development data in helpful formats.

Options:
  --help  Show this message and exit.

Commands:
  assign-geom-to-projects  Transform development table into spatial data,...
  export-shp               Export a spatial table from SQL to shapefile
  import-data              Import CSV and Shapefiles to SQL database
```

## Usage

### (1) Load a development table and/or shapefiles:

```bash
❯ urbansim import-data
```

`import-data` does not require any arguments. It reads CSV and shapefile data from the `Inputs` subfolder of the environment variable named "`GOOGLE_DRIVE_ROOT`".

### (2) Transform non-spatial development table into points:

```bash
❯ urbansim assign-geom-to-projects
```

`assign-geom-to-projects` does not require any arguments, but provides three optional ones, as shown in the help text:

```bash
❯ urbansim assign-geom-to-projects --help

Usage: urbansim assign-geom-to-projects [OPTIONS]

  Transform development table into spatial data, using parcel centroid

Options:
  -pr, --project-table TEXT  Name of the project table. Defaults to most
                             recent download.

  -pa, --parcel-table TEXT   Name of the parcel geo-table. Defaults to
                             'parcels'

  -y, --year-filter TEXT     SQL-valid filter to limit developments to a
                             certain time range. Defaults to 'start_year >=
                             2020'

  --help                     Show this message and exit.
```

Using these options, you could do something like this:

```bash
❯ urbansim assign-geom-to-projects --project-table my_project_table --parcel-table my_parcel_table --year-filter 'start_year >= 1995'
```

### (3) Export data from PostGIS to shapefile:

```bash
❯ urbansim export-shp TABLENAME
```

The prior transformation step creates a table with a name that combines the source development table and the year filter that was applied. For example, to export a table named `projects_2021_05_27_start_year_gte_1995`:

```bash
❯ urbansim export-shp projects_2021_05_27_start_year_gte_1995
```

This will generate a shapefile named `projects_2021_05_27_start_year_gte_1995.shp` within the `Outputs` subfolder of the environment variable named "`GOOGLE_DRIVE_ROOT`".
