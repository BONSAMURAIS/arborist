__all__ = (
    "generate_climate_change_uris",
    "generate_electricity_grid_uris",
    "generate_exiobase_us_epa_uris",
    "generate_foaf_uris",
    "generate_time_uris",
    "generate_unit_uris",
    "generate_us_epa_uris",
    "get_metadata",
)
__version__ = (0, 1)

from pathlib import Path
data_dir = Path(__file__).parent / "data"

from .climate_change import generate_climate_change_uris
from .electricity_grid import generate_electricity_grid_uris
from .exiobase_us_epa import generate_exiobase_us_epa_uris
from .extract_metadata import get_metadata
from .foaf import generate_foaf_uris
from .time_uris import generate_time_uris
from .units import generate_unit_uris
from .us_epa import generate_us_epa_uris
