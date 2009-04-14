#!/usr/bin/python

import unittest
from cStringIO import StringIO
import sys
sys.path.append('../plex/lib')

import eris

class LexTest(object):
    def mk_scanner(self, source):
        return eris.Scanner(source)

    def assertScan(self, src, exp_tokens):
        s = self.mk_scanner(src)
        tokens = list(s.tokens())
        self.assertEqual(tokens, exp_tokens)

    def assertScanFails(self, src, e):
        s = self.mk_scanner(src)
        self.assertRaises(e, list, s.tokens())


class TestNumber(unittest.TestCase, LexTest):
    def test_digit(self):
        src = "4"
        self.assertScan(src, [('number', '4')])

    def test_number(self):
        src = "44"
        self.assertScan(src, [('number', '44')])

    def test_float(self):
        src = "42.666"
        self.assertScan(src, [('number', '42.666')])


class TestEmpty(unittest.TestCase, LexTest):
    def assertEmpty(self, l):
        self.assertEqual(l, [])

    def test_empty(self):
        src = ""
        s = self.mk_scanner(src)
        self.assertEmpty(list(s.tokens()))

    def test_blanklines(self):
        src = "\n\n\n"
        s = self.mk_scanner(src)
        self.assertEmpty(list(s.tokens()))


class TestComment(unittest.TestCase, LexTest):
    def test_comment(self):
        src = "# foo\n4"
        self.assertScan(src, [('number', '4')])

    def test_comment(self):
        src = "42 # comment"
        self.assertScan(src, [('number', '42')])


class TestString(unittest.TestCase, LexTest):
    def test_string(self):
        src = '"master shake"'
        self.assertScan(src, [('string', '"master shake"')])


class TestMultiple(unittest.TestCase, LexTest):
    def test_multiple(self):
        src = "42\n'call me'"
        self.assertScan(src, [
            ('number', "42"),
            ('string', "'call me'")
        ])

    def test_name(self):
        src = "foo"
        self.assertScan(src, [('identifier', 'foo')])


class TestPunctuation(unittest.TestCase, LexTest):
    def test_punct(self):
        src = "42 + 420"
        self.assertScan(src, [
            ('number', '42'),
            ('+', '+'),
            ('number', '420')
        ])


class TestIf(unittest.TestCase, LexTest):
    def test_if(self):
        src = """
            if (10) {
                statement    
            }
        """

        self.assertScan(src, [
            ('reserved', 'if'),
            ('(', '('),
            ('number', '10'),
            (')', ')'),
            ('{', '{'),
            ('identifier', 'statement'),
            ('}', '}'),
        ])


class TestParenthesis(unittest.TestCase, LexTest):
    def test_parenthesis(self):
        src = "(1 + 2)"
        self.assertScan(src, [
            ('(', '('),
            ('number', '1'),
            ('+', '+'),
            ('number', '2'),
            (')', ')'),
        ])

    def test_balanced(self):
        src = ")"
        self.assertScanFails(src, eris.ScannerError)
        src = "(1 + 2))"
        self.assertScanFails(src, eris.ScannerError)
        src = ")"
        self.assertScanFails(src, eris.ScannerError)



class TestFunction(unittest.TestCase, LexTest):
    def test_function(self):
        src = """
            a = function (foo, bar, baz) {
                statement1
                statement2
            }
        """
        self.assertScan(src, [
            ('identifier', 'a'),
            ('=', '='),
            ('identifier', 'function'),
            ('(', '('),
            ('identifier', 'foo'),
            (',', ','),
            ('identifier', 'bar'),
            (',', ','),
            ('identifier', 'baz'),
            (')', ')'),
            ('{', '{'),
            ('identifier', 'statement1',),
            ('identifier', 'statement2',),
            ('}', '}'),
        ])
