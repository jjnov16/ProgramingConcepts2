"""
Programming_Exercise2JoeN

Scans an email message entered by the user for 30 common spam keywords
and phrases.  Each occurrence of a keyword or phrase adds one point to
the message's "spam score."  The program then displays the total spam
score, a likelihood rating, and every word or phrase that was found.

The list of 30 spam trigger words/phrases was compiled from research
on commonly flagged terms identified by major email providers and
anti-spam organizations (sources include Mailwarm, ActiveCampaign,
HubSpot, MailGenius, and Mailmeteor).

Author: <your name>
"""

import re

# ---------------------------------------------------------------------------
# 30 common spam trigger words and phrases, organized by category.
# Each entry is stored in lowercase for case-insensitive matching.
# ---------------------------------------------------------------------------
SPAM_KEYWORDS = [
    # Financial promises (1-6)
    "act now",
    "click here",
    "buy now",
    "limited time",
    "earn money",
    "make money",

    # Too-good-to-be-true offers (7-12)
    "free",
    "guaranteed",
    "no cost",
    "risk free",
    "winner",
    "congratulations",

    # Urgency / pressure tactics (13-18)
    "urgent",
    "last chance",
    "offer expires",
    "don't delete",
    "exclusive deal",
    "immediate",

    # Health / weight-loss claims (19-22)
    "lose weight",
    "miracle",
    "viagra",
    "anti-aging",

    # Security / phishing lures (23-27)
    "verify your account",
    "account suspended",
    "click below",
    "security alert",
    "update required",

    # Miscellaneous junk signals (28-30)
    "no obligation",
    "unsubscribe",
    "this is not spam",
]


def scan_for_spam(message, keywords):
    """Scan *message* for every keyword/phrase in *keywords*.

    Matching is case-insensitive and counts every occurrence of each
    keyword (a phrase that appears three times adds three points).

    Returns a tuple of:
        spam_score  – int, total number of keyword hits
        found       – dict mapping each found keyword to its count
    """
    lower_message = message.lower()
    spam_score = 0
    found = {}

    for keyword in keywords:
        # re.findall with word boundaries would break multi-word phrases
        # that start/end at punctuation, so we simply count occurrences.
        count = len(re.findall(re.escape(keyword), lower_message))
        if count > 0:
            found[keyword] = count
            spam_score += count

    return spam_score, found


def rate_spam_likelihood(spam_score):
    """Return a human-readable likelihood string based on the spam score.

    Thresholds:
        0       -> Not spam
        1-3     -> Low likelihood
        4-6     -> Medium likelihood
        7-10    -> High likelihood
        11+     -> Very high – almost certainly spam
    """
    if spam_score == 0:
        return "Not Spam"
    elif spam_score <= 3:
        return "Low Likelihood of Spam"
    elif spam_score <= 6:
        return "Medium Likelihood of Spam"
    elif spam_score <= 10:
        return "High Likelihood of Spam"
    else:
        return "Very High – Almost Certainly Spam"


def display_results(spam_score, likelihood, found):
    """Print the spam score, likelihood rating, and matched keywords."""
    print("\n" + "=" * 50)
    print("           SPAM ANALYSIS RESULTS")
    print("=" * 50)
    print("  Spam Score       : {}".format(spam_score))
    print("  Likelihood       : {}".format(likelihood))
    print("-" * 50)

    if found:
        print("  Flagged words/phrases:")
        for keyword, count in found.items():
            label = "({} occurrence{})".format(count,
                                               "s" if count > 1 else "")
            print("    - {:<25s} {}".format('"' + keyword + '"', label))
    else:
        print("  No spam keywords or phrases were detected.")

    print("=" * 50)


def get_email_message():
    """Prompt the user and return the email message they enter."""
    print("Enter the email message you would like to scan for spam.")
    print("(Type or paste the message, then press Enter.)\n")
    return input("Message: ")


def main():
    """Drive the program: collect the message, scan, rate, and display."""
    message = get_email_message()

    if not message.strip():
        print("\nNo message was entered.")
        return

    spam_score, found = scan_for_spam(message, SPAM_KEYWORDS)
    likelihood = rate_spam_likelihood(spam_score)
    display_results(spam_score, likelihood, found)


if __name__ == "__main__":
    main()
