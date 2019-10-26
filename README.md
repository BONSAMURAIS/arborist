# Arborist

Arborist creates turtle files of the istances of data based on an ontology. The turtle files are needed for the BONSAI knowledge graph. 

The turtle files generated are stored in the BONSAI [rdf repository](https://github.com/BONSAMURAIS/rdf).

Currently generates the following:

* Activity types, flow objects, and custom locations for EXIOBASE 3.3.17.
* Custom activity types and flow objects for electricity modelling
* URIs for the complete years 2010-2019.

## Installation

Installable via `pip` or `conda` (channel `cmutel`). See [requirements](https://github.com/BONSAMURAIS/arborist/blob/master/requirements.txt), though these should be installed automatically.

## Usage

### Generation of URIs

This library has a number of generation functions; you can call them all with:

    from arborist import generate_all
    generate_all("filepath/to/rdf/repository/base/")

`arborist` will write out the [turtle](https://en.wikipedia.org/wiki/Turtle_(syntax)) files in the correct directory structure to commit changes to the [rdf repository](https://rdf.bonsai.uno/).

The RDF output directory has the following structure:

    activitytype
        lcia
    flowobject
        lcia
        us_epa
        exiobase3_3_17
    unit
    location
    foaf

The convention now is that each subdirectory has a `.ttl` file *and* and `.jsonld` file with the **same name** as the directory.

### Retrieval of URIs

## Contributing

All contributions should be via pull request, do not edit this package directly! We actually use it for stuff.
