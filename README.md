# English Morphological Transducer & Base Word Extractor

## 🎯 What is This Project?

This is a comprehensive **morphological analysis system** for English that implements advanced natural language processing techniques to extract base words from derived forms. The system combines **Finite State Transducers (FST)** with **Trie-based validation** to perform rule-based morphological parsing.

### Core Functionality
- **Morphological Analysis**: Takes inflected/derived words (e.g., "running", "happiest", "studies") and extracts their root/base forms ("run", "happy", "study")
- **Rule-Based Processing**: Uses 101 carefully crafted morphological transformation rules
- **Validation**: Ensures extracted base words exist in a dictionary using efficient trie data structures
- **Interactive Web Interface**: User-friendly tool for real-time morphological analysis

## 🧩 What Problem Does It Solve?

### The Morphological Analysis Challenge
English morphology is complex and irregular. Words change forms through:
- **Inflection**: happy → happier → happiest
- **Derivation**: happy → happiness → happily
- **Spelling Changes**: happy → happier (y→ier)
- **Irregular Forms**: good → better (not "gooder")

Traditional approaches struggle with:
- **Spelling alternations** (y/i changes, doubling rules)
- **Silent-e rules** (hope → hoping vs. hop → hopping)
- **Irregular exceptions** (go → went, not "goed")
- **Ambiguity resolution** (multiple possible base forms)

### Our Solution
This project provides a **practical morphological analyzer** that:
- Handles 101+ morphological patterns systematically
- Prioritizes rules to avoid over-application
- Validates results against real dictionary words
- Provides visual feedback and explanations

## 🚀 What's New & Innovative?

### Advanced Rule Architecture
- **Layered Rule Application**: Rules are organized in priority layers to prevent conflicts
- **Context-Aware Transformations**: Handles spelling changes, silent-e rules, and consonant doubling
- **Comprehensive Coverage**: 101 rules covering inflectional, derivational, and irregular morphology

### Technical Innovations
- **Hybrid FST-Trie Approach**: Combines rule-based FST with dictionary validation
- **Real-Time Web Interface**: Interactive analysis with immediate visual feedback
- **Graph Visualization**: See morphological transformation paths
- **Dual Analysis Modes**: Default dictionary vs. custom dictionary analysis

### Educational Value
- **Complete Documentation**: Every rule is documented with examples
- **Academic Implementation**: Demonstrates compiler design concepts in NLP
- **Open-Source Reference**: Comprehensive morphological rule catalog

## 📋 Prerequisites

- **Web Browser**: Modern browser with JavaScript enabled (Chrome, Firefox, Safari, Edge)
- **No Server Required**: Runs entirely in the browser
- **No Dependencies**: Self-contained HTML/CSS/JS application

## 🏃‍♂️ How to Run It

### Quick Start
1. **Download/Clone** this repository
2. **Navigate** to the `project/` directory
3. **Open** `index.html` in your web browser
4. **Start analyzing** words immediately!

### Detailed Steps
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/english-morphological-transducer.git
cd english-morphological-transducer/project

# Open in browser (or double-click index.html)
# The application runs entirely in your browser
```

## 📖 How to Use It

### Two Analysis Modes

#### Model 1: Auto FST (Default Dictionary)
- **Best for**: General morphological analysis
- **Dictionary**: Pre-loaded with 3,000+ common English words
- **Process**:
  1. Type a derived word (e.g., "running", "happiest", "studies")
  2. System applies FST rules in priority order
  3. Validates base word against dictionary trie
  4. Shows transformation path and result

#### Model 2: Manual FST (Custom Dictionary)
- **Best for**: Domain-specific analysis or testing
- **Dictionary**: User-defined word list
- **Process**:
  1. Enter comma-separated dictionary words
  2. Click "Build Trie (DFA)" to create validation structure
  3. Enter test word for analysis
  4. System finds base forms within your custom vocabulary

### Example Usage

**Input Word**: `happiest`
**Analysis**:
1. Rule `iest → y` applied: `happiest` → `happyest` (invalid)
2. Rule `est → ''` applied: `happyest` → `happy` (valid!)
3. **Result**: Base word = `happy`

**Input Word**: `running`
**Analysis**:
1. Rule `ing → ''` with undoubling: `running` → `runing` (invalid)
2. Rule `ing → ''` with silent-e: `runing` → `run` (valid!)
3. **Result**: Base word = `run`

## 🏗️ Project Structure

```
main/
├── ENGLISH_MORPHOLOGY_RULE_NOTE.md    # Complete rule documentation (101 rules)
├── README.md                          # This file
└── project/
    ├── index.html                     # Main web interface
    ├── script.js                      # Morphological analysis engine
    ├── style.css                      # UI styling
    ├── test_logic_runner.js           # Testing utilities
    └── words_alpha.txt                # Default dictionary (3K+ words)
```

## 🔧 Technical Implementation

### Morphological Rules (101 Total)
- **Y/I Alternations**: happiest → happy, studies → study
- **Progressive/Past**: running → run, walked → walk
- **Comparative/Superlative**: bigger → big, fastest → fast
- **Plurals**: knives → knife, children → child
- **Derivational**: happiness → happy, creation → create
- **Irregular Forms**: went → go, better → good

### Algorithm Flow
1. **Input Processing**: Word segmentation and normalization
2. **Rule Application**: Layered FST transformation (priority-based)
3. **Validation**: Trie lookup for base word existence
4. **Output**: Base word + transformation explanation

### Performance
- **Rule Processing**: O(n) where n = word length
- **Trie Validation**: O(m) where m = base word length
- **Dictionary Size**: 3,000+ words, ~O(1) lookup
- **Browser-Based**: No server overhead

## 🎓 Academic Context

This project demonstrates **Compiler Design** principles applied to **Natural Language Processing**:

- **Finite State Transducers**: Rule-based morphological parsing
- **Trie Data Structures**: Efficient dictionary validation
- **Algorithm Design**: Priority-based rule application
- **User Interface Design**: Educational tool development

## 🤝 Contributing

1. **Study** the rule documentation in `ENGLISH_MORPHOLOGY_RULE_NOTE.md`
2. **Test** new words and edge cases
3. **Propose** additional morphological rules
4. **Improve** the web interface or algorithms

## 📄 License

This project is open-source and available under the MIT License.

## 🙏 Acknowledgments

- **Compiler Design Course**: For providing the academic framework
- **English Morphology Research**: For the comprehensive rule catalog
- **Open-Source Community**: For JavaScript libraries and inspiration

---

**Ready to explore English morphology?** Open `project/index.html` and start analyzing words!