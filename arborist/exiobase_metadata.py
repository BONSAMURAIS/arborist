from . import data_dir
from .filesystem import write_graph
from .graph_common import add_common_elements, generate_generic_graph
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef
from rdflib.namespace import RDFS, OWL
import pandas


def generate_exiobase_metadata_uris(output_base_dir):
    output_base_dir = Path(output_base_dir)

    df = pandas.read_excel(
        data_dir / "exiobase_classifications_v_3_3_17.xlsx",
        sheet_name="Activities",
        header=0
    )

    generate_generic_graph(
        output_base_dir,
        kind='ActivityType',
        data=sorted(set(zip(df['Activity name'], df['Activity code 2']))),
        directory_structure=["exiobase3_3_17"],
        title="EXIOBASE 3.3.17 activity types",
        description='ActivityType instances needed for BONSAI modelling of EXIOBASE version 3.3.17',
        author="BONSAI team",
        version="0.3",
    )

    # # TODO: Need to add preferred unit
    df = pandas.read_excel(
        data_dir / "exiobase_classifications_v_3_3_17.xlsx",
        sheet_name="Products_HSUTs",
        header=0
    )

    generate_generic_graph(
        output_base_dir,
        kind='FlowObject',
        data=sorted(set(zip(df['Product name'], df['product code 2']))),
        directory_structure=["exiobase3_3_17"],
        title="EXIOBASE 3.3.17 flow objects",
        description='FlowObject instances needed for BONSAI modelling of EXIOBASE version 3.3.17',
        author="BONSAI team",
        version="0.3",
    )

    # Exiobase locations are hardcoded to geoname URIs, so just use CSV
    # created by hand
    df = pandas.read_csv(
        data_dir / "exiobase_location_uris.csv",
        header=0
    )

    g = add_common_elements(
        Graph(),
        "http://rdf.bonsai.uno/location/exiobase3_3_17/",
        "Custom locations for EXIOBASE 3.3",
        "Country groupings used EXIOBASE 3.3.17",
        "Chris Mutel",
        "0.3",
    )
    g.bind('gn', 'http://sws.geonames.org/')
    g.bind('brdflo', "http://rdf.bonsai.uno/location/exiobase3_3_17/")
    g.bind("schema", "http://schema.org/")

    for dct in df.replace({float('nan'): None}).to_dict(orient='records'):
        if dct['geonames_code']:
            node = URIRef("http://" + dct['URI'])
        else:
            node = URIRef("http://rdf.bonsai.uno/location/exiobase3_3_17/#" + dct['name'])
        g.add((node, RDF.type, URIRef("http://schema.org/Place")))
        g.add((node, RDFS.label, Literal(dct['label'] or dct['name'])))

    write_graph(output_base_dir / "location" / "exiobase3_3_17", g)
