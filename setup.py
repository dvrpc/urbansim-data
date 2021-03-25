from setuptools import find_packages, setup

setup(
    name="urbansim_data",
    packages=find_packages(),
    version="0.0.1",
    description="Python module to manipulate development data in UrbanSim into GIS data products",
    author="Aaron Fraint, AICP",
    license="GNU General Public License v3.0",
    entry_points="""
        [console_scripts]
        urbansim=urbansim_data.cli:main
    """,
)
