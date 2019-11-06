from .filesystem import write_graph
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, SKOS, DC, OWL, XSD


def generate_foaf_uris(output_base_dir):
    """Note the URIs needed for units. They all come from the Ontology of Units
    of Measure."""
    output_base_dir = Path(output_base_dir)

    org = Namespace("https://www.w3.org/TR/vocab-org/")

    g = Graph()
    g.bind("org", "https://www.w3.org/TR/vocab-org/")
    g.bind("skos", SKOS)
    g.bind("foaf", FOAF)
    g.bind("dc", DC)
    g.bind("owl", OWL)

    node = URIRef("https://bonsai.uno/foaf/foaf.ttl#bonsai")
    g.add((node, RDF.type, org.Organization))
    g.add(
        (
            node,
            SKOS.prefLabel,
            Literal(
                "BONSAI – Big Open Network for Sustainability Assessment Information"
            ),
        )
    )
    g.add((node, FOAF.homepage, URIRef("https://bonsai.uno")))
    g.add((node, FOAF.interest, URIRef("https://www.wikidata.org/wiki/Q131201")))
    g.add((node, FOAF.interest, URIRef("https://www.wikidata.org/wiki/Q2323664")))
    g.add((node, FOAF.interest, URIRef("https://www.wikidata.org/wiki/Q18692990")))

    ds = URIRef("https://bonsai.uno/foaf")
    g.add((ds, RDF.type, URIRef("https://purl.org/dc/dcmitype/Dataset")))
    g.add((ds, DC.creator, node))
    g.add((ds, DC.publisher, Literal("bonsai.uno")))
    g.add((ds, DC.title, Literal("The BONSAI Organization")))
    g.add((ds, DC.description, Literal("Contains information about the BONSAI organization")))
    g.add((ds, OWL.versionInfo, Literal("0.2")))
    g.add((ds, FOAF.homepage, URIRef("https://rdf.bonsai.uno/unit/documentation.html")))
    g.add((ds, DC.license, URIRef("https://creativecommons.org/licenses/by/3.0/")))
    g.add((ds, DC.modified, Literal("2019-04-02", datatype=XSD.date)))

    write_graph(output_base_dir / "foaf", g)
