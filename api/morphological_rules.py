"""
English Morphological Rules for Base Word Extraction

This module implements the Finite State Transducer (FST) rules for morphological analysis
of English words. The rules are organized in priority layers to handle different types
of morphological transformations systematically.

Based on the comprehensive catalog from ENGLISH_MORPHOLOGY_RULE_NOTE.md
"""

class MorphologicalRule:
    """Represents a single morphological transformation rule"""

    def __init__(self, suffix, replace, name, undouble=False, add_e=False):
        self.suffix = suffix
        self.replace = replace
        self.name = name
        self.undouble = undouble  # Remove double consonants (running -> run)
        self.add_e = add_e        # Add silent E (loving -> love)

# FST Rule Layers - Priority-based application
FST_RULE_LAYERS = [
    # LAYER 1: High-priority Superlative/Comparative y-alternations
    [
        MorphologicalRule("iness", "y", "iness -> y"),
        MorphologicalRule("iest", "y", "iest -> y"),
        MorphologicalRule("ier", "y", "ier -> y"),
        MorphologicalRule("ily", "y", "ily -> y")
    ],
    # LAYER 2: Plurals and y-alternations
    [
        MorphologicalRule("ied", "y", "ied -> y"),
        MorphologicalRule("ied", "ie", "ied -> ie"),
        MorphologicalRule("ies", "y", "ies -> y"),
        MorphologicalRule("ies", "ie", "ies -> ie"),
        MorphologicalRule("ying", "ie", "ying -> ie")
    ],
    # LAYER 3: Progressive and Past (with undoubling/silent-e)
    [
        MorphologicalRule("ing", "", "ing -> ''", undouble=True, add_e=True),
        MorphologicalRule("ed", "", "ed -> ''", undouble=True, add_e=True),
        MorphologicalRule("king", "c", "king -> c"),
        MorphologicalRule("ked", "c", "ked -> c")
    ],
    # LAYER 4: Degree and Plurals
    [
        MorphologicalRule("er", "", "er -> ''", undouble=True, add_e=True),
        MorphologicalRule("est", "", "est -> ''", undouble=True, add_e=True),
        MorphologicalRule("ves", "f", "ves -> f"),
        MorphologicalRule("ves", "fe", "ves -> fe"),
        MorphologicalRule("men", "man", "men -> man"),
        MorphologicalRule("ses", "sis", "ses -> sis")
    ],
    # LAYER 5: Core Derivational Reversal
    [
        MorphologicalRule("ability", "able", "ability -> able"),
        MorphologicalRule("ibility", "ible", "ibility -> ible"),
        MorphologicalRule("ization", "ize", "ization -> ize"),
        MorphologicalRule("isation", "ise", "isation -> ise"),
        MorphologicalRule("ation", "ate", "ation -> ate"),
        MorphologicalRule("ness", "", "ness -> ''"),
        MorphologicalRule("ment", "", "ment -> ''"),
        MorphologicalRule("ship", "", "ship -> ''"),
        MorphologicalRule("hood", "", "hood -> ''"),
        MorphologicalRule("dom", "", "dom -> ''"),
        MorphologicalRule("fully", "ful", "fully -> ful"),
        MorphologicalRule("ful", "", "ful -> ''"),
        MorphologicalRule("less", "", "less -> ''"),
        MorphologicalRule("ical", "ic", "ical -> ic"),
        MorphologicalRule("ly", "", "ly -> ''"),
        MorphologicalRule("ity", "e", "ity -> e"),
        MorphologicalRule("ity", "", "ity -> ''")
    ],
    # LAYER 6: Basic Inflection
    [
        MorphologicalRule("es", "", "es -> ''"),
        MorphologicalRule("s", "", "s -> ''")
    ]
]

def generate_candidates(word, log_callback=None):
    """
    Generate morphological candidates for a word using FST rules

    Args:
        word (str): Input word to analyze
        log_callback (callable): Optional callback for logging rule applications

    Returns:
        list: List of candidate dictionaries with 'word' and 'rule' keys
    """
    candidates = []

    # Identity check - word itself is always a candidate
    candidates.append({"word": word, "rule": "Self"})

    for layer in FST_RULE_LAYERS:
        for rule in layer:
            if word.endswith(rule.suffix) and len(word) > len(rule.suffix):
                stem = word[:-len(rule.suffix)]

                # Base transformation
                base = stem + rule.replace
                candidates.append({"word": base, "rule": rule.name})

                if log_callback:
                    log_callback(f"Rule Match: '{word}' -> '{base}' ({rule.name})")

                # Consonant Undoubling (running -> run)
                if rule.undouble and len(stem) >= 2 and stem[-1] == stem[-2]:
                    undoubled = stem[:-1]
                    candidates.append({"word": undoubled, "rule": rule.name + " + Undouble"})
                    if log_callback:
                        log_callback(f"Undouble Rule: '{word}' -> '{undoubled}'")

                # Silent E restoration (loving -> love)
                if rule.add_e:
                    with_e = stem + "e"
                    candidates.append({"word": with_e, "rule": rule.name + " + Add-E"})
                    if log_callback:
                        log_callback(f"Silent-E Rule: '{word}' -> '{with_e}'")

    # Remove duplicates while preserving order
    unique_candidates = []
    seen = set()
    for candidate in candidates:
        if candidate["word"] not in seen:
            unique_candidates.append(candidate)
            seen.add(candidate["word"])

    return unique_candidates