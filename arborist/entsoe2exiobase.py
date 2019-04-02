from .filesystem import create_dir
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import DC, RDFS, OWL, XSD,FOAF
import pandas
from . import data_dir

def generate_entsoe_uris(output_base_dir):
    
    #add namespaces
    nb = Namespace("http://ontology.bonsai.uno/core#")
    nat = Namespace("http://rdf.bonsai.uno/activitytype/exiobase3_3_17/")
    

    #add prefix
    g = Graph()
    g.bind('bont', 'http://ontology.bonsai.uno/core#')
    g.bind('brdfat', 'http://rdf.bonsai.uno/activitytype/exiobase3_3_17/')
    g.bind('dtype','http://purl.org/dc/dcmitype/')
    g.bind('cc','http://creativecommons.org/ns#')
    g.bind('ns0','http://purl.org/vocab/vann/')
    g.bind('brdaten','http://rdf.bonsai.uno/activitytype/entsoe/')

    g.bind("dc", DC)
    g.bind("owl", OWL)
    g.bind("xsd", XSD)
    g.bind("rdfs",RDFS)
    g.bind("foaf",FOAF)

    
    data = pandas.read_csv(data_dir / 'entsoe2exiobase.csv')

    data['entsoe_name']=data['entsoe name'].str.replace('\s|/','_',
        regex=True)

    for r in data.iterrows():
        exiobase_code=r[1]['exiobase code']
        entsoe_code=r[1]['entsoe_name']
        entsoe_label=r[1]['entsoe name']

        #this is hardcoding is wrong
        entsoe_uri='http://rdf.bonsai.uno/activitytype/entsoe/'+entsoe_code
        
        g.add( ("brdaten:{}".format(entsoe_code),
                 RDF.type,
                 nb.ActivityType) )
        
        g.add( ("brdaten:{}".format(entsoe_code),
                OWL.sameAs,
                'brdfat:{}'.format(exiobase_code)))
        
        g.add( ("brdaten:{}".format(entsoe_code),
                RDFS.label,
                entsoe_label
               )
             )

        #f.write('brdfatb:{} a bont:ActivityType;\n'.format(r[1]['brdfatb']))
        #f.write('  owl:sameAs brdfat:{};\n'.format(r[1]['brdfat']))
        #f.write('  rdfs:label:"{}".\n'.format(r[1]['rdfs:label']))
        #f.write('\n')

        #brdfatb:Wind_Onshore a bont:ActivityType;
        #owl:sameAs brdfat:A_POWW;
        #rdfs:label:"Wind Onshore".

        #print(entsoe_uri)/

    create_dir(output_base_dir / "activitytype" / "entsoe") 
    with open(
            output_base_dir / "activitytype" / "entsoe" / "entsoe.ttl",
            "wb") as f:
        g.serialize(f, format="turtle", encoding='utf-8')

    output_base_dir = Path(output_base_dir)