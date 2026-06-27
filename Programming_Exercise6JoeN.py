"""
Input Validator - Phone Number, SSN, and Zip Code Validation
Uses regular expressions to validate common US data formats.
"""

import re


# ─────────────────────────────────────────────
# Validation Functions
# ─────────────────────────────────────────────

def validate_phone_number(phone: str) -> bool:
    """
    Validates US phone numbers.

    Accepted formats:
        (123) 456-7890
        123-456-7890
        123.456.7890
        1234567890
        +1 123 456 7890
        +11234567890

    Returns True if valid, False otherwise.
    """
    pattern = re.compile(
        r"""
        ^                          # start of string
        (\+1[\s\-]?)?              # optional country code +1 (with optional space or dash)
        (\(\d{3}\)[\s\-]?         # area code in parentheses: (123) or (123)-
        |\d{3}[\s\-\.]?)          # OR plain area code: 123- or 123. or 123
        \d{3}                      # first 3 digits
        [\s\-\.]?                  # optional separator
        \d{4}                      # last 4 digits
        $                          # end of string
        """,
        re.VERBOSE,
    )
    return bool(pattern.match(phone.strip()))


def validate_ssn(ssn: str) -> bool:
    """
    Validates US Social Security Numbers.

    Accepted format:
        XXX-XX-XXXX  (with dashes)
        XXXXXXXXX    (9 digits, no dashes)

    Rules enforced:
        - Area number (first 3 digits) cannot be 000 or 666
        - Area number cannot be 900–999
        - Group number (middle 2 digits) cannot be 00
        - Serial number (last 4 digits) cannot be 0000

    Returns True if valid, False otherwise.
    """
    pattern = re.compile(
        r"""
        ^                          # start of string
        (?!000)                    # area cannot be 000
        (?!666)                    # area cannot be 666
        (?!9\d{2})                 # area cannot be 900-999
        \d{3}                      # area: 3 digits
        [-]?                       # optional dash
        (?!00)                     # group cannot be 00
        \d{2}                      # group: 2 digits
        [-]?                       # optional dash
        (?!0000)                   # serial cannot be 0000
        \d{4}                      # serial: 4 digits
        $                          # end of string
        """,
        re.VERBOSE,
    )
    return bool(pattern.match(ssn.strip()))


def validate_zip_code(zip_code: str) -> bool:
    """
    Validates US ZIP codes.

    Accepted formats:
        12345          (5-digit)
        12345-6789     (ZIP+4 with dash)
        12345 6789     (ZIP+4 with space)

    Returns True if valid, False otherwise.
    """
    pattern = re.compile(
        r"""
        ^               # start of string
        \d{5}           # exactly 5 digits
        (               # optional ZIP+4 extension
            [\s\-]      # separator: space or dash
            \d{4}       # exactly 4 more digits
        )?              # extension is optional
        $               # end of string
        """,
        re.VERBOSE,
    )
    return bool(pattern.match(zip_code.strip()))



# Automated Tests


