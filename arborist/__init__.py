import os
import json
import pkg_resources
from pathlib import Path

__all__ = (
    "generate_climate_change_uris",
    "generate_electricity_grid_uris",
    "generate_entsoe_uris",
    "generate_exiobase_metadata_uris",
    "generate_exiobase_us_epa_uris",
    "generate_foaf_uris",
    "generate_time_uris",
    "generate_unit_uris",
    "generate_us_epa_uris",
    "generate_all",
    "get_metadata",
    "generate_provenance_uris",
    "generate_emissions"
)
VERSION = (0, 5)
__version__ = ".".join(str(v) for v in VERSION)

data_dir = "data"

from .climate_change import generate_climate_change_uris
from .electricity_grid import generate_electricity_grid_uris
from .entsoe import generate_entsoe_uris
from .exiobase_metadata import generate_exiobase_metadata_uris
from .exiobase_us_epa import generate_exiobase_us_epa_uris
from .extract_metadata import get_metadata
from .foaf import generate_foaf_uris
from .time_uris import generate_time_uris
from .unit_uris import generate_unit_uris
from .us_epa_elem_flow_list import generate_us_epa_uris
from .provenance_uris import generate_provenance_uris
from .extract_emissions import generate_emissions


def generate_all(base_dir):
    config_name = "config.json"
    config_path = Path(config_name)
    if not os.path.exists(config_path):
        print("Configuration file not present")
        exit(0)

    with open(config_name) as json_file:
        options = json.load(json_file)

        if options['extract_exiobase_emissions'] is True:
            generate_emissions(base_dir)

        if options["extract_climate_change"] is True:
            generate_climate_change_uris(base_dir)

        if options["extract_electricity_grid"] is True:
            generate_electricity_grid_uris(base_dir)

        if options["extract_entsoe"] is True:
            generate_entsoe_uris(base_dir)

        if options["extract_exiobase_metadata"] is True:
            generate_exiobase_metadata_uris(base_dir)

        if options["extract_exiobase_us_epa"] is True:
            # generate_exiobase_us_epa_uris(base_dir)
            pass

        if options["extract_foaf"] is True:
            generate_foaf_uris(base_dir)

        if options["extract_time"] is True:
            generate_time_uris(base_dir)

        if options["extract_unit"] is True:
            generate_unit_uris(base_dir)

        if options["extract_us_epa"] is True:
            generate_us_epa_uris(base_dir)

        if options["extract_provenance"] is True:
            generate_provenance_uris(base_dir)
