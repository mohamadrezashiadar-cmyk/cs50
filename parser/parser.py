import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP2 VP | S Conj S

NP -> N | Det N | Det AP N | AP N
NP2 -> NP PP
AP -> Adj | Adj AP
PP -> P NP | P NP2

VP -> V | V NP | V NP2 | V PP
VP -> Adv VP | VP Adv | VP Conj VP
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    try:
        tokens = nltk.word_tokenize(sentence)
    except LookupError:
        tokens = nltk.tokenize.wordpunct_tokenize(sentence)

    return [
        word.lower()
        for word in tokens
        if any(char.isalpha() for char in word)
    ]


def np_chunk(tree):
    chunks = []
    for subtree in tree.subtrees(lambda t: t.label() == "NP"):
        has_inner_np = any(
            inner.label() in ("NP", "NP2")
            for inner in subtree.subtrees(lambda t: t is not subtree)
        )
        if not has_inner_np:
            chunks.append(subtree)
    return chunks


if __name__ == "__main__":
    main()