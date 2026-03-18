# English Morphological Analysis API

A FastAPI-based REST API that provides morphological analysis for English words, extracting base forms from derived words using Finite State Transducers and Trie validation.

## Features

- **Single Word Analysis**: Analyze individual words morphologically
- **Batch Processing**: Analyze multiple words in one request
- **Custom Dictionary**: Update the dictionary with custom words
- **Detailed Logging**: Optional detailed processing logs
- **RESTful API**: Clean, documented endpoints
- **CORS Enabled**: Ready for web applications

## Quick Start

### Installation

```bash
cd api
pip install -r requirements.txt
```

### Run the API

```bash
python api.py
```

The API will be available at `http://localhost:8000`

### API Documentation

- **Interactive Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Docs**: `http://localhost:8000/redoc` (ReDoc)

## API Endpoints

### GET `/analyze`
Analyze a single word morphologically.

**Parameters:**
- `word` (string, required): Word to analyze
- `include_logs` (boolean, optional): Include detailed processing logs

**Example:**
```bash
curl "http://localhost:8000/analyze?word=running&include_logs=true"
```

**Response:**
```json
{
  "input_word": "running",
  "base_word": "run",
  "rule_applied": "ing -> '' + Undouble",
  "found_in_dictionary": true,
  "candidates_checked": 8,
  "dictionary_size": 370105,
  "logs": [
    "LEXICAL ANALYSIS: \"running\"",
    "Rule Match: 'running' -> 'runing' (ing -> '' + Undouble)",
    "Traversing DFA for: \"runing\"",
    "DFA Trace: No edge for 'i' from state 'n'",
    "Traversing DFA for: \"run\"",
    "DFA Accept: 'run' reached a final state."
  ]
}
```

### POST `/analyze/batch`
Analyze multiple words in a single request.

**Request Body:**
```json
{
  "words": ["running", "happiest", "studies"],
  "include_logs": false
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/analyze/batch" \
     -H "Content-Type: application/json" \
     -d '{"words": ["running", "happiest"], "include_logs": false}'
```

### GET `/dictionary`
Get information about the loaded dictionary.

**Response:**
```json
{
  "word_count": 370105,
  "sample_words": ["a", "aa", "aaa", "aah", "aahed", "aahing", "aahs", "aal", "aalii", "aaliis"]
}
```

### POST `/dictionary/update`
Add words to the dictionary.

**Request Body:**
```json
{
  "words": ["customword1", "customword2"]
}
```

## Python Usage

You can also use the morphological analyzer directly in Python:

```python
from morphological_analyzer import MorphologicalAnalyzer

# Initialize with default dictionary
analyzer = MorphologicalAnalyzer()

# Analyze a word
result = analyzer.analyze_word("running", include_logs=True)
print(f"Base word: {result['base_word']}")
print(f"Rule applied: {result['rule_applied']}")

# Analyze multiple words
results = analyzer.analyze_multiple_words(["running", "happiest", "studies"])
for result in results:
    print(f"{result['input_word']} -> {result['base_word']}")
```

## Morphological Rules

The API implements 101 morphological transformation rules organized in priority layers:

1. **Y/I Alternations**: happiest → happy, studies → study
2. **Progressive/Past**: running → run, walked → walk
3. **Comparative/Superlative**: bigger → big, fastest → fast
4. **Plurals**: knives → knife, children → child
5. **Derivational**: happiness → happy, creation → create
6. **Basic Inflection**: cats → cat, running → run

## Architecture

- **morphological_rules.py**: FST rule definitions and candidate generation
- **trie.py**: Trie data structure for dictionary validation
- **morphological_analyzer.py**: Core analysis engine
- **api.py**: FastAPI application with REST endpoints

## Performance

- **Dictionary Size**: 370,000+ words
- **Lookup Time**: O(word_length) for trie searches
- **Rule Processing**: Fast rule-based transformations
- **Memory Efficient**: Trie structure optimized for English words

## Error Handling

The API includes comprehensive error handling:
- Invalid input validation
- Dictionary loading fallbacks
- Detailed error messages
- HTTP status codes

## Development

### Project Structure
```
api/
├── __init__.py
├── api.py                    # FastAPI application
├── morphological_analyzer.py # Core analysis engine
├── morphological_rules.py    # FST rules
├── trie.py                   # Trie implementation
├── requirements.txt          # Python dependencies
└── README.md                # This file
```

### Testing the API

```bash
# Test single word
curl "http://localhost:8000/analyze?word=running"

# Test batch analysis
curl -X POST "http://localhost:8000/analyze/batch" \
     -H "Content-Type: application/json" \
     -d '{"words": ["run", "running", "runner"]}'

# Check dictionary info
curl "http://localhost:8000/dictionary"
```

## License

This API is part of the English Morphological Transducer project.