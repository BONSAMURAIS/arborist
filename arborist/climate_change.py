"""Generate the URIs needed for modelling the effects of climate change.
This code creates both `activityTypes` and `flowObjects`.

As these are not present in any online data, we have hard coded our own URIs"""
from . import data_dir
from rdflib import Literal, RDF, URIRef, Namespace, Graph
from rdflib.namespace import DC, RDFS, OWL, FOAF, XSD
from .graph_common import NS, add_common_elements
from .filesystem import create_dir
from pathlib import Path


def generate_climate_change_uris(output_base_dir):
    output_base_dir = Path(output_base_dir)
    output_dir = create_dir(output_base_dir / "activitytype" / "lcia" / "climate_change")

    g = add_common_elements(
        graph=Graph(),
        base_uri="http://rdf.bonsai.uno/activitytype/lcia/climate_change/",
        title="Climate change activity types",
        description='ActivityType instances needed for BONSAI climate change modelling',
        author="Tiago Morais",
        version="0.3",
    )

    g.bind('brdfat', 'http://rdf.bonsai.uno/activitytype/lcia/climate_change/')

    DATA = [
        ("Atmospheric energy balance",
         "http://rdf.bonsai.uno/activitytype/lcia/climate_change/atmospheric_energy_balance"),
        ("Temperature increase",
         "http://rdf.bonsai.uno/activitytype/lcia/climate_change/temperature_increse"),
    ]

    for label, uri in DATA:
        node = URIRef(uri)
        g.add( (node, RDF.type, NS.nb.ActivityType) )
        g.add( (node, RDFS.label, Literal(label)) )

    with open(output_dir / "climate_change.ttl", "wb") as f:
        g.serialize(f, format="turtle", encoding='utf-8')

    output_dir = create_dir(output_base_dir / "flowobject" / "lcia" / "climate_change")

    g = add_common_elements(
        graph=Graph(),
        base_uri="http://rdf.bonsai.uno/flowobject/lcia/climate_change/",
        title="Climate change activity types",
        description='FlowObject instances needed for BONSAI climate change modelling',
        author="Tiago Morais",
        version="0.3",
    )

    g.bind('brdffo', 'http://rdf.bonsai.uno/flowobject/lcia/climate_change/')

    DATA = [
        ("Radiative forcing",
         "http://rdf.bonsai.uno/flowobject/lcia/climate_change/radiative_forcing"),
        ("Temperature increase - 100 year horizon",
         "http://rdf.bonsai.uno/flowobject/lcia/climate_change/temperature_increase_100yr_horizon"),
    ]

    for label, uri in DATA:
        node = URIRef(uri)
        g.add( (node, RDF.type, NS.nb.FlowObject) )
        g.add( (node, RDFS.label, Literal(label)) )

    with open(output_dir / "climate_change.ttl", "wb") as f:
        g.serialize(f, format="turtle", encoding='utf-8')
