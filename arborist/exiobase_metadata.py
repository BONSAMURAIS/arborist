from . import data_dir
from .filesystem import write_graph
from .graph_common import add_common_elements, generate_generic_graph
from .provenance_uris import generate_provenance_uris
from .graph_common import NS
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, XSD, OWL
from rdflib.namespace import RDFS
import pandas
import pkg_resources
import os


def generate_exiobase_metadata_uris(output_base_dir):
    output_base_dir = Path(output_base_dir)

    file_path = os.path.join(data_dir, "exiobase_classifications_v_3_3_17.xlsx")
    file_handler = pkg_resources.resource_stream(__name__, file_path)
    df = pandas.read_excel(
        file_handler,
        sheet_name="Activities",
        header=0,
    )

    generate_generic_graph(
        output_base_dir,
        kind="ActivityType",
        data=sorted(set(zip(df["Activity name"], df["Activity code 2"]))),
        directory_structure=["exiobase3_3_17"],
        title="EXIOBASE 3.3.17 activity types",
        description="ActivityType instances needed for BONSAI modelling of EXIOBASE version 3.3.17",
        author="BONSAI team"
    )

    # # TODO: Need to add preferred unit
    df = pandas.read_excel(
        file_handler,
        sheet_name="Products_HSUTs",
        header=0,
    )

    generate_generic_graph(
        output_base_dir,
        kind="FlowObject",
        data=sorted(set(zip(df["Product name"], df["product code 2"]))),
        directory_structure=["exiobase3_3_17"],
        title="EXIOBASE 3.3.17 flow objects",
        description="FlowObject instances needed for BONSAI modelling of EXIOBASE version 3.3.17",
        author="BONSAI team"
    )

    # Exiobase locations are hardcoded to geoname URIs, so just use CSV
    # created by hand
    file_path = os.path.join(data_dir, "exiobase_location_uris.csv")
    file_handler = pkg_resources.resource_stream(__name__, file_path)
    df = pandas.read_csv(file_handler, header=0)

    g = add_common_elements(
        Graph(),
        "http://rdf.bonsai.uno/location/exiobase3_3_17#",
        "Custom locations for EXIOBASE 3.3",
        "Country groupings used EXIOBASE 3.3.17",
        "Chris Mutel"
    )
    g.bind("gn", "http://sws.geonames.org/")
    g.bind("brdflo", "http://rdf.bonsai.uno/location/exiobase3_3_17#")
    g.bind("schema", "http://schema.org/")

    for dct in df.replace({float("nan"): None}).to_dict(orient="records"):

        geoname = URIRef("http://{}".format(dct["URI"]))
        node = URIRef("http://rdf.bonsai.uno/location/exiobase3_3_17#{}".format(dct["name"]))

        g.add((node, RDF.type, URIRef("http://schema.org/Place")))
        g.add((node, RDFS.label, Literal(dct["label"] or dct["name"])))
        if node != geoname:
            g.add((node, OWL.sameAs, URIRef(geoname)))
        g.add((URIRef("http://rdf.bonsai.uno/location/exiobase3_3_17#"), NS.prov.hadMember, node))

    write_graph(output_base_dir / "location" / "exiobase3_3_17", g)
