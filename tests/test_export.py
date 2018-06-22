# -*- coding: utf-8 -*-

"""Tests for exporting CX to RDF."""

import json
import unittest

from ndex2 import NiceCXNetwork
from ndex2.cx import CX_CONSTANTS
from ndex2.cx.aspects.CitationElement import CitationElement
from ndex2.cx.aspects.SupportElement import SupportElement
from rdflib import Graph

from cx_rdf import cx_to_rdf_graph


class TestExport(unittest.TestCase):
    """Tests for exporting CX to RDF."""

    @classmethod
    def setUpClass(cls):
        """Set up nice CX network and JSON."""
        ncx = NiceCXNetwork()
        ncx.set_name('Test Name')

        a, b, c, d, e = [
            ncx.create_node(node_name=letter)
            for letter in 'ABCDE'
        ]

        e1 = ncx.create_edge(
            edge_source=a,
            edge_target=b,
        )

        e2 = ncx.create_edge(
            edge_source=b,
            edge_target=c,
            edge_interaction='increases',
        )

        c1 = CitationElement(id=0, title='Hi')
        ncx.add_citation(c1)

        s1 = SupportElement(id=0, text='Hi')
        ncx.add_support(s1)

        ncx.add_node_attribute(property_of=a, name='Color', values='Red')
        ncx.add_node_attribute(property_of=b, name='Color', values='Red')
        ncx.add_node_attribute(property_of=c, name='Color', values='Red')
        ncx.add_node_attribute(property_of=d, name='Color', values='Blue')
        ncx.add_node_attribute(property_of=e, name='Color', values='Blue')

        ncx.add_edge_attribute(property_of=e1, name='Color', values='Green')
        ncx.add_edge_attribute(property_of=e2, name='Color', values='Purple')

        ncx.add_edge_citations(edge_id=e1, citation_id=c1.get_id())

        edge_support_element_1 = {CX_CONSTANTS.PROPERTY_OF: [e1], CX_CONSTANTS.SUPPORTS: [c1.get_id()]}
        ncx.add_edge_supports(edge_supports_element=edge_support_element_1)

        cls.cx_json = json.loads(json.dumps(ncx.to_cx()))
        print(json.dumps(cls.cx_json, indent=2))

    def test_export_aspect_policy(self):
        graph = cx_to_rdf_graph(self.cx_json, policy='aspect')
        self.assertIsInstance(graph, Graph)

        print(f'\nResulting ASPECT graph ({len(graph)} triplets):\n')
        print(graph.serialize(format='turtle').decode('utf-8'))

    def test_export_predicate_policy(self):
        graph = cx_to_rdf_graph(self.cx_json, policy='predicate')
        self.assertIsInstance(graph, Graph)

        print(f'\nResulting PREDICATE graph ({len(graph)} triplets):\n')
        print(graph.serialize(format='turtle').decode('utf-8'))

    def test_export_abstract_policy(self):
        graph = cx_to_rdf_graph(self.cx_json, policy='abstract')
        self.assertIsInstance(graph, Graph)

        print(f'\nResulting ABSRAC graph ({len(graph)} triplets):\n')
        print(graph.serialize(format='turtle').decode('utf-8'))
