#!python

from Plex import Str, Rep, Rep1, Range, Any, AnyBut, AnyChar, Opt, TEXT, IGNORE
import Plex

from StringIO import StringIO

class ScannerError(Exception):
    pass

class Scanner(Plex.Scanner):
    def open_bracket_action(self, text):
        self.bracket_nesting_level[text] += 1
        return text

    def close_bracket_action(self, text):
        bracket_dict = {
            ')': '(',
            '}': '{',
            ']': '[',
        }

        opening = bracket_dict[text]
        self.bracket_nesting_level[opening] -= 1
        if self.bracket_nesting_level[opening] < 0:
            raise ScannerError("Unbalanced parenthesis!")
        return text

    letter = Range("AZaz") | Any("_")
    digit = Range("09")
    hexdigit = Range("09AFaf")

    identifier = letter + Rep(letter | digit)
    number = Rep1(digit) | (Str("0x") + Rep1(hexdigit)) | \
        (Rep1(digit) + Str('.') + Rep1(digit))
    
    sq_string = (
        Str("'") + 
        Rep(AnyBut("\\\n'") | (Str("\\") + AnyChar)) + 
        Str("'"))
        
    dq_string = (
        Str('"') + 
        Rep(AnyBut('\\\n"') | (Str("\\") + AnyChar)) + 
        Str('"'))
            
    stringlit = sq_string | dq_string
    open_bracket = Any("([{")
    close_bracket = Any(")]}")

    punct1 = Any(":,;+-*/|&<>=.%`~^")
    punct2 = Str("==", "<>", "!=", "<=", "<<", ">>", "**")
    punctuation = punct1 | punct2

    spaces = Rep1(Any(" \t"))
    empty_line = Rep(spaces) + Str("\n")
    indentation = Rep(Str(" ")) | Rep(Str("\t"))
    escaped_newline = Str("\\\n")
    comment = Str("#") + Rep(AnyBut("\n"))
    blank_line = indentation + Opt(comment)
    reserved = Str('if')

    lexicon = Plex.Lexicon([
        (reserved,        'reserved'),
        (identifier,      'identifier'),
        (number,          'number'),
        (stringlit,       'string'),
        (punctuation,     TEXT),
        (open_bracket, open_bracket_action),
        (close_bracket, close_bracket_action),
        (comment,         IGNORE),
        (spaces,          IGNORE),
        (empty_line,      IGNORE),
        (escaped_newline, IGNORE),
    ])

    def __init__(self, source):
        Plex.Scanner.__init__(self, self.lexicon, StringIO(source))

        self.bracket_nesting_level = {
            '(': 0,
            '{': 0,
            '[': 0
        }
