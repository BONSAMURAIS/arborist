"""Generate the URIs needed for core activity type `electricity grid`.
Handcrafted as not available elsewhere."""

from . import data_dir
from .filesystem import create_dir
from .graph_common import NS, add_common_elements
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import RDFS
import pandas


def generate_electricity_grid_uris(output_base_dir):
    output_base_dir = Path(output_base_dir)

    g = add_common_elements(
        graph=Graph(),
        base_uri="http://rdf.bonsai.uno/activitytype/core/electricity_grid/",
        title="Electricity grid activity types for BONSAI",
        description='ActivityType instances needed for BONSAI electricity grid modelling',
        author="Arthur Jakobs",
        version="0.2",
    )

    g.bind('brdfat', 'http://rdf.bonsai.uno/activitytype/core/electricity_grid/')

    node = URIRef("http://rdf.bonsai.uno/activitytype/core/eg")
    g.add( (node, RDF.type, NS.nb.ActivityType) )
    g.add( (node, RDFS.label, Literal("Electricity grid")) )

    node = URIRef("http://rdf.bonsai.uno/activitytype/core/em")
    g.add( (node, RDF.type, NS.nb.ActivityType) )
    g.add( (node, RDFS.label, Literal("Market for electricity")) )

    create_dir(output_base_dir / "activitytype" / "core" / "electricity_grid")
    with open(
            output_base_dir / "activitytype" / "core" / "electricity_grid" / "electricity_grid.ttl",
            "wb") as f:
        g.serialize(f, format="turtle", encoding='utf-8')

    g = add_common_elements(
        graph=Graph(),
        base_uri="http://rdf.bonsai.uno/flowobject/core/electricity_grid/",
        title="Electricity grid flow objects for BONSAI",
        description='FlowObject instances needed for BONSAI electricity grid modelling',
        author="Arthur Jakobs",
        version="0.2",
    )

    g.bind('brdfat', 'http://rdf.bonsai.uno/activitytype/core/electricity_grid/')

    node = URIRef("http://rdf.bonsai.uno/flowobject/core/elec")
    g.add( (node, RDF.type, NS.nb.FlowObject) )
    g.add( (node, RDFS.label, Literal("Electricity from the grid")) )

    create_dir(output_base_dir / "flowobject" / "core" / "electricity_grid")
    with open(
            output_base_dir / "flowobject" / "core" / "electricity_grid" / "electricity_grid.ttl",
            "wb") as f:
        g.serialize(f, format="turtle", encoding='utf-8')

