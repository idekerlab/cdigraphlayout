#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_cddiffusion
----------------------------------

Tests for `cddiffusion` module.
"""

import os
import sys
import unittest
import tempfile
import shutil
import io
import stat
from unittest.mock import MagicMock
from cddiffusion import cddiffusioncmd


class TestCdDiffusion(unittest.TestCase):

    TEST_DIR = os.path.dirname(__file__)

    HUNDRED_NODE_DIR = os.path.join(TEST_DIR, 'data',
                                    '100node_example')

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_parse_args_all_defaults(self):
        myargs = ['inputarg']
        res = cddiffusioncmd._parse_arguments('desc', myargs)
        self.assertEqual('inputarg', res.input)


if __name__ == '__main__':
    sys.exit(unittest.main())
