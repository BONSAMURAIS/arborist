from .filesystem import write_graph
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, SKOS, DC, OWL, XSD, RDFS
import datetime


def generate_provenance_uris(output_base_dir, exiobase_version, arborist_version, arborist_url):

    exiobase_version = exiobase_version.replace(".", "_")
    arborist_version = arborist_version.replace(".", "_")
    prov = Namespace("http://www.w3.org/ns/prov#")
    purl = Namespace("http://purl.org/dc/dcmitype/")
    bfoaf = Namespace("https://rdf.bonsai.uno/foaf/")
    bprov = Namespace("http://rdf.bonsai.uno/prov/")
    dtype = Namespace("http://purl.org/dc/dcmitype/")
    vann = Namespace("http://purl.org/vocab/vann/")

    g = Graph()
    g.bind("org", "https://www.w3.org/TR/vocab-org/")
    g.bind("dtype", "http://purl.org/dc/dcmitype/")
    g.bind("skos", SKOS)
    g.bind("foaf", FOAF)
    g.bind("dc", DC)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("prov", "http://www.w3.org/ns/prov#")
    g.bind("bfoaf", "https://rdf.bonsai.uno/foaf/")
    g.bind("bprov", "http://rdf.bonsai.uno/prov/")
    g.bind("vann", "http://purl.org/vocab/vann/")

    # Meta information about the Named Graph
    node = URIRef(bprov)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    g.add((node, RDF.type, dtype.Dataset))
    g.add((node, DC.contributor, Literal("BONSAI team")))
    g.add((node, DC.description, Literal("Provenance information about datasets and data extraction activities")))
    g.add((node, vann.preferredNamespaceUri, URIRef("http://rdf.bonsai.uno/prov/")))
    g.add((node, DC.creator, bfoaf.bonsai))
    g.add((node, DC.license, URIRef("https://creativecommons.org/licenses/by/3.0/")))
    g.add((node, DC.modified, Literal(today, datatype=XSD.date)))
    g.add((node, DC.publisher, Literal("bonsai.uno")))
    g.add((node, DC.title, Literal("Provenance information")))
    g.add((node, OWL.versionInfo, Literal("1.0")))

    # exiobase dataset
    ebd = URIRef(getattr(bprov, "exiobaseDataset_" + exiobase_version))
    g.add((ebd, RDF.type, purl.Dataset))
    g.add((ebd, RDF.type, prov.Entity))
    g.add(
        (
            ebd,
            RDFS.label,
            Literal(
                "A LCSA dataset created by the EXIOBASE-Consortium, version " + exiobase_version
            ),
        )
    )
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    g.add((ebd, OWL.versionInfo, Literal("3.3.17")))
    g.add((ebd, DC.term("license"), URIRef("https://www.exiobase.eu/index.php/terms-of-use")))
    g.add((ebd, DC.term("date"), Literal(today, datatype=XSD.date)))
    g.add((ebd, prov.wasAttributedTo, URIRef(bfoaf.exiobase_consortium)))
    g.add((ebd, DC.term("rights"), Literal("Copyright © 2015 - EXIOBASE Consortium")))

    # dataExtractionActivity
    crdfma = URIRef(getattr(bprov, "dataExtractionActivity_" + arborist_version))
    g.add((crdfma, RDF.type, prov.Activity))
    g.add(
        (
            crdfma,
            RDFS.label,
            Literal(
                "Activity to create instances of flowObjects, activityTypes and Locations"
            ),
        )
    )
    g.add((crdfma, prov.used, URIRef("http://ontology.bonsai.uno/core")))
    g.add((crdfma, prov.used, getattr(bprov, "exiobaseDataset_" + exiobase_version)))
    g.add((crdfma, prov.hadPlan, URIRef(bprov.extractionScript)))
    g.add((crdfma, prov.wasAssociatedWith, URIRef(bfoaf.bonsai)))
    g.add((crdfma, OWL.versionInfo, Literal(arborist_version)))

    plan = URIRef(bprov.extractionScript)
    g.add((plan, RDF.type, prov.Plan))
    g.add((plan, RDF.type, prov.Entity))
    g.add((plan, RDFS.label, Literal("Entity representing the latest version of the Arborist Script")))
    g.add((plan, prov.hadPrimarySource, URIRef(arborist_url)))

    write_graph(output_base_dir / "prov", g)