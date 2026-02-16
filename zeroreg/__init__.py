"""
zeroreg - A human-readable regex builder for Python.

Regex was a mistake. Just like your ex.

Example:
    >>> from zeroreg import digit, optional
    >>> phone = optional('+').then(digit(3)).then('-').then(digit(3)).then('-').then(digit(4))
    >>> phone.test('123-456-7890')
    True
    >>> phone.to_regex()
    re.compile(r'\\+?\\d{3}-\\d{3}-\\d{4}')

    >>> from zeroreg.patterns import email
    >>> email.test('hello@world.com')
    True
"""

from .pattern import Pattern, escape_regex, raw
from .builders import (
    # Character classes
    digit,
    non_digit,
    word,
    non_word,
    whitespace,
    non_whitespace,
    letter,
    lowercase,
    uppercase,
    alphanumeric,
    any_char,
    literal,
    char_in,
    char_not_in,
    range_of,
    # Quantifiers
    optional,
    one_or_more,
    zero_or_more,
    # Groups
    capture,
    group,
    one_of,
    # Anchors
    start_of_line,
    end_of_line,
    word_boundary,
    non_word_boundary,
    # Lookahead/Lookbehind
    lookahead,
    negative_lookahead,
    lookbehind,
    negative_lookbehind,
    # Special
    newline,
    tab,
    carriage_return,
)

__version__ = "0.1.0"
__all__ = [
    # Core
    "Pattern",
    "escape_regex",
    "raw",
    # Character classes
    "digit",
    "non_digit",
    "word",
    "non_word",
    "whitespace",
    "non_whitespace",
    "letter",
    "lowercase",
    "uppercase",
    "alphanumeric",
    "any_char",
    "literal",
    "char_in",
    "char_not_in",
    "range_of",
    # Quantifiers
    "optional",
    "one_or_more",
    "zero_or_more",
    # Groups
    "capture",
    "group",
    "one_of",
    # Anchors
    "start_of_line",
    "end_of_line",
    "word_boundary",
    "non_word_boundary",
    # Lookahead/Lookbehind
    "lookahead",
    "negative_lookahead",
    "lookbehind",
    "negative_lookbehind",
    # Special
    "newline",
    "tab",
    "carriage_return",
]