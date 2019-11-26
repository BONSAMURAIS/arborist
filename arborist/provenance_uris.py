from .filesystem import write_graph
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, SKOS, DC, OWL, XSD, RDFS
import datetime


def generate_provenance_uris(output_base_dir, exiobaseVersion, arboristVersion):

    exiobaseVersion = exiobaseVersion.replace(".", "_")
    arboristVersion = arboristVersion.replace(".", "_")
    prov = Namespace("http://www.w3.org/ns/prov/")
    purl = Namespace("http://purl.org/dc/dcmitype/")
    bfoaf = Namespace("https://bonsai.uno/foaf/")
    bprov = Namespace("http://rdf.bonsai.uno/prov/")
    dtype = Namespace("http://purl.org/dc/dcmitype/")

    g = Graph()
    g.bind("org", "https://www.w3.org/TR/vocab-org/")
    g.bind("dtype", "http://purl.org/dc/dcmitype/")
    g.bind("skos", SKOS)
    g.bind("foaf", FOAF)
    g.bind("dc", DC)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("prov", "http://www.w3.org/ns/prov/")
    g.bind("bfoaf", "https://rdf.bonsai.uno/foaf/")
    g.bind("bprov", "http://rdf.bonsai.uno/prov/")

    node = URIRef(bprov)
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    g.add((node, RDF.type, dtype.Dataset))
    g.add((node, DC.creator, bfoaf.bonsai))
    g.add((node, DC.license, URIRef("https://creativecommons.org/licenses/by/3.0/")))
    g.add((node, DC.modified, Literal(today, datatype=XSD.date)))
    g.add((node, DC.publisher, Literal("bonsai.uno")))
    g.add((node, DC.title, Literal("The BONSAI Organization")))
    g.add((node, OWL.versionInfo, Literal("1.0")))

    # Abstract Exiobase Dataset
    ebd = URIRef(bprov.exiobaseDataset)
    g.add((ebd, RDF.type, purl.Dataset))
    g.add((ebd, RDF.type, prov.Entity))
    g.add(
        (
            ebd,
            RDFS.label,
            Literal(
                "A LCSA dataset created by the EXIOBASE-Consortium"
            ),
        )
    )
    g.add((ebd, prov.wasAttributedTo, URIRef(bfoaf.exiobase_consortium)))
    g.add((ebd, DC.term("rights"), Literal("Copyright © 2015 - EXIOBASE Consortium")))

    # Specific instance of exiobase dataset
    edbSpecific = URIRef(getattr(bprov, "exiobaseDataset_" + exiobaseVersion))
    g.add((edbSpecific, RDF.type, bprov.exiobaseDataset))
    g.add(
        (
            edbSpecific,
            RDFS.label,
            Literal(
                "The Exiobase Dataset version " + exiobaseVersion
            ),
        )
    )
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    g.add((edbSpecific, DC.term("license"), URIRef("https://www.exiobase.eu/index.php/terms-of-use")))
    g.add((edbSpecific, DC.term("date"), Literal(today, datatype=XSD.date)))

    # Abstract createRDFModelActivity
    crdfma = URIRef(bprov.dataExtractionActivity)
    g.add((crdfma, RDF.type, prov.Activity))
    g.add(
        (
            crdfma,
            RDFS.label,
            Literal(
                "Activity to create instances of flowObjects, activityTypes and Locations based on a dataset"
            ),
        )
    )
    g.add((crdfma, prov.wasAssociatedWith, URIRef(bfoaf.bonsai)))

    # Instance of createRDFModelActivity
    crdfmaConcrete = URIRef(getattr(bprov, "dataExtractionActivity_" + arboristVersion))
    g.add((crdfmaConcrete, RDF.type, bprov.dataExtractionActivity))
    g.add(
        (
            crdfmaConcrete,
            RDFS.label,
            Literal(
                "Concrete instance of dataExtractionActivity, version " + arboristVersion
            ),
        )
    )
    g.add((crdfmaConcrete, prov.used, URIRef("http://ontology.bonsai.uno/core")))
    g.add((crdfmaConcrete, prov.used, getattr(bprov, "exiobaseDataset_" + exiobaseVersion)))
    write_graph(output_base_dir / "prov", g)