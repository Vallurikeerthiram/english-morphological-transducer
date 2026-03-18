"""
English Morphological Analyzer

Main module for morphological analysis using FST rules and Trie validation.
Provides the core functionality for extracting base words from derived forms.
"""

from .morphological_rules import generate_candidates
from .trie import Trie

class MorphologicalAnalyzer:
    """Main morphological analysis engine"""

    def __init__(self, dictionary_path=None, custom_words=None):
        """
        Initialize the morphological analyzer

        Args:
            dictionary_path (str): Path to dictionary file (optional)
            custom_words (list): List of custom words for trie (optional)
        """
        self.trie = Trie()

        if custom_words:
            self.trie.load_from_list(custom_words)
        elif dictionary_path:
            self.trie.load_from_file(dictionary_path)
        else:
            # Load default dictionary from project folder
            import os
            default_dict = os.path.join(os.path.dirname(__file__), '..', 'project', 'words_alpha.txt')
            self.trie.load_from_file(default_dict)

    def analyze_word(self, word, include_logs=False):
        """
        Analyze a word morphologically to find its base form

        Args:
            word (str): Word to analyze
            include_logs (bool): Whether to include detailed logs

        Returns:
            dict: Analysis result with base word, rule applied, and optional logs
        """
        if not word or not word.strip():
            return {
                "input_word": word,
                "base_word": word,
                "rule_applied": "Empty input",
                "found_in_dictionary": False,
                "logs": ["Empty input"] if include_logs else []
            }

        word = word.lower().strip()
        logs = []

        def log_callback(message):
            if include_logs:
                logs.append(message)

        log_callback(f"LEXICAL ANALYSIS: \"{word}\"")

        # Generate morphological candidates
        candidates = generate_candidates(word, log_callback)

        # Try candidates in order until we find one in the dictionary
        final_base = word
        rule_applied = "Self (no transformation)"
        found = False

        for candidate in candidates:
            candidate_word = candidate["word"]
            log_callback(f"Traversing DFA for: \"{candidate_word}\"")
            result = self.trie.search(candidate_word, log_callback)

            if result["found"]:
                final_base = candidate_word
                rule_applied = candidate["rule"]
                found = True
                break

        return {
            "input_word": word,
            "base_word": final_base,
            "rule_applied": rule_applied,
            "found_in_dictionary": found,
            "candidates_checked": len(candidates),
            "dictionary_size": len(self.trie),
            "logs": logs
        }

    def analyze_multiple_words(self, words, include_logs=False):
        """
        Analyze multiple words at once

        Args:
            words (list): List of words to analyze

        Returns:
            list: List of analysis results
        """
        return [self.analyze_word(word, include_logs) for word in words]

    def get_dictionary_info(self):
        """
        Get information about the loaded dictionary

        Returns:
            dict: Dictionary statistics
        """
        return {
            "word_count": len(self.trie),
            "sample_words": self.trie.get_words()[:10]  # First 10 words as sample
        }

    def update_dictionary(self, words):
        """
        Add words to the dictionary

        Args:
            words (list): Words to add
        """
        self.trie.load_from_list(words)