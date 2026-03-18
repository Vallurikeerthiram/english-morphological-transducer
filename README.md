# English Morphological Transducer

A rule-based morphological analysis system for English word forms, implementing Finite State Transducers (FST) and Trie validation for base word extraction.

## Overview

This project demonstrates morphological analysis in compiler design, focusing on English inflectional and derivational morphology. The system uses a comprehensive catalog of 101 morphological rules to analyze derived words and extract their base forms.

## Features

- **Rule-Based FST**: Implements 101 morphological transformation rules for English
- **Trie Validation**: Validates extracted base words against a dictionary trie
- **Web Interface**: Interactive morphological analysis tool with two models:
  - Model 1: Auto FST with default dictionary
  - Model 2: Manual FST with custom dictionary
- **Visualization**: Graph visualization of morphological transformations

## Morphological Rules

The system includes rules for:
- Inflectional morphology (plural, tense, comparison)
- Derivational morphology (prefixes, suffixes)
- Spelling alternations (y/i, vowel changes)
- Irregular forms and exceptions

## Project Structure

- `ENGLISH_MORPHOLOGY_RULE_NOTE.md`: Comprehensive documentation of all 101 implemented rules
- `project/`: Web application files
  - `index.html`: Main interface
  - `script.js`: Morphological analysis logic
  - `style.css`: Styling
  - `test_logic_runner.js`: Testing utilities
  - `words_alpha.txt`: Dictionary file

## Usage

1. Open `project/index.html` in a web browser
2. Choose between Model 1 (default) or Model 2 (custom dictionary)
3. Enter a word to analyze its morphological structure

## Technical Details

- Built with vanilla JavaScript
- Uses vis-network for graph visualization
- Implements deterministic finite automata (DFA) for trie validation
- Rule-based approach to morphological parsing

## Academic Context

This project is part of a Compiler Design course, demonstrating practical applications of formal language theory and automata in natural language processing.