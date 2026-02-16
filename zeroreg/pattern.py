from __future__ import annotations

import re
from typing import List, Match, Optional, Pattern as RePattern, Union


class Pattern:
    """
    A chainable regex pattern builder.
    
    Example:
        >>> from zeroreg import digit, literal
        >>> pattern = digit(3).then('-').then(digit(4))
        >>> pattern.test('123-4567')
        True
        >>> pattern.to_regex()
        re.compile(r'\\d{3}-\\d{4}')
    """

    def __init__(self, source: str) -> None:
        self._source = source

    @property
    def source(self) -> str:
        """Get the raw regex pattern string."""
        return self._source

    def then(self, pattern: Union[Pattern, str]) -> Pattern:
        """Chain another pattern or string."""
        if isinstance(pattern, str):
            next_source = escape_regex(pattern)
        else:
            next_source = pattern.source
        return Pattern(self._source + next_source)

    def one_or_more(self) -> Pattern:
        """Match one or more times (+)."""
        return Pattern(self._wrap() + "+")

    def zero_or_more(self) -> Pattern:
        """Match zero or more times (*)."""
        return Pattern(self._wrap() + "*")

    def optional(self) -> Pattern:
        """Make pattern optional (?)."""
        return Pattern(self._wrap() + "?")

    def times(self, n: int) -> Pattern:
        """Match exactly n times."""
        return Pattern(self._wrap() + f"{{{n}}}")

    def between(self, min_count: int, max_count: int) -> Pattern:
        """Match between min and max times."""
        return Pattern(self._wrap() + f"{{{min_count},{max_count}}}")

    def at_least(self, n: int) -> Pattern:
        """Match at least n times."""
        return Pattern(self._wrap() + f"{{{n},}}")

    def at_most(self, n: int) -> Pattern:
        """Match at most n times."""
        return Pattern(self._wrap() + f"{{0,{n}}}")

    def or_(self, pattern: Union[Pattern, str]) -> Pattern:
        """Add OR logic with another pattern."""
        if isinstance(pattern, str):
            alt = escape_regex(pattern)
        else:
            alt = pattern.source
        return Pattern(f"(?:{self._source}|{alt})")

    def to_regex(self, flags: int = 0) -> RePattern[str]:
        """Convert to native re.Pattern (compiled regex)."""
        return re.compile(self._source, flags)

    def test(self, input_str: str) -> bool:
        """Test if string matches the pattern."""
        return bool(self.to_regex().search(input_str))

    def match(self, input_str: str) -> Optional[Match[str]]:
        """Match string and return Match object or None."""
        return self.to_regex().search(input_str)

    def match_all(self, input_str: str) -> List[str]:
        """Find all matches in string."""
        return self.to_regex().findall(input_str)

    def replace(self, input_str: str, replacement: str) -> str:
        """Replace all matches in string."""
        return self.to_regex().sub(replacement, input_str)

    def __str__(self) -> str:
        """Get pattern as string."""
        return self._source

    def __repr__(self) -> str:
        return f"Pattern({self._source!r})"

    def _wrap(self) -> str:
        """Wrap pattern in non-capturing group if needed."""
        if len(self._source) == 1 or self._is_wrapped():
            return self._source
        return f"(?:{self._source})"

    def _is_wrapped(self) -> bool:
        """Check if pattern is already wrapped or is a character class."""
        return (
            (self._source.startswith("(?:") and self._source.endswith(")"))
            or (self._source.startswith("(") and self._source.endswith(")"))
            or (self._source.startswith("[") and self._source.endswith("]"))
            or self._source.startswith("\\")
        )


def escape_regex(string: str) -> str:
    """Escape special regex characters in a string."""
    return re.escape(string)


def raw(source: str) -> Pattern:
    """Create a pattern from a raw regex string (no escaping)."""
    return Pattern(source)