#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cdigraphlayout
----------------------------------

Tests for `cdigraphlayout` module.
"""

import os
import sys
import unittest
import io
import tempfile
import shutil
import json
import ndex2
from cdigraphlayout import cdigraphlayoutcmd


class TestCdIgraphLayout(unittest.TestCase):

    TEST_DIR = os.path.dirname(__file__)

    HUNDRED_NODE_DIR = os.path.join(TEST_DIR, 'data',
                                    '100node_example')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_args_all_defaults(self):
        myargs = ['inputarg']
        res = cdigraphlayoutcmd._parse_arguments('desc', myargs)
        self.assertEqual('inputarg', res.input)
        self.assertEqual('auto', res.layout)
        self.assertEqual(None, res.scale)
        self.assertEqual(None, res.fit_into)

    def test_parse_args_scale_and_layoutset(self):
        myargs = ['inputarg', '--layout', 'circle',
                  '--scale', '5.0']
        res = cdigraphlayoutcmd._parse_arguments('desc', myargs)
        self.assertEqual('inputarg', res.input)
        self.assertEqual('circle', res.layout)
        self.assertEqual(5.0, res.scale)
        self.assertEqual(None, res.fit_into)

    def test_parse_args_fit_into_set(self):
        myargs = ['inputarg',
                  '--fit_into', '1,2,3,4']
        res = cdigraphlayoutcmd._parse_arguments('desc', myargs)
        self.assertEqual('inputarg', res.input)
        self.assertEqual('auto', res.layout)
        self.assertEqual(None, res.scale)
        self.assertEqual('1,2,3,4', res.fit_into)

    def test_get_node_size_from_cyvisual_properties_with_none(self):
        try:
            cdigraphlayoutcmd._get_node_size_from_cyvisual_properties()
            self.fail('Expected ValueError')
        except ValueError as ve:
            self.assertEqual('Network passed in cannot be None',
                             str(ve))

    def test_get_node_size_from_cyvisual_properties_network_missing_aspect(self):
        net = ndex2.nice_cx_network.NiceCXNetwork()
        res = cdigraphlayoutcmd._get_node_size_from_cyvisual_properties(net_cx=net)
        self.assertIsNone(res)

    def test_get_node_size_from_cyvisual_properties_on_real_network(self):
        five_node = os.path.join(os.path.dirname(__file__), 'data',
                                 '5node.cx')
        net = ndex2.create_nice_cx_from_file(five_node)
        res = cdigraphlayoutcmd._get_node_size_from_cyvisual_properties(net_cx=net)
        self.assertEqual(85.0, res)

    def test_get_bounding_box_based_on_node_size_with_none(self):
        try:
            cdigraphlayoutcmd._get_bounding_box_based_on_node_size()
            self.fail('Expected ValueError')
        except ValueError as ve:
            self.assertEqual('Network passed in cannot be None',
                             str(ve))

    def test_get_bounding_box_based_on_node_size_with_5node(self):
        five_node = os.path.join(os.path.dirname(__file__), 'data',
                                 '5node.cx')
        net = ndex2.create_nice_cx_from_file(five_node)
        res = cdigraphlayoutcmd._get_bounding_box_based_on_node_size(net_cx=net)
        self.assertEqual((0.0, 0.0, 550.0, 550.0), res.coords)

    def test_get_bounding_box_from_user_str(self):
        self.assertIsNone(cdigraphlayoutcmd.
                          _get_bounding_box_from_user_str(None))

        # test empty str
        try:
            cdigraphlayoutcmd._get_bounding_box_from_user_str('')
            self.fail('Expected ValueError')
        except ValueError as ve:
            self.assertEqual('Could not parse bounding box coordinates from '
                             'input string: ', str(ve))

        # test str with only 1 comma
        try:
            cdigraphlayoutcmd._get_bounding_box_from_user_str('1,2')
            self.fail('Expected ValueError')
        except ValueError as ve:
            self.assertEqual('Could not parse bounding box coordinates from '
                             'input string: 1,2', str(ve))

        # test str with non numeric values
        try:
            cdigraphlayoutcmd._get_bounding_box_from_user_str('1,b,c,d')
            self.fail('Expected ValueError')
        except ValueError as ve:
            self.assertTrue('invalid coordinate' in str(ve))

        # test valid
        res = cdigraphlayoutcmd._get_bounding_box_from_user_str('0.0,1.0,2,3')
        self.assertEqual((0.0, 1.0, 2.0, 3.0), res.coords)

    def test_runlayout_input_is_not_a_file(self):
        temp_dir = tempfile.mkdtemp()
        try:
            args = cdigraphlayoutcmd._parse_arguments('desc',
                                                      [os.path.join(temp_dir,
                                                                    'input')])
            o_stream = io.StringIO()
            e_stream = io.StringIO()
            res = cdigraphlayoutcmd.run_layout(args, out_stream=o_stream,
                                               err_stream=e_stream)
            self.assertEqual(3, res)

        finally:
            shutil.rmtree(temp_dir)

    def test_runlayout_input_is_not_an_empty_file(self):
        temp_dir = tempfile.mkdtemp()
        try:
            input_file = os.path.join(temp_dir, 'input')
            open(input_file, 'a').close()
            args = cdigraphlayoutcmd._parse_arguments('desc',
                                                      [input_file])
            o_stream = io.StringIO()
            e_stream = io.StringIO()
            res = cdigraphlayoutcmd.run_layout(args, out_stream=o_stream,
                                               err_stream=e_stream)
            self.assertEqual(4, res)
        finally:
            shutil.rmtree(temp_dir)

    def test_runlayout_on_5node(self):
        temp_dir = tempfile.mkdtemp()
        try:
            five_node = os.path.join(os.path.dirname(__file__), 'data',
                                     '5node.cx')

            args = cdigraphlayoutcmd._parse_arguments('desc',
                                                      [five_node])
            o_stream = io.StringIO()
            e_stream = io.StringIO()
            res = cdigraphlayoutcmd.run_layout(args, out_stream=o_stream,
                                               err_stream=e_stream)
            self.assertEqual('', e_stream.getvalue())
            self.assertEqual(0, res)
            cart_layout = json.loads(o_stream.getvalue())
            self.assertTrue(isinstance(cart_layout, list))
            self.assertEqual(5, len(cart_layout))
            for entry in cart_layout:
                self.assertTrue('node' in entry)
                self.assertTrue('x' in entry)
                self.assertTrue('y' in entry)
                self.assertTrue(entry['node'] in [175, 180, 185, 190, 195])
        finally:
            shutil.rmtree(temp_dir)

    def test_runlayout_on_5node_scale_set(self):
        temp_dir = tempfile.mkdtemp()
        try:
            five_node = os.path.join(os.path.dirname(__file__), 'data',
                                     '5node.cx')

            args = cdigraphlayoutcmd._parse_arguments('desc',
                                                      [five_node,
                                                       '--scale',
                                                       '10.0'])
            o_stream = io.StringIO()
            e_stream = io.StringIO()
            res = cdigraphlayoutcmd.run_layout(args, out_stream=o_stream,
                                               err_stream=e_stream)
            self.assertEqual('', e_stream.getvalue())
            self.assertEqual(0, res)
            cart_layout = json.loads(o_stream.getvalue())
            self.assertTrue(isinstance(cart_layout, list))
            self.assertEqual(5, len(cart_layout))
            for entry in cart_layout:
                self.assertTrue('node' in entry)
                self.assertTrue('x' in entry)
                self.assertTrue('y' in entry)
                self.assertTrue(entry['node'] in [175, 180, 185, 190, 195])
        finally:
            shutil.rmtree(temp_dir)

    def test_runlayout_on_5node_fit_into_set(self):
        temp_dir = tempfile.mkdtemp()
        try:
            five_node = os.path.join(os.path.dirname(__file__), 'data',
                                     '5node.cx')

            args = cdigraphlayoutcmd._parse_arguments('desc',
                                                      [five_node,
                                                       '--fit_into',
                                                       '0.0,0.0,1.0,1.0'])
            o_stream = io.StringIO()
            e_stream = io.StringIO()
            res = cdigraphlayoutcmd.run_layout(args, out_stream=o_stream,
                                               err_stream=e_stream)
            self.assertEqual('', e_stream.getvalue())
            self.assertEqual(0, res)
            cart_layout = json.loads(o_stream.getvalue())
            self.assertTrue(isinstance(cart_layout, list))
            self.assertEqual(5, len(cart_layout))
            print(cart_layout)
            for entry in cart_layout:
                self.assertTrue('node' in entry)
                self.assertTrue('x' in entry)
                self.assertTrue('y' in entry)
                self.assertTrue(0.0 <= entry['x'] <= 1.1)
                self.assertTrue(0.0 <= entry['y'] <= 1.1)
                self.assertTrue(entry['node'] in [175, 180, 185, 190, 195])
        finally:
            shutil.rmtree(temp_dir)


if __name__ == '__main__':
    sys.exit(unittest.main())
