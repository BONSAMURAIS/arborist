from .filesystem import write_graph
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, SKOS, DC, OWL, XSD
import datetime
from . import __version__


def generate_foaf_uris(output_base_dir):
    """Note the URIs needed for units. They all come from the Ontology of Units
    of Measure."""
    output_base_dir = Path(output_base_dir)

    org = Namespace("https://www.w3.org/TR/vocab-org/")
    prov = Namespace("http://www.w3.org/ns/prov#")
    bfoaf = Namespace("http://rdf.bonsai.uno/foaf/exiobase3_3_17#")
    bfoaf_b = Namespace("http://rdf.bonsai.uno/foaf/bonsai#")
    dtype = Namespace("http://purl.org/dc/dcmitype/")
    vann = Namespace("http://purl.org/vocab/vann/")
    bprov = Namespace("http://rdf.bonsai.uno/prov/exiobase3_3_17#")

    g = Graph()
    g.bind("vann", vann)
    g.bind("org", org)
    g.bind("dtype", dtype)
    g.bind("skos", SKOS)
    g.bind("foaf", FOAF)
    g.bind("bonsaifoaf", bfoaf_b)
    g.bind("dc", DC)
    g.bind("bprov", bprov)
    g.bind("owl", OWL)
    g.bind("prov", prov)
    g.bind("bfoaf", bfoaf)

    b = Graph()
    b.bind("vann", vann)
    b.bind("org", org)
    b.bind("dtype", dtype)
    b.bind("skos", SKOS)
    b.bind("foaf", FOAF)
    b.bind("bprov", bprov)
    b.bind("dc", DC)
    b.bind("owl", OWL)
    b.bind("prov", prov)
    b.bind("bfoaf", bfoaf_b)

    node = URIRef("http://rdf.bonsai.uno/foaf/exiobase3_3_17")
    node_b = URIRef("http://rdf.bonsai.uno/foaf/bonsai")

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    g.add((node, RDF.type, dtype.Dataset))
    g.add((node, DC.creator, bfoaf_b.bonsai))
    g.add((node, DC.description, Literal("Instances of Organizations")))
    g.add((node, vann.preferredNamespaceUri, URIRef(bfoaf)))
    g.add((node, DC.license, URIRef("https://creativecommons.org/licenses/by/3.0/")))
    g.add((node, DC.modified, Literal(today, datatype=XSD.date)))
    g.add((node, DC.publisher, bfoaf_b.bonsai))
    g.add((node, DC.title, Literal("Organizations")))
    g.add((node, OWL.versionInfo, Literal(__version__)))

    b.add((node_b, RDF.type, dtype.Dataset))
    b.add((node_b, DC.creator, bfoaf_b.bonsai))
    b.add((node_b, DC.description, Literal("Instances of Organizations")))
    b.add((node_b, vann.preferredNamespaceUri, URIRef(bfoaf)))
    b.add((node_b, DC.license, URIRef("https://creativecommons.org/licenses/by/3.0/")))
    b.add((node_b, DC.modified, Literal(today, datatype=XSD.date)))
    b.add((node_b, DC.publisher, bfoaf_b.bonsai))
    b.add((node_b, DC.title, Literal("Organizations")))
    b.add((node_b, OWL.versionInfo, Literal(__version__)))

    bonsai = URIRef(bfoaf_b.bonsai)
    b.add((bonsai, RDF.type, org.Organization))
    b.add((bonsai, RDF.type, prov.Agent))
    b.add(
        (
            bonsai,
            SKOS.prefLabel,
            Literal(
                "BONSAI – Big Open Network for Sustainability Assessment Information"
            ),
        )
    )
    b.add((bonsai, FOAF.homepage, URIRef("https://bonsai.uno")))
    b.add((bonsai, FOAF.interest, URIRef("https://www.wikidata.org/wiki/Q131201")))
    b.add((bonsai, FOAF.interest, URIRef("https://www.wikidata.org/wiki/Q2323664")))
    b.add((bonsai, FOAF.interest, URIRef("https://www.wikidata.org/wiki/Q18692990")))

    # Exiobase_Consortium
    ec = URIRef(bfoaf.exiobase_consortium)
    g.add((ec, RDF.type, org.Organization))
    g.add((ec, RDF.type, prov.Agent))
    g.add(
        (
            ec,
            DC.description,
            Literal("The EXIOBASE consortium consists of NTNU, TNO, SERI, Universiteit Leiden, WU, and 2.-0 LCA Consultant")
        )
    )
    g.add((ec, FOAF.homepage, URIRef("https://www.exiobase.eu/")))

    # Provenance
    b.add((node_b, prov.hadMember, bonsai))
    g.add((node, prov.hadMember, ec))

    # Provenance
    b.add((node_b, RDF.type, prov.Collection))
    b.add((node_b, prov.wasAttributedTo, bfoaf_b.bonsai))
    b.add((node_b, prov.wasGeneratedBy, bprov["dataExtractionActivity_{}".format(__version__.replace(".", "_"))]))
    b.add((node_b, prov.generatedAtTime, Literal(today, datatype=XSD.date)))
    b.add(
        (
            node_b,
            URIRef("http://creativecommons.org/ns#license"),
            URIRef("http://creativecommons.org/licenses/by/3.0/"),
        )
    )

    # Provenance
    g.add((node, RDF.type, prov.Collection))
    g.add((node, prov.wasAttributedTo, bfoaf_b.bonsai))
    g.add((node, prov.wasGeneratedBy, bprov["dataExtractionActivity_{}".format(__version__.replace(".", "_"))]))
    g.add((node, prov.generatedAtTime, Literal(today, datatype=XSD.date)))
    g.add(
        (
            node,
            URIRef("http://creativecommons.org/ns#license"),
            URIRef("http://creativecommons.org/licenses/by/3.0/"),
        )
    )

    write_graph(output_base_dir / "foaf" / "exiobase3_3_17", g)
    write_graph(output_base_dir / "foaf" / "bonsai", b)
