#!/usr/bin/python

import unittest
from cStringIO import StringIO


src = """
"string"
420
6.66
"""

import sys
sys.path.append('plex')

from Plex import *
import eris

class LexTest(unittest.TestCase):
    def setUp(self):
        self.lexicon = eris.create_lexicon()

    def mk_scanner(self, source):
        f = StringIO(source)
        return Scanner(self.lexicon, f, 'test')

class TestNumber(LexTest):
    def test_digit(self):
        src = "4"
        s = self.mk_scanner(src)
        self.assertEqual(list(s.tokens()), [('int', '4')])

    def test_number(self):
        src = "44"
        s = self.mk_scanner(src)
        self.assertEqual(list(s.tokens()), [('int', '44')])

    def test_float(self):
        src = "42.666"
        s = self.mk_scanner(src)
        self.assertEqual(list(s.tokens()), [('float', '42.666')])

class TestComment(LexTest):
    def test_comment(self):
        src = "foo"
