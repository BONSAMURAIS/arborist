from .filesystem import write_graph
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, SKOS, DC, OWL, XSD, RDFS
import datetime
from . import __version__
from pathlib import Path


def generate_provenance_uris(output_base_dir):
    exiobase_version = "3.3.17"
    exiobase_update_date = "2019-03-12"

    bprov_uri = "http://rdf.bonsai.uno/prov"
    prov = Namespace("http://www.w3.org/ns/prov#")
    purl = Namespace("http://purl.org/dc/dcmitype/")
    bfoaf = Namespace("http://rdf.bonsai.uno/foaf#")
    bprov = Namespace("{}#".format(bprov_uri))
    dtype = Namespace("http://purl.org/dc/dcmitype/")
    vann = Namespace("http://purl.org/vocab/vann/")

    g = Graph()
    g.bind("org", "https://www.w3.org/TR/vocab-org/")
    g.bind("dtype", dtype)
    g.bind("skos", SKOS)
    g.bind("foaf", FOAF)
    g.bind("dc", DC)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("prov", prov)
    g.bind("bfoaf", bfoaf)
    g.bind("bprov", bprov)
    g.bind("vann", vann)

    # Meta information about the Named Graph
    node = URIRef(bprov_uri)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    g.add((node, RDF.type, dtype.Dataset))
    g.add((node, DC.contributor, Literal("BONSAI team")))
    g.add((node, DC.description, Literal("Provenance information about datasets and data extraction activities")))
    g.add((node, vann.preferredNamespaceUri, URIRef(bprov)))
    g.add((node, DC.creator, bfoaf.bonsai))
    g.add((node, DC.license, URIRef("https://creativecommons.org/licenses/by/3.0/")))
    g.add((node, DC.modified, Literal(today, datatype=XSD.date)))
    g.add((node, DC.publisher, Literal("bonsai.uno")))
    g.add((node, DC.title, Literal("Provenance information")))
    g.add((node, OWL.versionInfo, Literal(__version__)))

    # exiobase dataset
    ebd = bprov["exiobaseDataset_{}".format(exiobase_version)]
    g.add((ebd, RDF.type, purl.Dataset))
    g.add((ebd, RDF.type, prov.Entity))
    g.add(
        (
            ebd,
            RDFS.label,
            Literal(
                "A LCSA dataset created by the EXIOBASE-Consortium, version {}".format(exiobase_version)
            ),
        )
    )
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    g.add((ebd, OWL.versionInfo, Literal("3.3.17")))
    g.add((ebd, DC.term("license"), URIRef("https://www.exiobase.eu/index.php/terms-of-use")))
    g.add((ebd, DC.term("date"), Literal(exiobase_update_date, datatype=XSD.date)))
    g.add((ebd, prov.wasAttributedTo, URIRef(bfoaf.exiobase_consortium)))
    g.add((ebd, DC.term("rights"), Literal("Copyright © 2015 - EXIOBASE Consortium")))
    g.add((ebd, prov.hadPrimarySource, URIRef("https://www.exiobase.eu/index.php/data-download/exiobase3hyb")))

    # dataExtractionActivity
    arborist_uri = bprov["dataExtractionActivity_{}".format(__version__.replace(".", "_"))]
    g.add((arborist_uri, RDF.type, prov.Activity))
    g.add(
        (
            arborist_uri,
            RDFS.label,
            Literal(
                "Activity to create instances of flowObjects, activityTypes and Locations"
            ),
        )
    )
    g.add((arborist_uri, prov.used, URIRef("http://ontology.bonsai.uno/core")))
    g.add((arborist_uri, prov.used, bprov["exiobaseDataset_{}".format(exiobase_version)]))
    g.add((arborist_uri, prov.hadPlan, URIRef(bprov.extractionScript)))
    g.add((arborist_uri, prov.wasAssociatedWith, URIRef(bfoaf.bonsai)))
    g.add((arborist_uri, OWL.versionInfo, Literal(__version__)))

    plan = URIRef(bprov.extractionScript)
    g.add((plan, RDF.type, prov.Plan))
    g.add((plan, RDF.type, prov.Entity))
    g.add((plan, RDFS.label, Literal("Entity representing the latest version of the Arborist Script")))
    g.add((plan, prov.hadPrimarySource, URIRef("https://github.com/BONSAMURAIS/arborist/tree/v{}".format(__version__.replace(".", "_")))))

    write_graph(Path(output_base_dir) / "prov", g)