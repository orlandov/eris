#!python

from Plex import *

def ErisScanner(Scanner):
    pass

def create_lexicon():
    letter = Range("AZaz")
    digit = Range("09")
    string = Str('"') + Rep(AnyBut('"')) + Str('"')
    name = letter + Rep(letter | digit)
    number = Rep1(digit)
    float = Rep1(number) + Str('.') + Rep1(number)
    space = Any(" \t\n")
    comment = Str("#") + Rep(AnyBut("\n"))

    resword = Str("if", "then", "else", "end")

    lex = Lexicon([
        (comment,         'comment'),
        (name,            'ident'),
        (number,          'int'),
        (float,           'float'),
        (resword,         TEXT),
        (Any("+-*/=<>"),  TEXT),
        (space | comment, IGNORE)
    ])

    return lex
