import os
import json
import ntpath
import warnings
import pkg_resources
from pathlib import Path

import pandas
import pandas as pd
from pyxlsb import open_workbook as open_xlsb
from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import DCTERMS, FOAF, XSD, OWL, RDFS, RDF, SKOS

from . import data_dir
from .filesystem import write_graph
from .graph_common import add_common_elements


def file_name(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def setup_empty_graph():
    global BONT, BRDFFO, BRDFLO, BRDFTIME, BRDFFAT, BRDFFOAF, BRDFDAT, BRDFPROV, dataset
    global CC, DC, DTYPE, NS0, NS1, OM2, OT, SCHEMA, TIME, XML, PROV, extent2011node

    BONT = Namespace('http://ontology.bonsai.uno/core#')
    BRDFFO = Namespace("http://rdf.bonsai.uno/flowobject/exiobase3_3_17#")
    BRDFLO = Namespace("http://rdf.bonsai.uno/location/exiobase3_3_17#")
    BRDFTIME = Namespace("http://rdf.bonsai.uno/time#")
    BRDFFAT = Namespace("http://rdf.bonsai.uno/activitytype/exiobase3_3_17#")
    BRDFFOAF = Namespace("http://rdf.bonsai.uno/foaf/exiobase3_3_17#")
    BRDFDAT = Namespace("http://rdf.bonsai.uno/data/exiobase3_3_17/emission#")
    BRDFPROV = Namespace("http://rdf.bonsai.uno/prov/exiobase3_3_17#")
    CC = Namespace('http://creativecommons.org/ns#')
    DC = Namespace('http://purl.org/dc/elements/1.1/')
    DTYPE = Namespace("http://purl.org/dc/dcmitype/")
    NS0 = Namespace('http://purl.org/vocab/vann/')
    NS1 = Namespace("http://creativecommons.org/ns#")
    OM2 = Namespace('http://www.ontology-of-units-of-measure.org/resource/om-2/')
    OT = Namespace("https://www.w3.org/TR/owl-time/")
    SCHEMA = Namespace('http://schema.org/')
    TIME = Namespace('http://www.w3.org/2006/time#')
    XML = Namespace("http://www.w3.org/XML/1998/namespace")
    PROV = Namespace("http://www.w3.org/ns/prov#")

    extent2011node = URIRef("{}{}".format(BRDFTIME, '2011'))

    dataset = "http://rdf.bonsai.uno/data/exiobase3_3_17/emission"
    g = add_common_elements(
        Graph(),
        base_uri=dataset,
        title="Emission flows from Exiobase",
        description="Extracted emission flows from exiobase extensions table",
        author="BONSAI Team",
    )

    g.bind("bont", BONT)
    g.bind("brdffo", BRDFFO)
    g.bind("brdflo", BRDFLO)
    g.bind("brdftime", BRDFTIME)
    g.bind("brdffat", BRDFFAT)
    g.bind("brdfdat", BRDFDAT)
    g.bind("brdfprov", BRDFPROV)
    g.bind("brdffoaf", BRDFFOAF)
    g.bind("cc", CC)
    g.bind("dc", DC)
    g.bind("dtype", DTYPE)
    g.bind("ns0", NS0)
    g.bind("ns1", NS1)
    g.bind("om2", OM2)
    g.bind("ot", OT)
    g.bind("schema", SCHEMA)
    g.bind("time", TIME)
    g.bind("xml", XML)
    g.bind("prov", PROV)

    return g


def emissions(base_dir, sheetnum = 6):
    csvArr = []
    output_base_dir = Path(base_dir)

    xlsb = "MR_HSUT_2011_v3_3_17_extensions.xlsb"
    file_path = os.path.join(data_dir, xlsb)
    file_handler = pkg_resources.resource_stream(__name__, file_path)

    with open_xlsb(file_handler) as wb:
        # Read the sheet to array first and convert to pandas first for quick access
        with wb.get_sheet(sheetnum) as sheet:
            for row in sheet.rows(sparse=True):
                vals = [item.v for item in row]
                csvArr.append(vals)

    csvDF = pd.DataFrame(csvArr)

    # Get emission codes from exiobase classifications
    file_path = os.path.join(data_dir, "exiobase_classifications_v_3_3_17.xlsx")
    file_handler = pkg_resources.resource_stream(__name__, file_path)
    df2 = pandas.read_excel(
        file_handler,
        sheet_name="Emissions",
        header=0,
    )
    emission_objects = {name: label for name, label in zip(df2["Emission name"], df2["Label"])}

    # Start or and colum take into account headers
    startCol = 3
    startRow = 4
    print("Parsed sheet has size {}".format(csvDF.shape))

    # Create Common Graph
    g = setup_empty_graph()

    # Start triple extraction
    rows = csvDF.shape[0]
    cols = csvDF.shape[1]
    triple_counter = 0
    for i in range(startCol, cols):
        if (i - startCol) % 50 == 1:
            print("Parsed {}".format(i - startCol - 1))
        for j in range(startRow, rows):
            if csvDF.iat[j, i] != 0:  # If we consider
                location = csvDF.iat[0, i]
                activity = csvDF.iat[3, i]
                value = csvDF.iat[j, i]
                emiss = csvDF.iat[j, 0]
                flow_object = emission_objects[emiss]

                # Crete emission output activity
                activity_output = URIRef("{}#A_{}".format(dataset, triple_counter))
                g.add((activity_output, RDF.type, URIRef(BONT.Activity)))
                g.add((
                    activity_output,
                    BONT.hasActivityType,
                    URIRef("{}{}".format(BRDFFAT, activity))
                ))
                g.add((
                    activity_output,
                    BONT.hasTemporalExtent,
                    extent2011node
                ))
                g.add((activity_output, BONT.hasLocation, URIRef("{}{}".format(BRDFLO, location))))
                triple_counter += 1

                # Balanceable Property
                balance = URIRef("{}#B_{}".format(dataset, triple_counter))
                g.add((balance, RDF.type, URIRef(BONT.BalanceableProperty)))
                g.add((balance, BONT.hasBalanceablePropertyType, OM2.DryMass))  # TODO: This is not correct
                g.add((balance, OM2.hasNumericalValue, Literal(value, datatype=XSD.float)))
                g.add((balance, OM2.hasUnit, OM2.tonne))
                g.add((
                    balance,
                    RDFS.label,
                    Literal("{};{} {}".format(emiss, value, 'tonnes'),
                            datatype=XSD.string)
                ))
                triple_counter += 1

                # Here we create the Flow
                flow = URIRef("{}#F_{}".format(dataset, triple_counter))
                g.add((flow, RDF.type, URIRef(BONT.Flow)))
                g.add((flow, BONT.hasObjectType, URIRef("{}{}".format(BRDFFO, flow_object))))
                g.add((flow, OM2.hasUnit, URIRef(OM2.tonne)))
                g.add((flow, BONT.hasBalanceableProperty, balance))
                g.add((flow, OM2.hasNumericalValue, Literal(value, datatype=XSD.float)))
                g.add((flow, BONT.isOutputOf, activity_output))
                triple_counter += 1

                # Provenance Information
                g.add((URIRef(dataset), PROV.hadMember, flow))
                g.add((URIRef(dataset), PROV.hadMember, activity_output))
                g.add((URIRef(dataset), PROV.hadMember, balance))

    write_graph(output_base_dir / "flow" / "exiobase3_3_17" / "emission", g)


def generate_emissions(base_dir):
    config_filename = "config.json"
    file_path = os.path.join(data_dir, config_filename)
    file_handler = pkg_resources.resource_stream(__name__, file_path)

    data = json.load(file_handler)

    if data['extract_exiobase_emissions'] is True:
        try:
            emissions(base_dir)
        except:
            warnings.warn("Exiobase HSUT extensions file must be in data folder to extract emission flows")