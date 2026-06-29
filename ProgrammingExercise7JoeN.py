

import re

# ---------------------------------------------------------------------------
# Regular expression used to split the paragraph into sentences.
#
#   (?<=[.!?])   POSITIVE LOOK-BEHIND  -> the split point must come right
#                AFTER a sentence-ending punctuation mark.  The look-behind
#                does not consume the punctuation, so it stays attached to
#                the sentence it ends.
#
#   \s+          one or more whitespace characters between sentences (this
#                IS consumed, so the leading space is stripped from the
#                next sentence).
#
#   (?=[A-Za-z0-9"'])   POSITIVE LOOK-AHEAD -> the next sentence must begin
#                with a letter, a digit, or an opening quote.  The look-ahead
#                does not consume that character, so sentences are free to
#                begin with a number.  Requiring a "real" start character
#                here is what prevents a split inside a decimal number such
#                as 3.50, because the character after that period is a digit
#                that immediately follows the period with no space.
# ---------------------------------------------------------------------------
SENTENCE_SPLIT = re.compile(r'(?<=[.!?])\s+(?=[A-Za-z0-9"\'])')


def split_into_sentences(paragraph):
    """Split a paragraph string into a list of individual sentences.

    Uses the look-ahead / look-behind regular expression above so that
    sentences may begin with numbers while decimal numbers inside a
    sentence are not mistaken for sentence boundaries.

    Returns a list of sentence strings with surrounding whitespace
    removed.  Empty pieces are discarded.
    """
    paragraph = paragraph.strip()
    if not paragraph:
        return []

    pieces = SENTENCE_SPLIT.split(paragraph)
    # Strip each piece and drop anything that ended up empty.
    return [piece.strip() for piece in pieces if piece.strip()]


def display_sentences(sentences):
    """Print each sentence on its own numbered line, then the total count."""
    print("\nIndividual sentences")
    print("-" * 20)
    for number, sentence in enumerate(sentences, start=1):
        print("{}. {}".format(number, sentence))

    print("\nTotal number of sentences: {}".format(len(sentences)))


def get_paragraph():
    """Prompt the user and return the paragraph they enter as one string."""
    print("Enter a paragraph (sentences may begin with numbers).")
    return input("Paragraph: ")


def main():
    """Drive the program: get input, split it, and display the results."""
    paragraph = get_paragraph()
    sentences = split_into_sentences(paragraph)

    if not sentences:
        print("\nNo sentences were entered.")
        return

    display_sentences(sentences)


if __name__ == "__main__":
    main()
