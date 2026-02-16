"""Tests for zeroReg."""

import pytest
from zeroreg import (
    digit,
    non_digit,
    word,
    non_word,
    letter,
    lowercase,
    uppercase,
    alphanumeric,
    literal,
    optional,
    one_or_more,
    zero_or_more,
    capture,
    group,
    one_of,
    start_of_line,
    end_of_line,
    word_boundary,
    char_in,
    char_not_in,
    range_of,
    whitespace,
    non_whitespace,
    any_char,
    lookahead,
    negative_lookahead,
    lookbehind,
    negative_lookbehind,
    newline,
    tab,
    raw,
)
from zeroreg.patterns import (
    email,
    url,
    phone,
    date,
    time,
    ipv4,
    ipv6,
    uuid,
    hex_color,
    hex_string,
    slug,
    hashtag,
    mention,
    credit_card,
    ssn,
    zip_code,
    username,
    strong_password,
    semver,
    mac_address,
)


# =============================================================================
# CHARACTER CLASSES
# =============================================================================


class TestDigit:
    def test_matches_single_digit(self):
        assert digit().test("5") is True
        assert digit().test("a") is False

    def test_matches_exact_count(self):
        pattern = start_of_line().then(digit(3)).then(end_of_line())
        assert pattern.test("123") is True
        assert pattern.test("12") is False
        assert pattern.test("1234") is False

    def test_chains_with_one_or_more(self):
        assert digit().one_or_more().test("123") is True
        assert digit().one_or_more().test("") is False


class TestNonDigit:
    def test_matches_non_digit(self):
        assert non_digit().test("a") is True
        assert non_digit().test("5") is False


class TestWord:
    def test_matches_word_chars(self):
        assert word().test("a") is True
        assert word().test("Z") is True
        assert word().test("5") is True
        assert word().test("_") is True
        assert word().test("@") is False


class TestNonWord:
    def test_matches_non_word_chars(self):
        assert non_word().test("@") is True
        assert non_word().test("a") is False


class TestLetter:
    def test_matches_letters(self):
        assert letter().test("a") is True
        assert letter().test("Z") is True
        assert letter().test("5") is False


class TestLowercase:
    def test_matches_lowercase(self):
        assert lowercase().test("a") is True
        assert lowercase().test("A") is False


class TestUppercase:
    def test_matches_uppercase(self):
        assert uppercase().test("A") is True
        assert uppercase().test("a") is False


class TestAlphanumeric:
    def test_matches_alphanumeric(self):
        assert alphanumeric().test("a") is True
        assert alphanumeric().test("5") is True
        assert alphanumeric().test("_") is False


class TestWhitespace:
    def test_matches_whitespace(self):
        assert whitespace().test(" ") is True
        assert whitespace().test("\t") is True
        assert whitespace().test("a") is False


class TestNonWhitespace:
    def test_matches_non_whitespace(self):
        assert non_whitespace().test("a") is True
        assert non_whitespace().test(" ") is False


class TestAnyChar:
    def test_matches_any_char(self):
        assert any_char().test("a") is True
        assert any_char().test("5") is True
        assert any_char().test("@") is True


class TestLiteral:
    def test_matches_exact_string(self):
        assert literal("hello").test("hello") is True
        assert literal("hello").test("world") is False

    def test_escapes_special_chars(self):
        assert literal(".").test(".") is True
        assert literal(".").test("a") is False
        assert literal("$100").test("$100") is True


class TestCharIn:
    def test_matches_chars_in_set(self):
        vowels = char_in("aeiou")
        assert vowels.test("a") is True
        assert vowels.test("b") is False


class TestCharNotIn:
    def test_matches_chars_not_in_set(self):
        not_vowels = char_not_in("aeiou")
        assert not_vowels.test("b") is True
        assert not_vowels.test("a") is False


class TestRangeOf:
    def test_matches_range(self):
        digit_range = range_of("0", "9")
        assert digit_range.test("5") is True
        assert digit_range.test("a") is False


# =============================================================================
# CHAINING
# =============================================================================


class TestChaining:
    def test_chains_with_then(self):
        pattern = digit(3).then("-").then(digit(4))
        assert pattern.test("123-4567") is True
        assert pattern.test("12-4567") is False

    def test_one_or_more(self):
        pattern = digit().one_or_more()
        assert pattern.test("1") is True
        assert pattern.test("123") is True
        assert pattern.test("") is False

    def test_zero_or_more(self):
        pattern = digit().zero_or_more()
        assert pattern.test("") is True
        assert pattern.test("123") is True

    def test_optional(self):
        pattern = literal("+").optional().then(digit(3))
        assert pattern.test("123") is True
        assert pattern.test("+123") is True

    def test_times(self):
        pattern = letter().times(3)
        assert pattern.test("abc") is True
        assert pattern.test("ab") is False

    def test_between(self):
        pattern = start_of_line().then(digit().between(2, 4)).then(end_of_line())
        assert pattern.test("12") is True
        assert pattern.test("1234") is True
        assert pattern.test("1") is False
        assert pattern.test("12345") is False

    def test_at_least(self):
        pattern = digit().at_least(3)
        assert pattern.test("123") is True
        assert pattern.test("12345") is True
        assert pattern.test("12") is False

    def test_at_most(self):
        pattern = start_of_line().then(digit().at_most(3)).then(end_of_line())
        assert pattern.test("") is True
        assert pattern.test("123") is True
        assert pattern.test("1234") is False

    def test_or(self):
        pattern = literal("cat").or_("dog")
        assert pattern.test("cat") is True
        assert pattern.test("dog") is True
        assert pattern.test("bird") is False