def run_tests() -> None:
    """Runs a suite of valid and invalid test cases for all three validators."""

    # Phone Number Tests
    phone_tests = [
        # (input, expected_result, description)
        ("(123) 456-7890",  True,  "Standard format with parentheses"),
        ("123-456-7890",    True,  "Dash-separated"),
        ("123.456.7890",    True,  "Dot-separated"),
        ("1234567890",      True,  "10 digits, no separators"),
        ("+1 123 456 7890", True,  "Country code with spaces"),
        ("+11234567890",    True,  "Country code, no separators"),
        ("(123)456-7890",   True,  "Parentheses, no space before digits"),
        ("123 456 7890",    True,  "Space-separated"),
        ("12345",           False, "Too short"),
        ("(123) 456-78901", False, "Too many digits"),
        ("abc-def-ghij",    False, "Non-numeric characters"),
        ("(12) 456-7890",   False, "Area code too short"),
        ("",                False, "Empty string"),
    ]

    # ── SSN Tests ───────────────────────────────────────────────────
    ssn_tests = [
        ("123-45-6789",  True,  "Standard dashed format"),
        ("123456789",    True,  "9 digits, no dashes"),
        ("001-45-6789",  True,  "Low area number (valid)"),
        ("000-45-6789",  False, "Area = 000 (invalid)"),
        ("666-45-6789",  False, "Area = 666 (invalid)"),
        ("900-45-6789",  False, "Area 900-999 (invalid)"),
        ("123-00-6789",  False, "Group = 00 (invalid)"),
        ("123-45-0000",  False, "Serial = 0000 (invalid)"),
        ("12-345-6789",  False, "Wrong grouping"),
        ("123-456-789",  False, "Wrong grouping (too many in group)"),
        ("abc-de-fghi",  False, "Non-numeric"),
        ("",             False, "Empty string"),
    ]

    # ── ZIP Code Tests ──────────────────────────────────────────────
    zip_tests = [
        ("12345",       True,  "Standard 5-digit ZIP"),
        ("12345-6789",  True,  "ZIP+4 with dash"),
        ("12345 6789",  True,  "ZIP+4 with space"),
        ("00501",       True,  "Lowest valid ZIP (Holtsville, NY)"),
        ("99950",       True,  "High ZIP (Ketchikan, AK)"),
        ("1234",        False, "Only 4 digits"),
        ("123456",      False, "6 digits (no extension separator)"),
        ("12345-678",   False, "Extension too short (3 digits)"),
        ("12345-67890", False, "Extension too long (5 digits)"),
        ("ABCDE",       False, "Letters instead of digits"),
        ("",            False, "Empty string"),
    ]

    def run_group(label: str, tests: list) -> tuple:
        passed = 0
        failed = 0
        print(f"\n{'─' * 55}")
        print(f"  {label}")
        print(f"{'─' * 55}")
        for value, expected, description in tests:
            if label.startswith("Phone"):
                result = validate_phone_number(value)
            elif label.startswith("SSN"):
                result = validate_ssn(value)
            else:
                result = validate_zip_code(value)

            status = "PASS" if result == expected else "FAIL"
            if result == expected:
                passed += 1
            else:
                failed += 1

            display = repr(value) if value else "''"
            print(f"  [{status}]  {display:<22} | {description}")
        return passed, failed

    total_pass = 0
    total_fail = 0

    for label, tests in [
        ("Phone Number Tests", phone_tests),
        ("SSN Tests", ssn_tests),
        ("ZIP Code Tests", zip_tests),
    ]:
        p, f = run_group(label, tests)
        total_pass += p
        total_fail += f

    print(f"\n{'═' * 55}")
    print(f"  Results: {total_pass} passed, {total_fail} failed "
          f"out of {total_pass + total_fail} total tests")
    print(f"{'═' * 55}\n")



# Interactive Main Function


def main() -> None:
    """Prompts the user for input and validates phone number, SSN, and ZIP code."""

    print("\n" + "═" * 50)
    print("   Input Validator — Phone | SSN | ZIP Code")
    print("═" * 50)

    # Phone Number
    phone = input("\nEnter a phone number: ").strip()
    if validate_phone_number(phone):
        print(f"  ✓  '{phone}' is a VALID phone number.")
    else:
        print(f"  ✗  '{phone}' is NOT a valid phone number.")

    # Social Security Number
    ssn = input("\nEnter a Social Security Number (SSN): ").strip()
    if validate_ssn(ssn):
        print(f"  ✓  '{ssn}' is a VALID SSN.")
    else:
        print(f"  ✗  '{ssn}' is NOT a valid SSN.")

    # ZIP code
    zip_code = input("\nEnter a ZIP code: ").strip()
    if validate_zip_code(zip_code):
        print(f"  ✓  '{zip_code}' is a VALID ZIP code.")
    else:
        print(f"  ✗  '{zip_code}' is NOT a valid ZIP code.")

    print("\n" + "═" * 50 + "\n")



# Entry Point

if __name__ == "__main__":
    print("\nRunning automated test suite first...\n")
    run_tests()
    main()
