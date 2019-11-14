from .filesystem import write_graph
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, SKOS, DC, OWL, XSD, RDFS
import datetime


def generate_provenance_uris(output_base_dir, exiobaseVersion, arboristVersion):

    exiobaseVersion = exiobaseVersion.replace(".", "_")
    arboristVersion = arboristVersion.replace(".", "_")
    prov = Namespace("http://www.w3.org/ns/prov/")
    purl = Namespace("http://purl.org/dc/dcmitype/")
    bfoaf = Namespace("http://bonsai.uno/foaf/")
    bprov = Namespace("http://bonsai.uno/prov/")

    g = Graph()
    g.bind("org", "https://www.w3.org/TR/vocab-org/")
    g.bind("dtype", "http://purl.org/dc/dcmitype/")
    g.bind("skos", SKOS)
    g.bind("foaf", FOAF)
    g.bind("dc", DC)
    g.bind("owl", OWL)
    g.bind("rdfs", RDFS)
    g.bind("prov", "http://www.w3.org/ns/prov/")
    g.bind("bfoaf", "http://rdf.bonsai.uno/foaf#")
    g.bind("bprov", "http://bonsai.uno/prov/")

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
    edbSpecific = URIRef(getattr(bprov, "exiobaseDateset_" + exiobaseVersion))
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

    # Arborist agent
    arborist = URIRef(bprov.arboristAgent)
    g.add((arborist, RDF.type, prov.SoftwareAgent))
    g.add(
        (
            arborist,
            RDFS.label,
            Literal(
                "Arborist, a software agent"
            ),
        )
    )
    g.add((arborist, prov.actedOnBehalfOf, bfoaf.bonsai))

    # Abstract createRDFModelActivity
    crdfma = URIRef(bprov.createRDFMOdelActivity)
    g.add((crdfma, RDF.type, prov.Activity))
    g.add(
        (
            crdfma,
            RDFS.label,
            Literal(
                "Activity to create instances of flowObjects, activityTypes and Locations based on the BONSAI ontology and a dataset"
            ),
        )
    )
    g.add((crdfma, prov.wasAssociatedWith, bprov.arboristAgent))

    # Instance of createRDFModelActivity
    crdfmaConcrete = URIRef(getattr(bprov, "createRDFMOdelActivity_" + arboristVersion))
    g.add((crdfmaConcrete, RDF.type, bprov.createRDFMOdelActivity))
    g.add(
        (
            crdfmaConcrete,
            RDFS.label,
            Literal(
                "Concrete instance of createRDFModelActivity, version " + arboristVersion
            ),
        )
    )
    g.add((crdfmaConcrete, prov.used, URIRef("http://ontology.bonsai.uno/core")))
    g.add((crdfmaConcrete, prov.used, getattr(bprov, "exiobaseDataset_" + exiobaseVersion)))
    write_graph(output_base_dir / "prov", g)