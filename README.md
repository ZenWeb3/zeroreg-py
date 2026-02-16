<p align="center">
  <img src="https://em-content.zobj.net/source/apple/391/crying-face_1f622.png" width="80" />
</p>

<h1 align="center">zeroReg</h1>

<p align="center">
  <strong>Regex was a mistake. Just like your ex.</strong>
</p>

<p align="center">
  Write regex without the tears or confusion.<br/>
  A human-readable regex builder for Python.
</p>

<p align="center">
  <a href="https://pypi.org/project/zeroreg/"><img src="https://img.shields.io/pypi/v/zeroreg?style=flat-square&color=000&labelColor=000" alt="PyPI version" /></a>
  <a href="https://pypi.org/project/zeroreg/"><img src="https://img.shields.io/pypi/dm/zeroreg?style=flat-square&color=000&labelColor=000" alt="PyPI downloads" /></a>
  <a href="https://github.com/zenweb3/zeroreg-py/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-000?style=flat-square&labelColor=000" alt="license" /></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/pypi/pyversions/zeroreg?style=flat-square&color=000&labelColor=000" alt="python versions" /></a>
</p>

---

## The Problem

```python
import re
pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
```

Your coworker asks what it does. You mass tears. You mass confusion. You mass quit.

## The Solution

```python
from zeroreg.patterns import email

email.test('hello@world.com')  # True
```

Or build your own:

```python
from zeroreg import digit, optional

phone = (
    optional('+')
    .then(digit(3))
    .then('-')
    .then(digit(3))
    .then('-')
    .then(digit(4))
)

phone.test('123-456-7890')   # True
phone.test('+123-456-7890')  # True
phone.to_regex()             # re.compile(r'\+?\d{3}-\d{3}-\d{4}')
```

## Installation

```bash
pip install zeroreg
```

## API

### Character Classes

| Function | Description | Regex |
|----------|-------------|-------|
| `digit(n?)` | Match digits | `\d` or `\d{n}` |
| `word()` | Word characters | `\w` |
| `letter()` | Letters only | `[a-zA-Z]` |
| `whitespace()` | Whitespace | `\s` |
| `any_char()` | Any character | `.` |
| `literal(str)` | Exact match | (escaped) |
| `char_in(chars)` | Match any in set | `[...]` |
| `char_not_in(chars)` | Match any NOT in set | `[^...]` |

### Quantifiers

| Method | Description |
|--------|-------------|
| `.one_or_more()` | 1+ times |
| `.zero_or_more()` | 0+ times |
| `.optional()` | 0 or 1 |
| `.times(n)` | Exactly n |
| `.between(min, max)` | Range |
| `.at_least(n)` | n or more |

### Groups

| Function | Description |
|----------|-------------|
| `capture(pattern, name?)` | Capturing group |
| `group(pattern)` | Non-capturing group |
| `one_of(*patterns)` | Match any of |

### Anchors

| Function | Description |
|----------|-------------|
| `start_of_line()` | `^` |
| `end_of_line()` | `$` |
| `word_boundary()` | `\b` |

### Output

| Method | Description |
|--------|-------------|
| `.to_regex(flags?)` | Get compiled `re.Pattern` |
| `.test(str)` | Test string |
| `.match(str)` | Get match object |
| `.match_all(str)` | Get all matches |
| `.replace(str, replacement)` | Replace matches |

## Pre-built Patterns

```python
from zeroreg.patterns import email, url, phone, date, ipv4, uuid
```

Available: `email`, `url`, `phone`, `date`, `time`, `ipv4`, `ipv6`, `hex_color`, `hex_string`, `uuid`, `slug`, `hashtag`, `mention`, `credit_card`, `ssn`, `zip_code`, `username`, `strong_password`, `semver`, `mac_address`

## Real World Examples

### Extract Date Parts

```python
from zeroreg import digit, capture

date_pattern = (
    capture(digit(4), 'year')
    .then('-')
    .then(capture(digit(2), 'month'))
    .then('-')
    .then(capture(digit(2), 'day'))
)

match = date_pattern.match('2024-03-15')
print(match.group('year'))   # '2024'
print(match.group('month'))  # '03'
print(match.group('day'))    # '15'
```

### Password Validation

```python
from zeroreg import start_of_line, end_of_line, any_char, digit, letter, lookahead, char_in

password = (
    start_of_line()
    .then(lookahead(any_char().zero_or_more().then(digit())))
    .then(lookahead(any_char().zero_or_more().then(letter())))
    .then(lookahead(any_char().zero_or_more().then(char_in('@$!%*?&'))))
    .then(any_char().between(8, 32))
    .then(end_of_line())
)

password.test('MyP@ssw0rd')  # True
password.test('weak')        # False
```

## Also Available

- **JavaScript/TypeScript**: `npm install zeroreg`

## License

MIT