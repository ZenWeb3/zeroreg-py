
from __future__ import annotations

from typing import Union

from .pattern import Pattern, escape_regex, raw



# CHARACTER CLASSES



def digit(count: int | None = None) -> Pattern:
    """
    Match any digit (0-9).
    
    Args:
        count: Optional exact count of digits to match.
    
    Example:
        >>> digit().test('5')
        True
        >>> digit(3).test('123')
        True
    """
    if count is not None:
        return Pattern(f"\\d{{{count}}}")
    return Pattern(r"\d")


def non_digit() -> Pattern:
    """Match any non-digit character."""
    return Pattern(r"\D")


def word() -> Pattern:
    """Match any word character (a-z, A-Z, 0-9, _)."""
    return Pattern(r"\w")


def non_word() -> Pattern:
    """Match any non-word character."""
    return Pattern(r"\W")


def whitespace() -> Pattern:
    """Match any whitespace character."""
    return Pattern(r"\s")


def non_whitespace() -> Pattern:
    """Match any non-whitespace character."""
    return Pattern(r"\S")


def letter() -> Pattern:
    """Match any letter (a-z, A-Z)."""
    return Pattern("[a-zA-Z]")


def lowercase() -> Pattern:
    """Match lowercase letters only."""
    return Pattern("[a-z]")


def uppercase() -> Pattern:
    """Match uppercase letters only."""
    return Pattern("[A-Z]")


def alphanumeric() -> Pattern:
    """Match alphanumeric characters (a-z, A-Z, 0-9)."""
    return Pattern("[a-zA-Z0-9]")


def any_char() -> Pattern:
    """Match any character (except newline by default)."""
    return Pattern(".")


def literal(string: str) -> Pattern:
    """
    Match a specific character or string (escaped).
    
    Example:
        >>> literal('.').test('.')
        True
        >>> literal('.').test('a')
        False
    """
    return Pattern(escape_regex(string))


def char_in(chars: str) -> Pattern:
    """
    Match any character in the set.
    
    Example:
        >>> char_in('aeiou').test('e')
        True
    """
    escaped = chars.replace("]", "\\]").replace("\\", "\\\\").replace("^", "\\^").replace("-", "\\-")
    return Pattern(f"[{escaped}]")


def char_not_in(chars: str) -> Pattern:
    """
    Match any character NOT in the set.
    
    Example:
        >>> char_not_in('aeiou').test('b')
        True
    """
    escaped = chars.replace("]", "\\]").replace("\\", "\\\\").replace("^", "\\^").replace("-", "\\-")
    return Pattern(f"[^{escaped}]")


def range_of(start: str, end: str) -> Pattern:
    """
    Match a range of characters.
    
    Example:
        >>> range_of('a', 'z').test('m')
        True
    """
    return Pattern(f"[{start}-{end}]")



# QUANTIFIERS (standalone)



def optional(pattern: Union[Pattern, str]) -> Pattern:
    """
    Make a pattern optional.
    
    Example:
        >>> optional('+').then(digit(3)).test('123')
        True
        >>> optional('+').then(digit(3)).test('+123')
        True
    """
    if isinstance(pattern, str):
        return Pattern(f"(?:{escape_regex(pattern)})?")
    return pattern.optional()


def one_or_more(pattern: Union[Pattern, str]) -> Pattern:
    """Match one or more of a pattern."""
    if isinstance(pattern, str):
        return Pattern(f"(?:{escape_regex(pattern)})+")
    return pattern.one_or_more()


def zero_or_more(pattern: Union[Pattern, str]) -> Pattern:
    """Match zero or more of a pattern."""
    if isinstance(pattern, str):
        return Pattern(f"(?:{escape_regex(pattern)})*")
    return pattern.zero_or_more()



# GROUPS


def capture(pattern: Union[Pattern, str], name: str | None = None) -> Pattern:
    """
    Create a capturing group.
    
    Args:
        pattern: Pattern to capture.
        name: Optional name for named capture group.
    
    Example:
        >>> p = capture(digit(4), 'year').then('-').then(capture(digit(2), 'month'))
        >>> m = p.match('2024-03')
        >>> m.group('year')
        '2024'
    """
    src = escape_regex(pattern) if isinstance(pattern, str) else pattern.source
    if name:
        return Pattern(f"(?P<{name}>{src})")
    return Pattern(f"({src})")


def group(pattern: Union[Pattern, str]) -> Pattern:
    """
    Create a non-capturing group.
    
    Example:
        >>> group(literal('ab').or_('cd')).one_or_more().test('abcdab')
        True
    """
    src = escape_regex(pattern) if isinstance(pattern, str) else pattern.source
    return Pattern(f"(?:{src})")


def one_of(*patterns: Union[Pattern, str]) -> Pattern:
    """
    Match any of the provided patterns.
    
    Example:
        >>> one_of('cat', 'dog', 'bird').test('dog')
        True
    """
    sources = [escape_regex(p) if isinstance(p, str) else p.source for p in patterns]
    return Pattern(f"(?:{'|'.join(sources)})")



# ANCHORS


def start_of_line() -> Pattern:
    """Match start of string/line."""
    return Pattern("^")


def end_of_line() -> Pattern:
    """Match end of string/line."""
    return Pattern("$")


def word_boundary() -> Pattern:
    """Match word boundary."""
    return Pattern(r"\b")


def non_word_boundary() -> Pattern:
    """Match non-word boundary."""
    return Pattern(r"\B")


# =============================================================================
# LOOKAHEAD / LOOKBEHIND
# =============================================================================


def lookahead(pattern: Union[Pattern, str]) -> Pattern:
    """
    Positive lookahead - match if followed by pattern.
    
    Example:
        >>> digit().one_or_more().then(lookahead(literal('px'))).test('100px')
        True
    """
    src = escape_regex(pattern) if isinstance(pattern, str) else pattern.source
    return Pattern(f"(?={src})")


def negative_lookahead(pattern: Union[Pattern, str]) -> Pattern:
    """Negative lookahead - match if NOT followed by pattern."""
    src = escape_regex(pattern) if isinstance(pattern, str) else pattern.source
    return Pattern(f"(?!{src})")


def lookbehind(pattern: Union[Pattern, str]) -> Pattern:
    """Positive lookbehind - match if preceded by pattern."""
    src = escape_regex(pattern) if isinstance(pattern, str) else pattern.source
    return Pattern(f"(?<={src})")


def negative_lookbehind(pattern: Union[Pattern, str]) -> Pattern:
    """Negative lookbehind - match if NOT preceded by pattern."""
    src = escape_regex(pattern) if isinstance(pattern, str) else pattern.source
    return Pattern(f"(?<!{src})")


# SPECIAL


def newline() -> Pattern:
    """Match a newline."""
    return Pattern(r"\n")


def tab() -> Pattern:
    """Match a tab."""
    return Pattern(r"\t")


def carriage_return() -> Pattern:
    """Match a carriage return."""
    return Pattern(r"\r")


# Re-export raw
__all__ = [
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
    # Core
    "raw",
]