# =============================================================================
# STANDALONE QUANTIFIERS
# =============================================================================


class TestStandaloneQuantifiers:
    def test_optional_with_pattern(self):
        pattern = optional(digit()).then(letter())
        assert pattern.test("a") is True
        assert pattern.test("5a") is True

    def test_optional_with_string(self):
        pattern = optional("+").then(digit(3))
        assert pattern.test("123") is True
        assert pattern.test("+123") is True

    def test_one_or_more_with_pattern(self):
        pattern = one_or_more(digit())
        assert pattern.test("123") is True
        assert pattern.test("") is False

    def test_zero_or_more_with_pattern(self):
        pattern = zero_or_more(digit())
        assert pattern.test("123") is True
        assert pattern.test("") is True


# =============================================================================
# GROUPS
# =============================================================================


class TestCapture:
    def test_creates_capturing_groups(self):
        pattern = capture(digit(3)).then("-").then(capture(digit(4)))
        match = pattern.match("123-4567")
        assert match is not None
        assert match.group(1) == "123"
        assert match.group(2) == "4567"

    def test_creates_named_groups(self):
        pattern = capture(digit(4), "year").then("-").then(capture(digit(2), "month"))
        match = pattern.match("2024-03")
        assert match is not None
        assert match.group("year") == "2024"
        assert match.group("month") == "03"


class TestGroup:
    def test_creates_non_capturing_groups(self):
        pattern = group(literal("ab").or_("cd")).one_or_more()
        assert pattern.test("ab") is True
        assert pattern.test("abcd") is True


class TestOneOf:
    def test_matches_any_pattern(self):
        pattern = one_of("cat", "dog", "bird")
        assert pattern.test("cat") is True
        assert pattern.test("dog") is True
        assert pattern.test("fish") is False


# =============================================================================
# ANCHORS
# =============================================================================


class TestAnchors:
    def test_start_of_line(self):
        pattern = start_of_line().then(literal("hello"))
        assert pattern.test("hello world") is True
        assert pattern.test("say hello") is False

    def test_end_of_line(self):
        pattern = literal("world").then(end_of_line())
        assert pattern.test("hello world") is True
        assert pattern.test("world hello") is False

    def test_word_boundary(self):
        pattern = word_boundary().then(literal("cat")).then(word_boundary())
        regex = pattern.to_regex()
        assert regex.search("the cat sat") is not None
        assert regex.search("category") is None


# =============================================================================
# LOOKAHEAD / LOOKBEHIND
# =============================================================================


class TestLookahead:
    def test_positive_lookahead(self):
        pattern = digit().one_or_more().then(lookahead(literal("px")))
        assert pattern.test("100px") is True
        assert pattern.test("100em") is False

    def test_negative_lookahead(self):
        pattern = digit().one_or_more().then(negative_lookahead(literal("px")))
        assert pattern.test("100em") is True
        assert pattern.test("100") is True


class TestLookbehind:
    def test_positive_lookbehind(self):
        pattern = lookbehind(literal("$")).then(digit().one_or_more())
        match = pattern.match("$100")
        assert match is not None
        assert match.group(0) == "100"

    def test_negative_lookbehind(self):
        pattern = negative_lookbehind(literal("$")).then(digit().one_or_more())
        regex = pattern.to_regex()
        assert regex.search("€100") is not None


# =============================================================================
# SPECIAL CHARACTERS
# =============================================================================


class TestSpecialChars:
    def test_newline(self):
        assert newline().test("\n") is True
        assert newline().test("n") is False

    def test_tab(self):
        assert tab().test("\t") is True
        assert tab().test("t") is False


# =============================================================================
# RAW
# =============================================================================


class TestRaw:
    def test_creates_raw_pattern(self):
        pattern = raw("[A-Z]{2,3}")
        assert pattern.test("AB") is True
        assert pattern.test("ABC") is True
        assert pattern.test("ab") is False


# =============================================================================
# OUTPUT METHODS
# =============================================================================


class TestOutputMethods:
    def test_to_regex(self):
        pattern = digit(3)
        regex = pattern.to_regex()
        assert regex.pattern == r"\d{3}"

    def test_test(self):
        pattern = digit(3)
        assert pattern.test("123") is True
        assert pattern.test("abc") is False

    def test_match(self):
        pattern = digit().one_or_more()
        match = pattern.match("abc123def")
        assert match is not None
        assert match.group(0) == "123"

    def test_match_all(self):
        pattern = digit().one_or_more()
        matches = pattern.match_all("abc 123 def 456")
        assert matches == ["123", "456"]

    def test_replace(self):
        pattern = digit().one_or_more()
        result = pattern.replace("abc 123 def 456", "X")
        assert result == "abc X def X"

    def test_str(self):
        pattern = digit(3).then("-").then(digit(4))
        assert str(pattern) == r"\d{3}\-\d{4}"


