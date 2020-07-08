# Arborist

Arborist creates turtle files of the istances of data based on an ontology. The turtle files are needed for the BONSAI knowledge graph. 

The turtle files generated are stored in the BONSAI [rdf repository](https://github.com/BONSAMURAIS/rdf).

Currently generates the following:

* Activity types, flow objects, and custom locations for EXIOBASE 3.3.17.
* Custom activity types and flow objects for electricity modelling
* URIs for the complete years 2010-2019.

## Installation

### with package managers [pip or conda]

Installable via `pip` or `conda` (channel `cmutel`). See [requirements](https://github.com/BONSAMURAIS/arborist/blob/master/requirements.txt), though these should be installed automatically.

### manual

Call `python setup.py install` inside the repository:

```
git clone git@github.com:BONSAMURAIS/arborist.git
cd arborist
python setup.py install
```

## Usage

### As a command line tool

If the package is correctly installed, you can use the command line tool `arborist-cli` to produce the rdfs as follows:

```
mkdir output
arborist-cli regenerate output
```

This will put inside the `output` directory the following contents:

```
output
├── activitytype
│   ├── core
│   │   └── electricity_grid
│   │       └── electricity_grid.ttl
│   ├── entsoe
│   │   └── entsoe.ttl
│   ├── exiobase3_3_17
│   │   └── exiobase3_3_17.ttl
│   └── lcia
│       └── climate_change
│           └── climate_change.ttl
├── flowobject
│   ├── core
│   │   └── electricity_grid
│   │       └── electricity_grid.ttl
│   ├── exiobase3_3_17
│   │   └── exiobase3_3_17.ttl
│   ├── lcia
│   │   └── climate_change
│   │       └── climate_change.ttl
│   └── us_epa_elem
│       └── us_epa_elem.ttl
├── foaf
│   └── foaf.ttl
├── location
│   └── exiobase3_3_17
│       └── exiobase3_3_17.ttl
├── time
│   └── time.ttl
|── unit
|   └── unit.ttl
└── prov
    └── prov.ttl
```

#### Emission flows
The library can also be used to extract emission flows from the exiobase extension table.
To do this, first download `MR_HSUT_2011_v3_3_17_extensions.xlsb` into a input/ folder, then set `"extract_exiobase_emissions": true` in `config.json`.
The exiobase extensions table can be downloaded from this url: [www.exiobase.eu](https://www.exiobase.eu/).

Using the cli tool to extract emissions can be done from the terminal with the `-i input/dir` argument, such as:
`arborist-cli regenerate output -i input/`.

#### Configuration
The package provides a `Config.json` file which enables the user to choose what graphs to extract. 
The value `True` enables the extraction of the specified graph, whereas the value `False` disables the creation of the specified graph.

### As a library

### Generation of URIs

This library has a number of generation functions; you can call them all with:

    from arborist import generate_all
    generate_all("filepath/to/rdf/repository/base/")

`arborist` will write out the [turtle](https://en.wikipedia.org/wiki/Turtle_(syntax)) files in the correct directory structure to commit changes to the [rdf repository](https://rdf.bonsai.uno/).

The RDF output directory has the following structure:

    activitytype
        core
        entsoe
        exiobase3_3_17
        lcia
    flowobject
        core
        exiobase3_3_17
        lcia
        us_epa_elem
    location
        exiobase3_3_17
    prov
    time
    unit
    foaf

The convention now is that each subdirectory has a `.ttl` file *and* and `.jsonld` file with the **same name** as the directory.

### Retrieval of URIs

## Contributing

All contributions should be via pull request, do not edit this package directly! We actually use it for stuff.
