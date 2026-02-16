from .pattern import Pattern

# Email address pattern
email: Pattern = Pattern(
    r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
)

# URL pattern (http/https)
url: Pattern = Pattern(
    r"^https?:\/\/(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&\/=]*)$"
)

# Phone number pattern (international)
phone: Pattern = Pattern(
    r"^\+?[1-9]?[0-9]{0,3}?[-. (]?[0-9]{1,4}[-. )]?[0-9]{1,4}[-. ]?[0-9]{1,9}$"
)

# ISO date pattern (YYYY-MM-DD)
date: Pattern = Pattern(
    r"^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])$"
)

# Time pattern (HH:MM or HH:MM:SS)
time: Pattern = Pattern(
    r"^(?:[01]\d|2[0-3]):[0-5]\d(?::[0-5]\d)?$"
)

# IPv4 address pattern
ipv4: Pattern = Pattern(
    r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$"
)

# IPv6 address pattern
ipv6: Pattern = Pattern(
    r"^(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$"
)

# Hexadecimal color pattern
hex_color: Pattern = Pattern(
    r"^#(?:[0-9a-fA-F]{3}){1,2}$"
)

# Hexadecimal string pattern
hex_string: Pattern = Pattern(
    r"^[0-9a-fA-F]+$"
)

# UUID pattern (v1-v5)
uuid: Pattern = Pattern(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$"
)

# URL slug pattern
slug: Pattern = Pattern(
    r"^[a-z0-9]+(?:-[a-z0-9]+)*$"
)

# Hashtag pattern
hashtag: Pattern = Pattern(
    r"#[a-zA-Z0-9_]+"
)

# @mention pattern
mention: Pattern = Pattern(
    r"@[a-zA-Z0-9_]+"
)

# Credit card number pattern (basic)
credit_card: Pattern = Pattern(
    r"^(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})$"
)

# US Social Security Number pattern
ssn: Pattern = Pattern(
    r"^\d{3}-\d{2}-\d{4}$"
)

# US ZIP code pattern
zip_code: Pattern = Pattern(
    r"^\d{5}(?:-\d{4})?$"
)

# Username pattern (alphanumeric + underscore, 3-16 chars)
username: Pattern = Pattern(
    r"^[a-zA-Z0-9_]{3,16}$"
)

# Strong password pattern
strong_password: Pattern = Pattern(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
)

# Semantic version pattern
semver: Pattern = Pattern(
    r"^(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)\.(?:0|[1-9]\d*)(?:-[a-zA-Z0-9]+)?$"
)

# MAC address pattern
mac_address: Pattern = Pattern(
    r"^(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$"
)


__all__ = [
    "email",
    "url",
    "phone",
    "date",
    "time",
    "ipv4",
    "ipv6",
    "hex_color",
    "hex_string",
    "uuid",
    "slug",
    "hashtag",
    "mention",
    "credit_card",
    "ssn",
    "zip_code",
    "username",
    "strong_password",
    "semver",
    "mac_address",
]