# =============================================================================
# PRE-BUILT PATTERNS
# =============================================================================


class TestPatternEmail:
    def test_matches_valid_emails(self):
        assert email.test("test@example.com") is True
        assert email.test("user.name+tag@domain.co.uk") is True

    def test_rejects_invalid_emails(self):
        assert email.test("invalid") is False
        assert email.test("@domain.com") is False


class TestPatternUrl:
    def test_matches_valid_urls(self):
        assert url.test("https://example.com") is True
        assert url.test("http://sub.domain.com/path?query=1") is True

    def test_rejects_invalid_urls(self):
        assert url.test("not a url") is False
        assert url.test("ftp://example.com") is False


class TestPatternPhone:
    def test_matches_phone_numbers(self):
        assert phone.test("123-456-7890") is True
        assert phone.test("+1-234-567-8900") is True


class TestPatternDate:
    def test_matches_iso_dates(self):
        assert date.test("2024-03-15") is True
        assert date.test("2024-12-01") is True

    def test_rejects_invalid_dates(self):
        assert date.test("2024-13-01") is False
        assert date.test("2024/03/15") is False


class TestPatternTime:
    def test_matches_valid_times(self):
        assert time.test("14:30") is True
        assert time.test("23:59:59") is True

    def test_rejects_invalid_times(self):
        assert time.test("25:00") is False


class TestPatternIpv4:
    def test_matches_valid_ipv4(self):
        assert ipv4.test("192.168.1.1") is True
        assert ipv4.test("10.0.0.255") is True

    def test_rejects_invalid_ipv4(self):
        assert ipv4.test("256.168.1.1") is False


class TestPatternIpv6:
    def test_matches_valid_ipv6(self):
        assert ipv6.test("2001:0db8:85a3:0000:0000:8a2e:0370:7334") is True


class TestPatternUuid:
    def test_matches_valid_uuids(self):
        assert uuid.test("550e8400-e29b-41d4-a716-446655440000") is True

    def test_rejects_invalid_uuids(self):
        assert uuid.test("not-a-uuid") is False


class TestPatternHexColor:
    def test_matches_hex_colors(self):
        assert hex_color.test("#fff") is True
        assert hex_color.test("#ffffff") is True

    def test_rejects_invalid_hex_colors(self):
        assert hex_color.test("fff") is False


class TestPatternSlug:
    def test_matches_valid_slugs(self):
        assert slug.test("my-awesome-post") is True
        assert slug.test("hello-world-123") is True

    def test_rejects_invalid_slugs(self):
        assert slug.test("Has Spaces") is False


class TestPatternHashtag:
    def test_matches_hashtags(self):
        assert hashtag.test("#hello") is True


class TestPatternMention:
    def test_matches_mentions(self):
        assert mention.test("@username") is True


class TestPatternCreditCard:
    def test_matches_credit_cards(self):
        assert credit_card.test("4111111111111111") is True


class TestPatternSsn:
    def test_matches_ssn(self):
        assert ssn.test("123-45-6789") is True

    def test_rejects_invalid_ssn(self):
        assert ssn.test("123456789") is False


class TestPatternZipCode:
    def test_matches_zip_codes(self):
        assert zip_code.test("12345") is True
        assert zip_code.test("12345-6789") is True


class TestPatternUsername:
    def test_matches_valid_usernames(self):
        assert username.test("user_name") is True

    def test_rejects_invalid_usernames(self):
        assert username.test("ab") is False


class TestPatternStrongPassword:
    def test_matches_strong_passwords(self):
        assert strong_password.test("MyP@ssw0rd") is True

    def test_rejects_weak_passwords(self):
        assert strong_password.test("password") is False


class TestPatternSemver:
    def test_matches_semver(self):
        assert semver.test("1.0.0") is True
        assert semver.test("0.0.1-alpha") is True

    def test_rejects_invalid_semver(self):
        assert semver.test("1.0") is False


class TestPatternMacAddress:
    def test_matches_mac_addresses(self):
        assert mac_address.test("00:1A:2B:3C:4D:5E") is True
        assert mac_address.test("00-1A-2B-3C-4D-5E") is True


# =============================================================================
# REAL WORLD EXAMPLES
# =============================================================================


class TestRealWorldExamples:
    def test_phone_number_pattern(self):
        phone_pattern = (
            optional("+")
            .then(digit(3))
            .then("-")
            .then(digit(3))
            .then("-")
            .then(digit(4))
        )
        assert phone_pattern.test("123-456-7890") is True
        assert phone_pattern.test("+123-456-7890") is True

    def test_date_extraction(self):
        date_pattern = (
            capture(digit(4), "year")
            .then("-")
            .then(capture(digit(2), "month"))
            .then("-")
            .then(capture(digit(2), "day"))
        )
        match = date_pattern.match("2024-03-15")
        assert match is not None
        assert match.group("year") == "2024"
        assert match.group("month") == "03"
        assert match.group("day") == "15"