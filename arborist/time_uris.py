from .filesystem import write_graph
from .graph_common import add_common_elements
from pathlib import Path
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import RDFS, OWL, XSD


def generate_time_uris(output_base_dir):
    """Time URIs used for now. Hard coded because no external data to consume."""
    output_base_dir = Path(output_base_dir)

    WIKIDATA_MAPPING = {
        1800: "http://www.wikidata.org/entity/Q6875",
        1801: "http://www.wikidata.org/entity/Q6877",
        1802: "http://www.wikidata.org/entity/Q6883",
        1803: "http://www.wikidata.org/entity/Q6887",
        1804: "http://www.wikidata.org/entity/Q6894",
        1805: "http://www.wikidata.org/entity/Q6898",
        1806: "http://www.wikidata.org/entity/Q6903",
        1807: "http://www.wikidata.org/entity/Q6909",
        1808: "http://www.wikidata.org/entity/Q6914",
        1809: "http://www.wikidata.org/entity/Q6919",
        1810: "http://www.wikidata.org/entity/Q6922",
        1811: "http://www.wikidata.org/entity/Q6928",
        1812: "http://www.wikidata.org/entity/Q6933",
        1813: "http://www.wikidata.org/entity/Q6937",
        1814: "http://www.wikidata.org/entity/Q6943",
        1815: "http://www.wikidata.org/entity/Q6948",
        1816: "http://www.wikidata.org/entity/Q6953",
        1817: "http://www.wikidata.org/entity/Q6958",
        1818: "http://www.wikidata.org/entity/Q6964",
        1819: "http://www.wikidata.org/entity/Q6967",
        1820: "http://www.wikidata.org/entity/Q6973",
        1821: "http://www.wikidata.org/entity/Q6976",
        1822: "http://www.wikidata.org/entity/Q6983",
        1823: "http://www.wikidata.org/entity/Q6988",
        1824: "http://www.wikidata.org/entity/Q6994",
        1825: "http://www.wikidata.org/entity/Q6997",
        1826: "http://www.wikidata.org/entity/Q7004",
        1827: "http://www.wikidata.org/entity/Q7008",
        1828: "http://www.wikidata.org/entity/Q7570",
        1829: "http://www.wikidata.org/entity/Q7572",
        1830: "http://www.wikidata.org/entity/Q7576",
        1831: "http://www.wikidata.org/entity/Q7579",
        1832: "http://www.wikidata.org/entity/Q7584",
        1833: "http://www.wikidata.org/entity/Q7587",
        1834: "http://www.wikidata.org/entity/Q7591",
        1835: "http://www.wikidata.org/entity/Q7597",
        1836: "http://www.wikidata.org/entity/Q7601",
        1837: "http://www.wikidata.org/entity/Q7608",
        1838: "http://www.wikidata.org/entity/Q7612",
        1839: "http://www.wikidata.org/entity/Q7616",
        1840: "http://www.wikidata.org/entity/Q7619",
        1841: "http://www.wikidata.org/entity/Q7622",
        1842: "http://www.wikidata.org/entity/Q7625",
        1843: "http://www.wikidata.org/entity/Q7629",
        1844: "http://www.wikidata.org/entity/Q7633",
        1845: "http://www.wikidata.org/entity/Q7636",
        1846: "http://www.wikidata.org/entity/Q7640",
        1847: "http://www.wikidata.org/entity/Q7644",
        1848: "http://www.wikidata.org/entity/Q7647",
        1849: "http://www.wikidata.org/entity/Q7650",
        1850: "http://www.wikidata.org/entity/Q7653",
        1851: "http://www.wikidata.org/entity/Q7656",
        1852: "http://www.wikidata.org/entity/Q7661",
        1853: "http://www.wikidata.org/entity/Q7666",
        1854: "http://www.wikidata.org/entity/Q7670",
        1855: "http://www.wikidata.org/entity/Q7673",
        1856: "http://www.wikidata.org/entity/Q7676",
        1857: "http://www.wikidata.org/entity/Q7680",
        1858: "http://www.wikidata.org/entity/Q7684",
        1859: "http://www.wikidata.org/entity/Q7687",
        1860: "http://www.wikidata.org/entity/Q7691",
        1861: "http://www.wikidata.org/entity/Q7693",
        1862: "http://www.wikidata.org/entity/Q7698",
        1863: "http://www.wikidata.org/entity/Q7701",
        1864: "http://www.wikidata.org/entity/Q7704",
        1865: "http://www.wikidata.org/entity/Q7708",
        1866: "http://www.wikidata.org/entity/Q7712",
        1867: "http://www.wikidata.org/entity/Q7715",
        1868: "http://www.wikidata.org/entity/Q7717",
        1869: "http://www.wikidata.org/entity/Q7720",
        1870: "http://www.wikidata.org/entity/Q7741",
        1871: "http://www.wikidata.org/entity/Q7746",
        1872: "http://www.wikidata.org/entity/Q7753",
        1873: "http://www.wikidata.org/entity/Q7757",
        1874: "http://www.wikidata.org/entity/Q7761",
        1875: "http://www.wikidata.org/entity/Q7764",
        1876: "http://www.wikidata.org/entity/Q7766",
        1877: "http://www.wikidata.org/entity/Q7773",
        1878: "http://www.wikidata.org/entity/Q7776",
        1879: "http://www.wikidata.org/entity/Q7783",
        1880: "http://www.wikidata.org/entity/Q7806",
        1881: "http://www.wikidata.org/entity/Q7808",
        1882: "http://www.wikidata.org/entity/Q7812",
        1883: "http://www.wikidata.org/entity/Q7816",
        1884: "http://www.wikidata.org/entity/Q7819",
        1885: "http://www.wikidata.org/entity/Q7821",
        1886: "http://www.wikidata.org/entity/Q7822",
        1887: "http://www.wikidata.org/entity/Q7826",
        1888: "http://www.wikidata.org/entity/Q7829",
        1889: "http://www.wikidata.org/entity/Q7831",
        1890: "http://www.wikidata.org/entity/Q7832",
        1891: "http://www.wikidata.org/entity/Q7837",
        1892: "http://www.wikidata.org/entity/Q7839",
        1893: "http://www.wikidata.org/entity/Q7840",
        1894: "http://www.wikidata.org/entity/Q7843",
        1895: "http://www.wikidata.org/entity/Q7844",
        1896: "http://www.wikidata.org/entity/Q7846",
        1897: "http://www.wikidata.org/entity/Q7847",
        1898: "http://www.wikidata.org/entity/Q7848",
        1899: "http://www.wikidata.org/entity/Q7851",
        1900: "http://www.wikidata.org/entity/Q2034",
        1901: "http://www.wikidata.org/entity/Q2035",
        1902: "http://www.wikidata.org/entity/Q2043",
        1903: "http://www.wikidata.org/entity/Q2045",
        1904: "http://www.wikidata.org/entity/Q2046",
        1905: "http://www.wikidata.org/entity/Q2047",
        1906: "http://www.wikidata.org/entity/Q2049",
        1907: "http://www.wikidata.org/entity/Q2048",
        1908: "http://www.wikidata.org/entity/Q2056",
        1909: "http://www.wikidata.org/entity/Q2057",
        1910: "http://www.wikidata.org/entity/Q2075",
        1911: "http://www.wikidata.org/entity/Q2076",
        1912: "http://www.wikidata.org/entity/Q2077",
        1913: "http://www.wikidata.org/entity/Q2080",
        1914: "http://www.wikidata.org/entity/Q2083",
        1915: "http://www.wikidata.org/entity/Q2084",
        1916: "http://www.wikidata.org/entity/Q2087",
        1917: "http://www.wikidata.org/entity/Q2092",
        1918: "http://www.wikidata.org/entity/Q2094",
        1919: "http://www.wikidata.org/entity/Q2157",
        1920: "http://www.wikidata.org/entity/Q2155",
        1921: "http://www.wikidata.org/entity/Q2162",
        1922: "http://www.wikidata.org/entity/Q2165",
        1923: "http://www.wikidata.org/entity/Q2169",
        1924: "http://www.wikidata.org/entity/Q2173",
        1925: "http://www.wikidata.org/entity/Q18107",
        1926: "http://www.wikidata.org/entity/Q5259",
        1927: "http://www.wikidata.org/entity/Q18110",
        1928: "http://www.wikidata.org/entity/Q19715",
        1929: "http://www.wikidata.org/entity/Q18792",
        1930: "http://www.wikidata.org/entity/Q18787",
        1931: "http://www.wikidata.org/entity/Q18782",
        1932: "http://www.wikidata.org/entity/Q18743",
        1933: "http://www.wikidata.org/entity/Q18726",
        1934: "http://www.wikidata.org/entity/Q18714",
        1935: "http://www.wikidata.org/entity/Q18658",
        1936: "http://www.wikidata.org/entity/Q18649",
        1937: "http://www.wikidata.org/entity/Q18647",
        1938: "http://www.wikidata.org/entity/Q18645",
        1939: "http://www.wikidata.org/entity/Q18639",
        1940: "http://www.wikidata.org/entity/Q18633",
        1941: "http://www.wikidata.org/entity/Q5231",
        1942: "http://www.wikidata.org/entity/Q18625",
        1943: "http://www.wikidata.org/entity/Q18623",
        1944: "http://www.wikidata.org/entity/Q5268",
        1945: "http://www.wikidata.org/entity/Q5240",
        1946: "http://www.wikidata.org/entity/Q18610",
        1947: "http://www.wikidata.org/entity/Q5263",
        1948: "http://www.wikidata.org/entity/Q5165",
        1949: "http://www.wikidata.org/entity/Q5188",
        1950: "http://www.wikidata.org/entity/Q18597",
        1951: "http://www.wikidata.org/entity/Q18591",
        1952: "http://www.wikidata.org/entity/Q5272",
        1953: "http://www.wikidata.org/entity/Q18585",
        1954: "http://www.wikidata.org/entity/Q18581",
        1955: "http://www.wikidata.org/entity/Q18577",
        1956: "http://www.wikidata.org/entity/Q5221",
        1957: "http://www.wikidata.org/entity/Q5311",
        1958: "http://www.wikidata.org/entity/Q5253",
        1959: "http://www.wikidata.org/entity/Q5302",
        1960: "http://www.wikidata.org/entity/Q3754",
        1961: "http://www.wikidata.org/entity/Q3696",
        1962: "http://www.wikidata.org/entity/Q2764",
        1963: "http://www.wikidata.org/entity/Q2755",
        1964: "http://www.wikidata.org/entity/Q2652",
        1965: "http://www.wikidata.org/entity/Q2650",
        1966: "http://www.wikidata.org/entity/Q2649",
        1967: "http://www.wikidata.org/entity/Q2648",
        1968: "http://www.wikidata.org/entity/Q2644",
        1969: "http://www.wikidata.org/entity/Q2485",
        1970: "http://www.wikidata.org/entity/Q2474",
        1971: "http://www.wikidata.org/entity/Q2475",
        1972: "http://www.wikidata.org/entity/Q2476",
        1973: "http://www.wikidata.org/entity/Q2477",
        1974: "http://www.wikidata.org/entity/Q2478",
        1975: "http://www.wikidata.org/entity/Q2479",
        1976: "http://www.wikidata.org/entity/Q2480",
        1977: "http://www.wikidata.org/entity/Q2481",
        1978: "http://www.wikidata.org/entity/Q2483",
        1979: "http://www.wikidata.org/entity/Q2484",
        1980: "http://www.wikidata.org/entity/Q2439",
        1981: "http://www.wikidata.org/entity/Q2437",
        1982: "http://www.wikidata.org/entity/Q2436",
        1983: "http://www.wikidata.org/entity/Q2434",
        1984: "http://www.wikidata.org/entity/Q2432",
        1985: "http://www.wikidata.org/entity/Q2431",
        1986: "http://www.wikidata.org/entity/Q2430",
        1987: "http://www.wikidata.org/entity/Q2429",
        1988: "http://www.wikidata.org/entity/Q2426",
        1989: "http://www.wikidata.org/entity/Q2425",
        1990: "http://www.wikidata.org/entity/Q2064",
        1991: "http://www.wikidata.org/entity/Q2062",
        1992: "http://www.wikidata.org/entity/Q2060",
        1993: "http://www.wikidata.org/entity/Q2065",
        1994: "http://www.wikidata.org/entity/Q2067",
        1995: "http://www.wikidata.org/entity/Q2068",
        1996: "http://www.wikidata.org/entity/Q2070",
        1997: "http://www.wikidata.org/entity/Q2088",
        1998: "http://www.wikidata.org/entity/Q2089",
        1999: "http://www.wikidata.org/entity/Q2091",
        2000: "http://www.wikidata.org/entity/Q1985",
        2001: "http://www.wikidata.org/entity/Q1988",
        2002: "http://www.wikidata.org/entity/Q1987",
        2003: "http://www.wikidata.org/entity/Q1986",
        2004: "http://www.wikidata.org/entity/Q2014",
        2005: "http://www.wikidata.org/entity/Q2019",
        2006: "http://www.wikidata.org/entity/Q2021",
        2007: "http://www.wikidata.org/entity/Q2024",
        2008: "http://www.wikidata.org/entity/Q2004",
        2009: "http://www.wikidata.org/entity/Q1996",
        2010: "http://www.wikidata.org/entity/Q1995",
        2011: "http://www.wikidata.org/entity/Q1994",
        2012: "http://www.wikidata.org/entity/Q1990",
        2013: "http://www.wikidata.org/entity/Q1998",
        2014: "http://www.wikidata.org/entity/Q1999",
        2015: "http://www.wikidata.org/entity/Q2002",
        2016: "http://www.wikidata.org/entity/Q25245",
        2017: "http://www.wikidata.org/entity/Q25290",
        2018: "http://www.wikidata.org/entity/Q25291",
        2019: "http://www.wikidata.org/entity/Q25274",
        2020: "http://www.wikidata.org/entity/Q25337",
        2021: "http://www.wikidata.org/entity/Q49628",
        2022: "http://www.wikidata.org/entity/Q49625",
        2023: "http://www.wikidata.org/entity/Q49622",
        2024: "http://www.wikidata.org/entity/Q49619",
        2025: "http://www.wikidata.org/entity/Q49616",
        2026: "http://www.wikidata.org/entity/Q49613",
        2027: "http://www.wikidata.org/entity/Q12814",
        2028: "http://www.wikidata.org/entity/Q12809",
        2029: "http://www.wikidata.org/entity/Q12803",
        2030: "http://www.wikidata.org/entity/Q12799",
        2031: "http://www.wikidata.org/entity/Q12794",
        2032: "http://www.wikidata.org/entity/Q12790",
        2033: "http://www.wikidata.org/entity/Q12786",
        2034: "http://www.wikidata.org/entity/Q12775",
        2035: "http://www.wikidata.org/entity/Q12127",
        2036: "http://www.wikidata.org/entity/Q12123",
        2037: "http://www.wikidata.org/entity/Q12120",
        2038: "http://www.wikidata.org/entity/Q12118",
        2039: "http://www.wikidata.org/entity/Q12112",
        2040: "http://www.wikidata.org/entity/Q12108",
        2041: "http://www.wikidata.org/entity/Q49914",
        2042: "http://www.wikidata.org/entity/Q49915",
        2043: "http://www.wikidata.org/entity/Q49917",
        2044: "http://www.wikidata.org/entity/Q49919",
        2045: "http://www.wikidata.org/entity/Q49920",
        2046: "http://www.wikidata.org/entity/Q49921",
        2047: "http://www.wikidata.org/entity/Q49922",
        2048: "http://www.wikidata.org/entity/Q49923",
        2049: "http://www.wikidata.org/entity/Q49924",
        2050: "http://www.wikidata.org/entity/Q49925",
        2051: "http://www.wikidata.org/entity/Q49926",
        2052: "http://www.wikidata.org/entity/Q49927",
        2053: "http://www.wikidata.org/entity/Q49928",
        2054: "http://www.wikidata.org/entity/Q49929",
        2055: "http://www.wikidata.org/entity/Q49930",
        2056: "http://www.wikidata.org/entity/Q49931",
        2057: "http://www.wikidata.org/entity/Q49932",
        2058: "http://www.wikidata.org/entity/Q49933",
        2059: "http://www.wikidata.org/entity/Q49935",
        2060: "http://www.wikidata.org/entity/Q592410",
        2061: "http://www.wikidata.org/entity/Q844737",
        2062: "http://www.wikidata.org/entity/Q1046496",
        2063: "http://www.wikidata.org/entity/Q1044976",
        2064: "http://www.wikidata.org/entity/Q1044959",
        2065: "http://www.wikidata.org/entity/Q890604",
        2066: "http://www.wikidata.org/entity/Q890609",
        2067: "http://www.wikidata.org/entity/Q890597",
        2068: "http://www.wikidata.org/entity/Q890596",
        2069: "http://www.wikidata.org/entity/Q890591",
        2070: "http://www.wikidata.org/entity/Q890619",
        2071: "http://www.wikidata.org/entity/Q890598",
        2072: "http://www.wikidata.org/entity/Q890576",
        2073: "http://www.wikidata.org/entity/Q668404",
        2074: "http://www.wikidata.org/entity/Q890581",
        2075: "http://www.wikidata.org/entity/Q890559",
        2076: "http://www.wikidata.org/entity/Q890563",
        2077: "http://www.wikidata.org/entity/Q890569",
        2078: "http://www.wikidata.org/entity/Q890571",
        2079: "http://www.wikidata.org/entity/Q890584",
        2080: "http://www.wikidata.org/entity/Q972030",
        2081: "http://www.wikidata.org/entity/Q972085",
        2082: "http://www.wikidata.org/entity/Q972651",
        2083: "http://www.wikidata.org/entity/Q972505",
        2084: "http://www.wikidata.org/entity/Q972519",
        2085: "http://www.wikidata.org/entity/Q972493",
        2086: "http://www.wikidata.org/entity/Q971970",
        2087: "http://www.wikidata.org/entity/Q971996",
        2088: "http://www.wikidata.org/entity/Q972009",
        2089: "http://www.wikidata.org/entity/Q971983",
        2090: "http://www.wikidata.org/entity/Q972326",
        2091: "http://www.wikidata.org/entity/Q972454",
        2092: "http://www.wikidata.org/entity/Q972071",
        2093: "http://www.wikidata.org/entity/Q972053",
        2094: "http://www.wikidata.org/entity/Q972633",
        2095: "http://www.wikidata.org/entity/Q972426",
        2096: "http://www.wikidata.org/entity/Q972412",
        2097: "http://www.wikidata.org/entity/Q692765",
        2098: "http://www.wikidata.org/entity/Q972019",
        2099: "http://www.wikidata.org/entity/Q972339",
        2100: "http://www.wikidata.org/entity/Q11183",
    }

    time_periods = [
        "1845-1899",
        "1900-1909",
        "1910-1919",
        "1920-1929",
        "1930-1939",
        "1940-1949",
        "1950-1959",
        "1960-1969",
        "1970-1979",
        "1980-1989",
        "1990-1999",
        "1995-2007",
        "2000-2005",
        "2000-2012"
    ]

    owltime = Namespace("https://www.w3.org/TR/owl-time/")

    g = add_common_elements(
        Graph(),
        base_uri="http://rdf.bonsai.uno/time",
        title="Years 2010 - 2020",
        description="Complete years 2010 - 2020 for use in BONSAI",
        author="Chris Mutel"
    )

    BRDFTIME = Namespace("http://rdf.bonsai.uno/time#")
    PROV = Namespace("http://www.w3.org/ns/prov#")
    time_node = URIRef("http://rdf.bonsai.uno/time")
    g.bind("brdftime", BRDFTIME)
    g.bind("prov", PROV)

    oneyear = BRDFTIME.oneyearlong
    g.add((oneyear, RDF.type, owltime.DurationDescription))
    g.add((oneyear, owltime.years, Literal("1", datatype=XSD.integer)))

    for year, wd in WIKIDATA_MAPPING.items():
        end = BRDFTIME["{}end".format(year)]
        g.add((end, RDF.type, owltime.Instant))
        g.add(
            (
                end,
                owltime.inXSDDate,
                Literal("{}-12-31".format(year), datatype=XSD.date),
            )
        )

        begin = BRDFTIME["{}start".format(year)]
        g.add((begin, RDF.type, owltime.Instant))
        g.add(
            (
                begin,
                owltime.inXSDDate,
                Literal("{}-01-01".format(year), datatype=XSD.date),
            )
        )

        node = BRDFTIME["{}".format(year)]
        g.add((node, RDF.type, owltime.ProperInterval))
        g.add((node, RDFS.label, Literal(year)))
        g.add((node, owltime.hasBeginning, begin))
        g.add((node, owltime.hasEnd, end))
        g.add((node, owltime.hasDurationDescription, oneyear))
        g.add(
            (
                node,
                owltime.inXSDDate,
                Literal("{}-01-01".format(year), datatype=XSD.date),
            )
        )
        g.add((node, OWL.sameAs, URIRef(wd)))
        g.add(
            (
                node,
                OWL.sameAs,
                URIRef("http://reference.data.gov.uk/doc/year/{}".format(year)),
            )
        )

        # Adding Provenance
        g.add((time_node, PROV.hadMember, node))

    for period in time_periods:
        start, end = period.split("-")
        end_url = BRDFTIME["{}end".format(end)]
        if end not in WIKIDATA_MAPPING:
            g.add((end_url, RDF.type, owltime.Instant))
            g.add(
                (
                    end_url,
                    owltime.inXSDDate,
                    Literal("{}-12-31".format(end), datatype=XSD.date),
                )
            )
        start_url = BRDFTIME["{}start".format(start)]
        if start not in WIKIDATA_MAPPING:
            g.add((start_url, RDF.type, owltime.Instant))
            g.add(
                (
                    start_url,
                    owltime.inXSDDate,
                    Literal("{}-01-01".format(start), datatype=XSD.date),
                )
            )

        node = BRDFTIME["{}".format(period.replace("-", "_"))]
        g.add((node, RDF.type, owltime.ProperInterval))
        g.add((node, RDFS.label, Literal(period)))
        g.add((node, owltime.hasBeginning, start_url))
        g.add((node, owltime.hasEnd, end_url))

    write_graph(output_base_dir / "time", g)
