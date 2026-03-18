"""
Trie Data Structure for Dictionary Validation

This module implements a Trie (prefix tree) for efficient dictionary word validation.
Used to check if morphologically extracted base words exist in the lexicon.
"""

import uuid

class TrieNode:
    """A node in the Trie data structure"""

    def __init__(self, char=''):
        self.char = char
        self.children = {}
        self.is_end_of_word = False
        self.id = f"node_{uuid.uuid4().hex[:8]}"

class Trie:
    """Trie data structure for word validation"""

    def __init__(self):
        self.root = TrieNode('START')
        self.word_count = 0

    def insert(self, word):
        """
        Insert a word into the trie

        Args:
            word (str): Word to insert
        """
        current = self.root
        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode(char)
            current = current.children[char]

        if not current.is_end_of_word:
            current.is_end_of_word = True
            self.word_count += 1

    def search(self, word, log_callback=None):
        """
        Search for a word in the trie

        Args:
            word (str): Word to search for
            log_callback (callable): Optional callback for logging search steps

        Returns:
            dict: {'found': bool, 'path': list of node IDs}
        """
        current = self.root
        path_ids = [current.id]

        for i, char in enumerate(word):
            if char not in current.children:
                if log_callback:
                    log_callback(f"DFA Trace: No edge for '{char}' from state '{current.char}'")
                return {"found": False, "path": path_ids}

            current = current.children[char]
            path_ids.append(current.id)

        if current.is_end_of_word:
            if log_callback:
                log_callback(f"DFA Accept: '{word}' reached a final state.")
            return {"found": True, "path": path_ids}
        else:
            if log_callback:
                log_callback(f"DFA Sink: '{word}' reached a non-accepting state.")
            return {"found": False, "path": path_ids}

    def load_from_file(self, filepath):
        """
        Load words from a file into the trie

        Args:
            filepath (str): Path to file containing words (one per line)
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip().lower()
                    if word:
                        self.insert(word)
        except FileNotFoundError:
            # Fallback to sample dictionary
            fallback_words = ["happy", "run", "study", "stop", "fast", "jump", "love", "hope", "care", "play"]
            for word in fallback_words:
                self.insert(word)

    def load_from_list(self, words):
        """
        Load words from a list into the trie

        Args:
            words (list): List of words to insert
        """
        for word in words:
            self.insert(word.lower().strip())

    def get_words(self):
        """
        Get all words in the trie

        Returns:
            list: All words stored in the trie
        """
        words = []

        def traverse(node, current_word):
            if node.is_end_of_word:
                words.append(current_word)

            for char, child in sorted(node.children.items()):
                traverse(child, current_word + char)

        traverse(self.root, "")
        return words

    def __len__(self):
        """Return the number of words in the trie"""
        return self.word_count