"""Time URIs used for now. Hard coded because no external data to consume."""
import json
from pathlib import Path
from .filesystem import create_dir


DOCKER = """
Please run the following to convert JSON-LD to TTL:

    cd "{}"
    docker run -it --rm -v `pwd`:/rdf stain/jena riot -out Turtle time/time.jsonld > time/time.ttl
"""


class ProperInterval:
    def __init__(self, years):
        """``years`` is a list of integer years."""
        self.years = years
        self.filename = "time"

    def map_wikidata_year(self, year):
        MAPPING = {
            2011: "https://www.wikidata.org/wiki/Q1994",
            2015: "https://www.wikidata.org/wiki/Q2002",
            2016: "https://www.wikidata.org/wiki/Q25245",
            2017: "https://www.wikidata.org/wiki/Q25290",
            2018: "https://www.wikidata.org/wiki/Q25291",
        }
        return MAPPING[year]

    def get_data(self):
        data = {
            "@context" : {
                "years" : {
                    "@id" : "https://www.w3.org/TR/owl-time/years",
                    "@type" : "http://www.w3.org/2001/XMLSchema#integer"
                },
                "sameAs" : {
                    "@id" : "http://www.w3.org/2002/07/owl#sameAs",
                    "@type" : "@id"
                },
                "hasEnd" : {
                    "@id" : "https://www.w3.org/TR/owl-time/hasEnd",
                    "@type" : "@id"
                },
                "hasDurationDescription" : {
                    "@id" : "https://www.w3.org/TR/owl-time/hasDurationDescription",
                "@type" : "@id"
                },
                "hasBeginning" : {
                    "@id" : "https://www.w3.org/TR/owl-time/hasBeginning",
                    "@type" : "@id"
                },
                "inXSDDate" : {
                    "@id" : "https://www.w3.org/TR/owl-time/inXSDDate",
                    "@type" : "http://www.w3.org/2001/XMLSchema#date"
                },
                "brdftim" : "http://rdf.bonsai.uno/time/",
                "time" : "https://www.w3.org/TR/owl-time/",
                },
            "@graph": [{
                "@id" : "brdftim:oneyearlong",
                "@type" : "time:DurationDescription",
                "time:years" : 1
            }]
        }
        for year in self.years:
            data['@graph'].extend([{
                "@id": "brdftim:{}end".format(year),
                "@type": "time:Instant",
                "inXSDDate": "{}-12-31".format(year),
            }, {
                "@id": "brdftim:{}start".format(year),
                "@type": "time:Instant",
                "inXSDDate": "{}-01-01".format(year),
            }, {
                "@id": "brdftim:{}".format(year),
                "@type": "time:ProperInterval",
                "sameAs": [
                    self.map_wikidata_year(year),
                    "http://reference.data.gov.uk/doc/year/{}".format(year)
                ],
                "hasBeginning": "brdftim:{}start".format(year),
                "hasDurationDescription": "brdftim:oneyearlong",
                "hasEnd": "brdftim:{}end".format(year),
            }])
        return data

    def write_file(self, output_dir):
        create_dir(output_dir / "time")
        with open(output_dir / "time" / (self.filename + ".jsonld"), "w", encoding='utf-8') as f:
            json.dump(self.get_data(), f, ensure_ascii=False, indent=2)


def generate_time_uris(output_base_dir):
    time = ProperInterval([2011, 2016, 2017, 2018])
    time.write_file(Path(output_base_dir))
    print(DOCKER.format(output_base_dir))
