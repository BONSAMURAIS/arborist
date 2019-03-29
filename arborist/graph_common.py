from rdflib import Literal, RDF, URIRef, Namespace
from rdflib.namespace import DC, RDFS, OWL, FOAF, XSD
import datetime


class CommonNamespaces:
    def __init__(self):
        self.nb = Namespace("http://ontology.bonsai.uno/core#")
        self.owltime = Namespace("https://www.w3.org/TR/owl-time/")
        self.vann = Namespace("http://purl.org/vocab/vann/")
        self.dt = Namespace("http://purl.org/dc/dcmitype/")

NS = CommonNamespaces()


def add_common_elements(graph, base_uri, title, description, author, version):
    """Add common graphs binds (abbreviations for longer namespaces) and a ``Dataset`` element.

    Input arguments:

    * ``graph``: A ``rdflib.Graph`` object
    * ``base_uri``: A string URI. Must end with ``/``.
    * ``title``, ``description``, ``author``, ``version``: Strings describing the relevant properties.

    Returns the modified graph.

    """
    if not base_uri.endswith("/"):
        raise ValueError("`base_uri` must end with '/'")

    graph.bind('bont', 'http://ontology.bonsai.uno/core#')
    graph.bind("dc", DC)
    graph.bind("foaf", FOAF)
    graph.bind("owl", OWL)
    graph.bind("ot", "https://www.w3.org/TR/owl-time/")
    graph.bind("dtype", "http://purl.org/dc/dcmitype/")

    node = URIRef(base_uri)
    graph.add( (node, RDF.type, NS.dt.Dataset) )
    graph.add( (node, DC.title, Literal(title)) )
    graph.add( (node, DC.description, Literal(description)) )
    graph.add( (node, FOAF.homepage, URIRef(base_uri + "documentation.html")) )
    graph.add( (node, NS.vann.preferredNamespaceUri, URIRef(base_uri + "#")) )
    graph.add( (node, OWL.versionInfo, Literal(version)) )
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    graph.add( (node, DC.modified,
            Literal(today, datatype=XSD.date)) )
    graph.add( (node, DC.publisher, Literal("bonsai.uno")) )
    graph.add( (node, DC.creator, URIRef("http://bonsai.uno/foaf/bonsai.rdf#bonsai")) )
    graph.add( (node, DC.contributor, Literal(author)) )
    graph.add( (node, URIRef("http://creativecommons.org/ns#license"), URIRef('http://creativecommons.org/licenses/by/3.0/')) )

    return graph
